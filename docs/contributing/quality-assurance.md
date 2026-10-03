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

When changing documentation features, also inspect the generated output:

- Open `site/tags/index.html` and follow a tag link to confirm folder and page tags appear in the listing.
- Check `site/search/search_index.json` when changing search settings: excluded pages should be absent and boosted pages should carry the intended value.
- Check `site/llms-full.txt` for new documentation pages, keeping `nav` and `llmstxt.sections` in sync.
- Confirm abbreviation definitions do not appear as stray text, and that abbreviations in prose render with their expansions.

For layout changes, inspect the narrow-screen view and keyboard navigation with `just docs`. Check that links remain descriptive and content stays readable in both color schemes.
