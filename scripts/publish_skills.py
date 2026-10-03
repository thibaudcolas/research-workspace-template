"""Publish repository skills and discovery catalogs during the MkDocs build."""

import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit

import yaml
from mkdocs.exceptions import PluginError


def _metadata(path: Path) -> dict[str, Any]:
    """Read and validate the metadata needed by the discovery catalogs."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise PluginError(f"{path}: expected YAML front matter")
    try:
        data = yaml.safe_load("\n".join(lines[1 : lines.index("---", 1)]))
    except yaml.YAMLError as error:
        raise PluginError(f"{path}: invalid YAML front matter") from error
    if not isinstance(data, dict):
        raise PluginError(f"{path}: front matter must be a mapping")
    name = data.get("name")
    if (
        not isinstance(name, str)
        or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
        or len(name) > 64
        or name != path.parent.name
    ):
        raise PluginError(f"{path}: name must match its lowercase skill directory")
    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        raise PluginError(f"{path}: description must be a nonempty string")
    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        raise PluginError(f"{path}: metadata must be a mapping")
    version = metadata.get("version")
    if not isinstance(version, str) or not version.strip():
        raise PluginError(f"{path}: metadata.version must be a nonempty string")
    return data


def on_post_build(config: Any, **kwargs: Any) -> None:
    """Copy complete skill folders and generate catalogs under the site URL."""
    root = Path(config["config_file_path"]).resolve().parent
    source = root / ".agents" / "skills"
    site = Path(config["site_dir"])
    site_url = str(config["site_url"] or "").rstrip("/")
    parsed = urlsplit(site_url)
    if parsed.scheme not in {"https", "http"} or not parsed.netloc:
        raise PluginError("Skill publishing requires an absolute http(s) site_url")
    if parsed.query or parsed.fragment:
        raise PluginError(
            "Skill publishing requires site_url without query or fragment"
        )

    # Validate before touching output, including resources that would escape the folder.
    skills = []
    for path in sorted(source.glob("*/SKILL.md")):
        if path.parent.is_symlink() or any(
            entry.is_symlink() for entry in path.parent.rglob("*")
        ):
            raise PluginError(
                f"{path.parent}: published skills cannot contain symlinks"
            )
        skills.append((path, _metadata(path)))

    # Remove stale skills during dirty builds and local development, too.
    output = site / ".well-known" / "agent-skills"
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    authority = ":".join(
        quote(part, safe="")
        for part in [parsed.netloc, *parsed.path.strip("/").split("/")]
        if part
    )
    host = {
        "displayName": config["site_name"],
        "identifier": f"did:web:{authority}",
        "documentationUrl": f"{site_url}/",
    }
    index_entries = []
    catalog_entries = []
    for path, data in skills:
        name = data["name"]
        shutil.copytree(
            path.parent,
            output / name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
        index_entries.append(
            {
                "name": name,
                "type": "skill-md",
                "description": data["description"],
                # Relative to the index, preserving GitHub Pages project subpaths.
                "url": f"{name}/SKILL.md",
                "digest": f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}",
            }
        )
        catalog_entries.append(
            {
                "identifier": f"urn:air:{authority}:skill:{name}",
                "displayName": name,
                "type": "application/agent-skills+md",
                "url": f"{site_url}/.well-known/agent-skills/{name}/SKILL.md",
                "description": data["description"],
                "version": data["metadata"]["version"],
                "publisher": host,
            }
        )
    catalogs = {
        output / "index.json": {
            "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
            "skills": index_entries,
        },
        site / ".well-known" / "ai-catalog.json": {
            "specVersion": "1.0",
            "host": host,
            "entries": catalog_entries,
        },
    }
    for destination, catalog in catalogs.items():
        destination.write_text(
            json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
