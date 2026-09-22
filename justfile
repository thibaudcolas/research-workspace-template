# Task runner: https://github.com/casey/just
# Requires: `uv`, `npm`, and `just`.

# List all the justfile recipes.
help:
    just --list --list-prefix 'just '

# Install dependencies and initialize for development.
init:
    uv venv
    uv sync --dev
    prek

# Lint the project.
lint:
    uv run ruff check
    uv run ruff format --check
    if git ls-files '*.py' | grep -q .; then uv run mypy .; fi
    uv run ty check
    npm run lint

# Format project files.
format *paths=".":
    uv run ruff check --fix {{ paths }}
    uv run ruff format {{ paths }}
    npm run format -- {{ paths }}

# Check links in all Markdown files (requires lychee).
check-links:
    lychee --no-progress --hidden .

# Build the documentation.
build-docs:
    NO_MKDOCS_2_WARNING=1 uv run mkdocs build --strict

# Build the documentation and serve it locally.
docs:
    NO_MKDOCS_2_WARNING=1 uv run mkdocs serve --strict
