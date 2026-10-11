# Task runner: https://github.com/casey/just
# Requires: `uv`, `npm`, and `just`.

# List all the justfile recipes.
help:
    just --list --list-prefix 'just '

# Install dependencies and initialize for development.
init:
    uv venv
    uv sync --locked --dev
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

# Run all checks required before publishing.
check: lint check-links test build-docs

# Format project files, or only the supplied files and directories.
[positional-arguments]
format *paths=".":
    #!/usr/bin/env bash
    set -euo pipefail
    python_paths=()
    for path in "$@"; do
        if [[ -d "$path" || "$path" == *.py || "$path" == *.pyi ]]; then
            python_paths+=("$path")
        fi
    done
    if (( ${#python_paths[@]} )); then
        uv run ruff check --fix -- "${python_paths[@]}"
        uv run ruff format -- "${python_paths[@]}"
    fi
    npx --no-install prettier --write --ignore-unknown -- "$@"

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
