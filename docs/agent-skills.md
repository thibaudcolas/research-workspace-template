# Agent skills

This workspace publishes [Agent Skills](https://agentskills.io/) alongside its documentation. The included `research-workspace` skill helps agents maintain the workspace's documentation structure and navigation.

## Use a skill

Skills are maintained in the repository's `.agents/skills/` directory. Tools that support that directory can discover them locally. To use a skill in another repository, copy its complete folder into that repository's `.agents/skills/` directory.

The documentation build also publishes these paths, relative to the site's base URL:

- `.well-known/agent-skills/research-workspace/SKILL.md`: the starter skill as raw Markdown.
- `.well-known/agent-skills/index.json`: skill descriptions, download URLs, and SHA-256 digests, following the [agent skills discovery proposal](https://github.com/cloudflare/agent-skills-discovery-rfc).
- `.well-known/ai-catalog.json`: publisher information, skill versions, and absolute download URLs, following [AI Catalog](https://ai-catalog.io/).

For a GitHub Pages project site, keep the repository path before `.well-known/`. Discovery requires a client that supports the relevant catalog format; publishing a catalog does not automatically install skills.

## Publish a skill

Create `.agents/skills/<name>/SKILL.md` with YAML front matter:

```yaml
---
name: my-skill
description: Describe the task this skill supports and when an agent should use it.
metadata:
  version: "1.0.0"
---
```

Use lowercase letters, digits, and single hyphens for the name, matching the directory name. Add the instructions below the front matter. Keep supporting references, scripts, and assets inside the skill folder: the build copies the whole folder. Symlinks are rejected. Every skill in this directory is published, so keep local-only material elsewhere.

Update `metadata.version` when releasing changes to the skill. Catalog versions come from skill metadata, independently of the workspace version. The catalog omits optional modification dates rather than reporting checkout time as a content update.

Run `just build-docs` and inspect `site/.well-known/`. Invalid metadata fails the build. The publishing hook in `scripts/publish_skills.py` generates catalogs from the skills and the `site_name` and `site_url` settings in `mkdocs.yml`. Update those settings when adopting this template. An empty skills directory produces empty catalogs.

GitHub Actions includes hidden files in its Pages artifact so `.well-known/` is deployed with the documentation. Publishing uses the existing deployment on pushes to `main`; no separate release or package upload is needed.
