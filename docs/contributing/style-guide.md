# Documentation style guide

How to write docs pages and posts for this workspace: tone, headings, callouts, tags, and media.

## General guidelines

- Write concise, direct, factual content in **Sentence case** (no Title Case for headings or titles).
- Use American English spelling.
- Prefer linking to other pages over repeating content.
- Use [Bulleted lists] when describing more than two comparable things or steps.
- One thing per paragraph; don't be afraid of whitespace.

<!-- TODO: Copy or adapt the full style guide from the source workspace (https://github.com/marketing-django/marketing-workspace/blob/main/docs/contributing/style-guide.md), or write one for your project. This placeholder documents the minimum conventions the templates rely on. -->

## Callouts and blockquotes

Use Material's admonitions for callouts, with `{ .info }`-style classes where needed:

```md
!!! note "Optional title"

    Content of the callout.
```

Collapsible callouts use `???` instead of `!!!`.

## Tags

Use short, consistent topic tags to connect related pages in the [tag index](../tags.md). Add page-specific tags in front matter:

```md
---
tags:
  - interviews
---
```

For tags shared by a section, create a `.meta.yml` file in that folder:

```yaml title="docs/project-a/.meta.yml"
tags:
  - project-a
```

The `meta` plugin applies these values to the folder and its subfolders. Page tags and folder tags are merged and deduplicated. Rename the example project tag when adopting this template. Use a visible callout to explain draft status; tags alone do not describe what remains unfinished.

## Search controls

Use search ranking sparingly. A maintained overview can have a small boost so readers find it before detailed notes:

```yaml
---
search:
  boost: 2
---
```

Use `boost: 0.5` to reduce an archived page's prominence while keeping it searchable. To exclude a page from search entirely, use:

```yaml
---
search:
  exclude: true
---
```

These settings can also go in `.meta.yml` to apply to an entire folder. Search exclusion does not unpublish a page or restrict access to it. Keep useful source notes searchable unless there is a concrete reason to exclude them. See [Material's search controls](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/#search-boosting).

## Tables

Use tables for comparisons with consistent fields. Keep column headings descriptive and cells short; use prose for complex explanations. Standard Markdown tables are already enabled by MkDocs:

```md
| Method     | Useful for            | Limitation        |
| ---------- | --------------------- | ----------------- |
| Interviews | Exploring motivations | Small samples     |
| Surveys    | Comparing responses   | Limited follow-up |
```

## Footnotes

Use footnotes for supporting detail that would interrupt the main argument. Prefer an inline source link when it makes a claim easier to verify. Give each note a descriptive identifier:

```md
The sample covers two project teams.[^sample]

[^sample]: Recruitment was limited to teams participating in the pilot.
```

## Landing-page grids

Use a card grid when a landing page needs short descriptions of several equally important destinations. Prefer an ordinary list for a few simple links. The required `attr_list` and `md_in_html` extensions are already enabled.

This example is relative to `docs/index.md`:

<!-- prettier-ignore -->
```md
<div class="grid cards" markdown>

- **Knowledge base**

    Background research and reusable reference material.

    [Browse the knowledge base](knowledge-base/README.md)

- **Project A**

    Research and working documents for the example project.

    [Read Project A documentation](project-a/README.md)

</div>
```

Keep links descriptive, retain a logical reading order, and use text rather than icons alone to identify destinations. See [Material's grid reference](https://squidfunk.github.io/mkdocs-material/reference/grids/).

## Abbreviations

Shared definitions live in `contributing/abbreviations.md` and use Python-Markdown's `*[NAME]: Expansion` syntax. For example, PSF and WG have definitions in the template. Define unfamiliar terms in the prose on first use as well.

The definitions file is excluded from page generation and from Prettier, which otherwise rewrites the abbreviation markers. Keep the leading asterisk when editing it.

## Code blocks

Fence code blocks with the language for syntax highlighting. Add a title for context:

````md
```python title="example.py"
print("Hello")
```
````

## Links

Link to other docs pages with relative Markdown links (`[Contributing](../contributing/README.md)`). Avoid root-relative paths such as `/contributing/`: the strict build rejects them, and they omit the repository path on GitHub Pages. Use full URLs for external sources.

[Bulleted lists]: https://developers.google.com/tech-writing/one/lists-and-tables
