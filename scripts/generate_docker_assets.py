#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("/root/src/chrome-gpt-backend/big_websites_massive/website/sites/jamstack-top15-ai-tools")
SITES_DIR = ROOT / "sites"

BASE_IMAGES = {
    "nextjs": "node:20-alpine",
    "docusaurus": "node:20-alpine",
    "nuxt": "node:20-alpine",
    "gatsby": "node:20-alpine",
    "astro": "node:20-alpine",
    "hexo": "node:20-alpine",
    "vuepress": "node:20-alpine",
    "eleventy": "node:20-alpine",
    "vitepress": "node:20-alpine",
    "mkdocs": "python:3.11-slim",
    "pelican": "python:3.11-slim",
    "sphinx": "python:3.11-slim",
    "hugo": "golang:1.21-alpine",
    "zola": "rust:1.94-slim",
    "mdbook": "rust:1.94-slim",
}


def dockerfile_for(metadata: dict) -> str:
    slug = metadata["slug"]
    image = BASE_IMAGES[slug]
    return f"""# Reproducible container wrapper for the {metadata['name']} static variant.
# The current batch commits built static output in dist/ so this Dockerfile can
# validate and serve the exact artifact deterministically. A later native
# framework implementation can replace the validation step with the framework's
# build command while keeping the same container entrypoint pattern.

FROM {image} AS validate
WORKDIR /workspace
COPY dist/ ./dist/
RUN test -f dist/index.html
RUN test -f dist/styles.css

FROM nginx:1.27-alpine
COPY --from=validate /workspace/dist/ /usr/share/nginx/html/
EXPOSE 80
"""


def playbook_entry(metadata: dict) -> str:
    slug = metadata["slug"]
    image = BASE_IMAGES[slug]
    return f"""## {metadata['name']}

- Source folder: `sites/{slug}`
- Static output: `sites/{slug}/dist`
- Docker base image: `{image}`
- Dockerfile: `sites/{slug}/Dockerfile`
- Current reproducible build command:

```bash
docker build -t {slug}-taaft -f sites/{slug}/Dockerfile sites/{slug}
docker run --rm -p 18{metadata['slug'].__len__():02d}:80 {slug}-taaft
```

- Generator note: {metadata['notes']}
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.
"""


def write_playbook(metadata_list: list[dict]) -> None:
    sections = "\n\n".join(playbook_entry(metadata) for metadata in metadata_list)
    content = f"""# Reproducible Framework Build Playbook

This document captures the current reproducible container workflow for the 15 Jamstack-inspired AI-tools site variants in this batch.

Principles:

- all variants are stored in one monorepo
- each framework variant has its own `dist/` output directory
- each framework variant has its own `Dockerfile`
- container builds are deterministic because they validate committed static artifacts before serving them
- Render can point each service at the corresponding `dist/` folder via the monorepo Blueprint

Current scope:

- one committed static output per framework variant
- one Dockerfile per framework variant
- one shared tool selection sourced from the local TAAFT dataset

Future native-framework step:

- replace each Dockerfile's validation stage with the framework's real build command
- keep the same final static serving stage or publish the generated output directly in Render

{sections}
"""
    (ROOT / "FRAMEWORK_DOCKER_PLAYBOOK.md").write_text(content)


def write_build_script(metadata_list: list[dict]) -> None:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        'ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"',
        'cd "$ROOT_DIR"',
        "",
    ]
    for metadata in metadata_list:
        slug = metadata["slug"]
        lines.append(f'echo "Building {slug}..."')
        lines.append(f'docker build -t {slug}-taaft -f "sites/{slug}/Dockerfile" "sites/{slug}"')
        lines.append("")
    (ROOT / "build_all_docker.sh").write_text("\n".join(lines) + "\n")


def main() -> None:
    metadata_list = []
    for metadata_path in sorted(SITES_DIR.glob("*/metadata.json")):
        metadata = json.loads(metadata_path.read_text())
        metadata_list.append(metadata)
        site_dir = metadata_path.parent
        (site_dir / "Dockerfile").write_text(dockerfile_for(metadata))

    write_playbook(metadata_list)
    write_build_script(metadata_list)
    print(f"Wrote Dockerfiles for {len(metadata_list)} framework variants")


if __name__ == "__main__":
    main()
