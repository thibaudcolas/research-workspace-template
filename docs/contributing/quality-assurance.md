# Quality assurance

What belongs in each content layer, and the checks content must pass before publishing.

## Content review

- Factual claims link to a source.
- Pages follow the [documentation style guide](style-guide.md).
- `just lint`, `just check-links`, `just build-docs`, and `just test` pass.

<!-- Adapt this page to your project's review process. The source workspace uses it to define what goes in each layer (knowledge base vs. project docs) and how drafts graduate to published pages. -->

## Checks

- **Strict build** (`just build-docs`): fails on missing nav entries, broken anchors, unresolved links, and missing snippets.
- **Local links** (`just check-links`): checks local file targets without network access. MkDocs checks documentation anchors as part of the strict build.
- **External links** (`just check-external-links`): checks HTTP(S) sources. CI runs this separately on pull requests, pushes to `main`, and every Monday, with a report in the workflow's job summary. It can also be run manually from GitHub Actions.
- **Formatting** (`just lint`): ruff, prettier, mypy, ty.
- **Prose** (`just lint-prose`, also part of `just lint`): Vale checks a small set of terminology and American English spelling rules.
- **Rendering and publishing** (`just test`): temporary builds exercise supported Markdown syntax and generated exports, alongside the skill publishing tests. Fixtures are not published on the documentation site.

### External link failures

External availability does not gate the documentation deployment. Investigate failed checks: replace broken links with maintained sources or archived copies where appropriate. A rate-limited response (HTTP 429) is unverified, not a successful check; rerun it later. Add exclusions in `lychee.toml` only for known automation blockers, with an explanation. Do not suppress a status code globally to make a report pass.

### Prose rules

Vale uses `.vale.ini` and the small `Workspace` style in `.vale/styles/`. It checks contributor and agent guidance as well as `docs/`. Rules enforce names such as MkDocs and GitHub, and common American spellings such as “color” and “organization.” This is a targeted word list, not a comprehensive spelling or grammar checker. Extend it when a recurring mistake warrants a rule.

Code examples are excluded by Vale's Markdown parser. Preserve wording in quotations and source titles; when a rule would change quoted evidence, surround only that passage with `<!-- vale off -->` and `<!-- vale on -->`. Explain the exception in a nearby comment. Avoid disabling checks for an entire page.

### Rendered output

When changing documentation features, also inspect the generated output:

- Open `site/tags/index.html` and follow a tag link to confirm folder and page tags appear in the listing.
- Check `site/search/search_index.json` when changing search settings: excluded pages should be absent and boosted pages should carry the intended value.
- Check `site/llms-full.txt` for new documentation pages, keeping `nav` and `llmstxt.sections` in sync.
- Confirm abbreviation definitions do not appear as stray text, and that abbreviations in prose render with their expansions.

For layout changes, inspect the narrow-screen view and keyboard navigation with `just docs`. Check that links remain descriptive and content stays readable in both color schemes.
