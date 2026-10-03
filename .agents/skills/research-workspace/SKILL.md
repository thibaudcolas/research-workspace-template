---
name: research-workspace
description: Maintain documentation in a repository based on research-workspace-template. Use when adding research notes, knowledge-base pages, or project documentation to this MkDocs workspace.
license: MIT
metadata:
  version: "1.0.0"
---

# Research workspace

Work from the target repository's `AGENTS.md`, `docs/contributing/README.md`, and `docs/contributing/style-guide.md` for its current structure, commands, and writing conventions.

Place reusable knowledge in `docs/knowledge-base/` and project-specific research in the relevant project folder. Follow the repository's existing sections; `project-a` is a template example. Section landing pages use `README.md` so they work on GitHub as well as the docs site.

When adding, moving, or renaming documentation, update both `nav` and the `llmstxt.sections` mapping in `mkdocs.yml`. Use relative Markdown links between documentation pages. Preserve source citations and distinguish findings from assumptions in research notes.

Run `just build-docs` after changes to catch navigation and link errors. The equivalent command is `uv run mkdocs build --strict`. Follow the repository's formatting and link-checking commands before completing the work.
