"""Exercise the real documentation configuration without publishing test pages."""

import copy
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse
from xml.etree.ElementTree import Element

import yaml
from mkdocs.commands.build import build
from mkdocs.config import load_config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import InclusionLevel, get_files
from pymdownx.snippets import SnippetMissingError  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"
# Source-only Markdown must be excluded deliberately, with a reason. Published
# pages, including those outside nav, must have Markdown exports.
EXPORT_EXCLUSIONS = {
    "contributing/abbreviations.md": "Shared snippet definitions, not a page.",
}
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class Document(HTMLParser):
    def __init__(self, html: str) -> None:
        super().__init__()
        self.root = Element("document")
        self.stack = [self.root]
        self.feed(html)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Element(tag, {key: value or "" for key, value in attrs})
        self.stack[-1].append(node)
        if tag not in VOID_ELEMENTS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID_ELEMENTS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        node = self.stack[-1]
        if len(node):
            node[-1].tail = (node[-1].tail or "") + data
        else:
            node.text = (node.text or "") + data


def content(node: Element) -> str:
    return "".join(node.itertext())


class DocumentationTests(unittest.TestCase):
    temp: tempfile.TemporaryDirectory[str]
    docs: Path
    site: Path
    settings: dict[str, Any]
    document: Element
    pages: dict[str, str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.docs = Path(cls.temp.name) / "docs"
        cls.site = Path(cls.temp.name) / "site"
        shutil.copytree(ROOT / "docs", cls.docs)
        shutil.copy(FIXTURES / "features.md", cls.docs / "features.md")
        shutil.copy(FIXTURES / "feature-snippet.txt", cls.docs / "feature-snippet.txt")
        cls.settings = yaml.safe_load((ROOT / "mkdocs.yml").read_text())
        cls.settings["nav"].append({"Documentation features": "features.md"})
        for extension in cls.settings["markdown_extensions"]:
            if isinstance(extension, dict) and "pymdownx.snippets" in extension:
                extension["pymdownx.snippets"]["base_path"] = str(cls.docs)
        for plugin in cls.settings["plugins"]:
            if isinstance(plugin, dict):
                if "git-revision-date-localized" in plugin:
                    # Temporary docs have no Git history; revision dates are not
                    # under test. Also avoid sandbox-restricted multiprocessing.
                    plugin["git-revision-date-localized"]["enabled"] = False
                    plugin["git-revision-date-localized"][
                        "enable_parallel_processing"
                    ] = False
                if "llmstxt" in plugin:
                    plugin["llmstxt"]["sections"]["Test fixture"] = ["features.md"]
        config = cls.make_config()
        files = get_files(config)
        cls.pages = {
            file.src_uri: file.dest_uri for file in files.documentation_pages()
        }
        # Unique source markers in temporary copies distinguish pages even when
        # they have identical headings or content. Never modify the real docs.
        for source in cls.pages:
            path = cls.docs / source
            path.write_text(path.read_text() + f"\n\n{cls.export_marker(source)}\n")
        build(config)
        page = Document((cls.site / "features/index.html").read_text()).root
        cls.document = next(page.iter("article"))

    @classmethod
    def make_config(cls) -> MkDocsConfig:
        return load_config(
            config_file=str(ROOT / "mkdocs.yml"),
            docs_dir=str(cls.docs),
            site_dir=str(cls.site),
            strict=True,
            nav=copy.deepcopy(cls.settings["nav"]),
            markdown_extensions=copy.deepcopy(cls.settings["markdown_extensions"]),
            plugins=copy.deepcopy(cls.settings["plugins"]),
        )

    def test_tables_and_shared_abbreviations(self) -> None:
        table = self.document.find(".//table")
        assert table is not None
        self.assertEqual(
            [content(cell) for cell in table.iter("th")], ["Finding", "Status"]
        )
        self.assertIn("Rendering works", content(table))
        abbreviations = {
            content(node): node.get("title") for node in self.document.iter("abbr")
        }
        self.assertEqual(abbreviations["PSF"], "Python Software Foundation")

    def test_footnote_links_resolve_in_both_directions(self) -> None:
        ids = {node.get("id") for node in self.document.iter() if node.get("id")}
        references = [
            node
            for node in self.document.iter("a")
            if "footnote-ref" in node.get("class", "").split()
        ]
        backlinks = [
            node
            for node in self.document.iter("a")
            if "footnote-backref" in node.get("class", "").split()
        ]
        self.assertEqual(len(references), 1)
        self.assertEqual(len(backlinks), 1)
        for link in references + backlinks:
            self.assertIn(unquote(link.attrib["href"]).removeprefix("#"), ids)
        self.assertIn("A traceable source", content(self.document))

    def test_nested_code_details_tabs_and_tasks(self) -> None:
        admonition = next(
            node
            for node in self.document.iter("div")
            if "admonition" in node.get("class", "").split()
        )
        code = admonition.find(".//pre/code")
        assert code is not None
        self.assertIn('print("Nested example")', content(code))
        details = self.document.find(".//details")
        assert details is not None
        summary = details.find("summary")
        assert summary is not None
        self.assertEqual(content(summary), "Supporting evidence")
        self.assertIn("Evidence remains available", content(details))
        labels = {content(node) for node in self.document.iter("label")}
        self.assertTrue({"Observation", "Interpretation"}.issubset(labels))
        checkboxes = [
            node
            for node in self.document.iter("input")
            if node.get("type") == "checkbox"
        ]
        self.assertEqual(len(checkboxes), 2)
        self.assertEqual(
            ["checked" in node.attrib for node in checkboxes], [True, False]
        )

    def test_snippets_are_rendered(self) -> None:
        self.assertIn(
            "research evidence",
            [content(node) for node in self.document.iter("strong")],
        )
        self.assertNotIn("--8<--", content(self.document))

    def test_missing_snippet_fails_build(self) -> None:
        fixture = self.docs / "features.md"
        original = fixture.read_text()
        self.addCleanup(fixture.write_text, original)
        fixture.write_text(original + '\n--8<-- "missing-research-snippet.txt"\n')
        # Authors must get the missing filename, not silently lose content.
        config = self.make_config()
        config.site_dir = str(Path(self.temp.name) / "broken-site")
        with self.assertRaisesRegex(
            SnippetMissingError, "missing-research-snippet.txt"
        ):
            build(config)

    def test_markdown_alternatives_and_full_export(self) -> None:
        self.assert_markdown_exports(self.site)
        self.assertIn("research evidence", (self.site / "llms-full.txt").read_text())

    @staticmethod
    def export_marker(source: str) -> str:
        return f"Export coverage marker: {source}."

    def test_export_exclusions_are_explicit(self) -> None:
        pages = get_files(self.make_config()).documentation_pages(
            inclusion=InclusionLevel.all
        )
        excluded = {
            file.src_uri
            for file in pages
            if file.inclusion in (InclusionLevel.EXCLUDED, InclusionLevel.DRAFT)
        }
        self.assertEqual(
            excluded,
            set(EXPORT_EXCLUSIONS),
            "Document intentional source exclusions in EXPORT_EXCLUSIONS; "
            "published pages must be exported.",
        )

    def assert_markdown_exports(self, site: Path) -> None:
        base_path = urlparse(self.settings["site_url"]).path
        exported = (site / "llms-full.txt").read_text()
        index = (site / "llms.txt").read_text()
        self.assertTrue(self.pages, "No documentation pages found for export checks")
        for source, relative in self.pages.items():
            document = Document((site / relative).read_text()).root
            alternatives = [
                node
                for node in document.iter("link")
                if node.get("rel") == "alternate"
                and node.get("type", "").startswith("text/markdown")
            ]
            self.assertEqual(len(alternatives), 1, f"{source}: Markdown alternative")
            href = alternatives[0].attrib["href"]
            path = unquote(urlparse(href).path)
            self.assertTrue(path.startswith(base_path), f"{source}: {href}")
            target = site / path.removeprefix(base_path)
            self.assertEqual(
                target,
                (site / relative).with_suffix(".md"),
                f"{source}: Markdown alternative points to another page",
            )
            self.assertTrue(
                target.is_file(),
                f"{source}: Markdown alternative missing; update llmstxt.sections",
            )
            markdown = target.read_text()
            self.assertIn(self.export_marker(source), markdown, f"{source}: raw export")
            self.assertIn(f"]({href})", index, f"{source}: missing from llms.txt")
            self.assertIn(
                markdown, exported, f"{source}: content missing from llms-full.txt"
            )

    def test_export_check_detects_omitted_section(self) -> None:
        config = self.make_config()
        del config.plugins["llmstxt"].config["sections"]["Test fixture"]
        site = Path(self.temp.name) / "omitted-section-site"
        config.site_dir = str(site)
        build(config)
        with self.assertRaisesRegex(
            AssertionError, r"features\.md: Markdown alternative missing"
        ):
            self.assert_markdown_exports(site)

    def test_export_check_detects_missing_full_content(self) -> None:
        site = Path(self.temp.name) / "incomplete-export-site"
        shutil.copytree(self.site, site)
        full = site / "llms-full.txt"
        fixture_markdown = (site / "features/index.md").read_text()
        full.write_text(full.read_text().replace(fixture_markdown, ""))
        with self.assertRaisesRegex(
            AssertionError, r"features\.md: content missing from llms-full\.txt"
        ):
            self.assert_markdown_exports(site)
