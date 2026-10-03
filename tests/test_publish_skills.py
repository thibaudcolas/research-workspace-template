import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urljoin

from mkdocs.exceptions import PluginError

SPEC = importlib.util.spec_from_file_location(
    "publish_skills", Path(__file__).resolve().parents[1] / "scripts/publish_skills.py"
)
assert SPEC is not None and SPEC.loader is not None
publisher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publisher)


class PublishingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / ".agents/skills/example"
        self.skill.mkdir(parents=True)
        self.entrypoint = self.skill / "SKILL.md"
        self.entrypoint.write_text(
            "---\nname: example\ndescription: An example skill\n"
            'metadata:\n  version: "1.2.3"\n---\n\n# Example\n',
            encoding="utf-8",
        )
        self.site = self.root / "site"
        self.config = {
            "config_file_path": str(self.root / "mkdocs.yml"),
            "site_dir": str(self.site),
            "site_name": "Example workspace",
            "site_url": "https://example.com/project/",
        }

    def test_publishes_resources_and_resolvable_catalogs(self):
        resource = self.skill / "references/guide.md"
        resource.parent.mkdir()
        resource.write_text("# Supporting reference\n", encoding="utf-8")
        publisher.on_post_build(self.config)
        output = self.site / ".well-known/agent-skills"
        self.assertEqual(
            (output / "example/references/guide.md").read_bytes(), resource.read_bytes()
        )
        self.assertEqual(
            (output / "example/SKILL.md").read_bytes(), self.entrypoint.read_bytes()
        )
        index = json.loads((output / "index.json").read_text())
        entry = index["skills"][0]
        self.assertEqual(
            entry["digest"],
            "sha256:" + hashlib.sha256(self.entrypoint.read_bytes()).hexdigest(),
        )
        catalog = json.loads((self.site / ".well-known/ai-catalog.json").read_text())
        self.assertEqual(
            urljoin(
                self.config["site_url"] + ".well-known/agent-skills/index.json",
                entry["url"],
            ),
            catalog["entries"][0]["url"],
        )
        self.assertEqual(catalog["entries"][0]["version"], "1.2.3")
        self.assertEqual(catalog["host"]["identifier"], "did:web:example.com:project")

    def test_dirty_build_removes_deleted_skills(self):
        publisher.on_post_build(self.config)
        self.entrypoint.unlink()
        publisher.on_post_build(self.config)
        output = self.site / ".well-known/agent-skills"
        self.assertFalse((output / "example").exists())
        self.assertEqual(json.loads((output / "index.json").read_text())["skills"], [])

    def test_rejects_invalid_metadata(self):
        for content in (
            "# No front matter",
            "---\n[broken YAML\n---",
            "---\n- a list\n---",
            "---\nname: wrong-directory\ndescription: Example\n---",
            "---\nname: example\ndescription: ''\n---",
            "---\nname: example\ndescription: Example\nmetadata: []\n---",
            "---\nname: example\ndescription: Example\nmetadata:\n  version: 1\n---",
        ):
            with self.subTest(content=content):
                self.entrypoint.write_text(content, encoding="utf-8")
                with self.assertRaises(PluginError):
                    publisher.on_post_build(self.config)

    def test_rejects_symlinked_resources(self):
        (self.skill / "outside").symlink_to(self.root)
        with self.assertRaises(PluginError):
            publisher.on_post_build(self.config)

    def test_requires_absolute_site_url(self):
        for url in ("", "/project/", "https://example.com/?query=yes"):
            with self.subTest(url=url), self.assertRaises(PluginError):
                publisher.on_post_build({**self.config, "site_url": url})
