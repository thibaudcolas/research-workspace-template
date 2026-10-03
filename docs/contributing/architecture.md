# Project architecture

How the workspace is organized, and the tooling that supports it.

## Content layers

We organize information across a small number of layers:

1. [Contributing](README.md): guidance on how to work within this workspace.
2. [Knowledge base](../knowledge-base/README.md): general-purpose information relevant for a wide range of tasks.
3. Projects, like [Project A](../project-a/README.md): information about a specific project.

Each section folder uses a `README.md` as its landing page, so it also renders when browsing the folder on GitHub.

<!-- Update the layers above to match your project, and keep them in sync with `docs/README.md` and `docs/index.md`. -->

## Documentation build

The site is built with [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme, configured in `mkdocs.yml`. Beyond rendering Markdown to HTML, the build applies a few transforms contributors should be aware of:

- **Last-modified dates** – each page footer shows the last commit date from git, taken via `mkdocs-git-revision-date-localized-plugin`.
- **Folder metadata** – Material's `meta` plugin applies `.meta.yml` values to pages in that folder and its subfolders. The example project and knowledge base each define a shared tag. Page-specific tags are merged with folder tags.
- **Tag index** – the `tags` plugin collects page and folder tags into `tags.json` and renders the listing marker in the [Tags page](../tags.md). See the [style guide](style-guide.md#tags) for authoring syntax.
- **`llms-full.txt`** – the `mkdocs-llmstxt` plugin concatenates select pages into `llms-full.txt` at the site root, so LLMs and agents can ingest the workspace in one file. The plugin's `sections` key in `mkdocs.yml` mirrors `nav`; keep both in sync when adding or removing sections.
- **Abbreviation tooltips** – `contributing/abbreviations.md` is auto-appended to every page by `pymdownx.snippets`, so any abbreviation registered there is available as a hover tooltip across the site.
- **Strict validation** – `mkdocs build --strict` (`just build-docs`) fails on pages missing from `nav`, broken anchors, unrecognized links, and root-relative links. Use file patterns in the top-level `not_in_nav` setting in `mkdocs.yml` for published pages intentionally omitted from navigation. Snippet sources are excluded from page generation with `exclude_docs`.

The Markdown-facing syntax for these features is documented in the [style guide](style-guide.md); `mkdocs.yml` carries inline comments explaining each option.

## Agent skill publishing

The native MkDocs hook in `scripts/publish_skills.py` copies `.agents/skills/` to `site/.well-known/agent-skills/` and generates the discovery index and AI catalog after each build. Skill metadata provides descriptions and versions; MkDocs configuration provides publisher details. The Pages upload includes hidden files so the catalogs reach the deployed site. See [Agent skills](../agent-skills.md) for authoring and installation instructions.

## Continuous integration

[`.github/workflows/ci.yml`](https://github.com/thibaudcolas/research-workspace-template/blob/main/.github/workflows/ci.yml) runs on every push to `main` and on pull requests:

- Python linting and formatting checks (`ruff`), type checking (`mypy`, `ty`).
- Non-Python formatting checks (`prettier`).
- Link checking ([lychee](https://lychee.cli.rs), configured in `lychee.toml`).
- A strict documentation build, then upload and deployment of the built `site/` to GitHub Pages.
