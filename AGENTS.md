# Agent guidelines

> For the human-readable contributor guide, see [docs/contributing/README.md](docs/contributing/README.md). This file is a concise quick-reference for the AI assistant.

## Project structure & module organization

Contributor and user docs are in `docs/`. Make sure `mkdocs.yml` (`nav` and `llmstxt` sections) reference relevant files.

## Development commands

See [docs/contributing/README.md#commands](docs/contributing/README.md#commands) for the full list. Key recipes:

- `just init` – install dependencies
- `just lint` – lint + type-check
- `just format` – auto-format
- `just check-links` – check links in Markdown files
- `just build-docs` – build the documentation (strict)

## Project tools

- `uv` for dependency management
- `ruff` for linting and formatting
- `mypy` for type checking
- `ty` for additional type checking (experimental)
- `prettier` for formatting non-Python files
- `prek` for git hooks
- `lychee` for link checking
- `GitHub Actions` for continuous integration and Pages deployment

## Coding style & naming conventions

See [docs/contributing/README.md#coding-style--conventions](docs/contributing/README.md#coding-style--conventions) for the full guide. Quick points:

- Python uses 4-space indentation, [PEP 8](https://peps.python.org/pep-0008/) style, enforced with `ruff`.
- Type annotations required on production code (checked by mypy, ty). Test code is exempt.
- Formatting: `ruff format` for Python, `prettier` for all other files.
- Feel free to ignore maximum line length rules for comments. Instead, hard-wrap at punctuation (or rephrase to be more concise).
- For prose documentation (README, MkDocs pages), follow the [documentation style guide](docs/contributing/style-guide.md): tone, terminology, headings, linking, and American English spelling.

## Commit & pull request guidelines

See [docs/contributing/README.md#pull-request-workflow](docs/contributing/README.md#pull-request-workflow). Quick points:

- Be concise and to the point. Explain rationales that aren't obvious.
- No Title Case usage ever. Always use Sentence case.
- Recent commit messages use short, capitalized, imperative summaries (e.g., "Enforce additional mypy check").
- When the agent commits directly, use `Assisted-by` in a `--trailer`. Example: `git commit -s -m "Add support for X" --trailer "Assisted-by: <agent-name>/<model-id>"`
- PRs should include a clear description, relevant test evidence (command + result), links to any related issues.
