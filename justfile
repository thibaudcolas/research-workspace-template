# Task runner: https://github.com/casey/just
# Requires: `uv`, `npm`, and `just`.

# List all the justfile recipes.
help:
    just --list --list-prefix 'just '

# Install dependencies and initialize for development.
init:
    uv venv
    uv sync --dev
    npm ci
    uv run vale --version
    prek

# Lint the project.
lint:
    uv run ruff check
    uv run ruff format --check
    if git ls-files '*.py' | grep -q .; then uv run mypy .; fi
    uv run ty check
    npm run lint
    just lint-prose

# Check the small, project-owned prose style (Vale is installed by uv).
lint-prose:
    uv run vale README.md CONTRIBUTING.md AGENTS.md docs .agents/skills

# Format project files.
format *paths=".":
    uv run ruff check --fix {{ paths }}
    uv run ruff format {{ paths }}
    npm run format -- {{ paths }}

# Check local links without network access (requires lychee).
check-links:
    lychee --offline --no-progress --hidden .

# Check external sources separately so availability does not block the docs build.
check-external-links:
    lychee --scheme http --scheme https --no-progress --hidden .

# Build the documentation.
build-docs:
    NO_MKDOCS_2_WARNING=1 uv run mkdocs build --strict

# Test skill publishing and documentation rendering in temporary builds.
test:
    uv run python -m unittest discover -s tests

# Build the documentation and serve it locally.
docs:
    NO_MKDOCS_2_WARNING=1 uv run mkdocs serve --strict
