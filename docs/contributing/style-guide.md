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

Add tags in page front matter; pages with the same tag are listed together at `/tags/`:

```md
---
tags:
  - draft
---
```

## Code blocks

Fence code blocks with the language for syntax highlighting. Add a title for context:

````md
```python title="example.py"
print("Hello")
```
````

## Links

Link to other docs pages with relative Markdown links (`[Contributing](../contributing/README.md)`). Never use absolute site URLs — the strict build fails on them.

[Bulleted lists]: https://developers.google.com/tech-writing/one/lists-and-tables
