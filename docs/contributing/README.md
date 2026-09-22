# Contribution guidelines

Thank you for considering to help this project.

## Project architecture

See [Project architecture](architecture.md) for how the workspace and its tooling are organized.

## Development

### Installation

> Requirements: [`uv`](https://github.com/astral-sh/uv), [just](https://github.com/casey/just), [prek](https://prek.j178.dev/), [lychee](https://lychee.cli.rs/)

Clone the repository, configure the git hooks, then initialize with `just init`.

```sh
git clone git@github.com:thibaudcolas/research-workspace-template.git
cd REPO/
# Install everything.
just init
```

### Commands

- `just help`: See what commands are available.
- `just init`: Install dependencies and initialize for development.
- `just lint`: Lint the project.
- `just format *paths="."`: Format project files.
- `just check-links`: Check links in all Markdown files.
- `just build-docs`: Build the documentation.
- `just docs`: Build the documentation and serve it locally.

## Coding style & conventions

We follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style, enforced automatically by `ruff`:

- **Python**: formatted with `ruff format`, linted with `ruff check`. Configuration in `pyproject.toml`.
- **Other files**: formatted with `prettier` (see `prettier.config.js`).
- **Indentation**: 4 spaces, no tabs.
- **Type annotations**: required on all production code, checked by `mypy` with strict settings and by `ty` (experimental).
- **Naming**: `snake_case` for functions, methods, and variables; `PascalCase` for classes; `UPPER_CASE` for constants. Test modules follow `test_*.py`, test functions `test_*`, test classes `Test*`.
- **Imports**: organized automatically by `ruff` (isort rules in `pyproject.toml`).
- **Error handling**: use specific exception types; avoid bare `except:` clauses (BLE rules).
- **Comments**: avoid hard-wrapping lines, except at full stops, or other punctuation like commas if must be.

## Documentation

Good documentation helps users and contributors understand the project without reading source code. We aim for docs that are accurate, discoverable, and maintainable.

For prose style, tone, terminology, headings, and linking conventions, follow the [documentation style guide](style-guide.md).

### Prose documentation

- User-facing docs live in `docs/`; the README is the entry point.
- Keep language concise and in **Sentence case** (no Title Case).
- Follow the [documentation style guide](style-guide.md) for tone, terminology, headings, and linking conventions.
- Run `just format` before committing so prettier formats Markdown files consistently.

### MkDocs configuration

The documentation site is built with [MkDocs](https://www.mkdocs.org/) from the Markdown files in `docs/`, configured in `mkdocs.yml`. When you add, rename, or move pages, keep the configuration in sync with the file structure:

- **Landing pages**: each section folder uses a `README.md` as its landing page, so it also renders when browsing the folder on GitHub.
- **Navigation**: the `nav` key should list all pages of the site.
- **llms.txt**: the `llmstxt` plugin's `sections` key lists the pages included in the generated `llms-full.txt`. Add new section landing pages there as well.

`mkdocs.yml` documents each option with an inline comment. The Markdown-facing syntax for features such as code annotations, tabbed blocks, or page tags is documented in the [documentation style guide](style-guide.md); the build-time behavior of each plugin is described in [Project architecture](architecture.md#documentation-build).

Every docs page must be listed in `nav`, or explicitly opted out:

- Working drafts are published like any other page, with a draft-status callout at the top (see the [style guide](style-guide.md#callouts-and-blockquotes)).
- Files that aren't pages (snippet sources like `contributing/abbreviations.md`) are listed in `exclude_docs`.
- Anything else outside `nav` needs `not_in_nav: true` front matter.

Run `just build-docs` to check your changes – it builds with `--strict`, so missing nav entries, unresolved links, and broken anchors fail the build.

## Pull request workflow

1. Create a branch from `main` with a descriptive name.
2. Make your changes, following the coding style and testing guidelines above.
3. Run `just lint` and `just check-links` locally to verify everything passes.
4. Open a pull request with a clear description of what the change does and why. Include relevant test evidence (commands and their output) and links to related issues.
5. CI will run linting (ruff, mypy, ty, prettier), link checking, and a strict documentation build. All checks must pass before merging.
6. Squash merge when approved. Keep the commit message concise, in the imperative mood, and using Sentence case (no Title Case).

## Support guidelines

### Static typing

All project code should pass static type checking by [mypy](https://mypy.readthedocs.io/en/latest/index.html), with as strict of a configuration as possible, and tentatively also pass type checks with the [ty](https://docs.astral.sh/ty/) checker.
