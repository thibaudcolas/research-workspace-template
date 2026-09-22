# Quality assurance

What belongs in each content layer, and the checks content must pass before publishing.

## Content review

- Factual claims link to a source.
- Pages follow the [documentation style guide](style-guide.md).
- `just lint` and `just build-docs` pass.

<!-- Adapt this page to your project's review process. The source workspace uses it to define what goes in each layer (knowledge base vs. project docs) and how drafts graduate to published pages. -->

## Checks

- **Strict build** (`just build-docs`): fails on missing nav entries, broken anchors, and unresolved links.
- **Link check** (`just check-links`): validates external links in all Markdown files.
- **Formatting** (`just lint`): ruff, prettier, mypy, ty.
