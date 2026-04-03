#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tools.json"
CONTENT = ROOT / "content"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "item"


def escape_toml(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def frontmatter(tool: dict) -> str:
    category = escape_toml(tool["category"])
    return "\n".join(
        [
            "+++",
            f'title = "{escape_toml(tool["name"])}"',
            f'description = "{escape_toml(tool["description"])}"',
            f'pricing = "{escape_toml(tool["pricing"])}"',
            f'external_url = "{tool["url"]}"',
            f'domain = "{escape_toml(tool["domain"])}"',
            f'categories = ["{category}"]',
            "type = \"tools\"",
            "+++",
            "",
            tool["description"],
            "",
        ]
    )


def main() -> None:
    payload = json.loads(DATA.read_text())
    tools = payload["tools"]

    if CONTENT.exists():
        shutil.rmtree(CONTENT)
    (CONTENT / "tools").mkdir(parents=True, exist_ok=True)
    (CONTENT / "categories").mkdir(parents=True, exist_ok=True)

    (CONTENT / "_index.md").write_text(
        "\n".join(
            [
                "+++",
                'title = "Hugo × TAAFT"',
                'description = "Hugo static AI tools directory built from the local TAAFT dataset."',
                "+++",
                "",
                "500 AI tools rendered by Hugo into static HTML.",
                "",
            ]
        )
    )
    (CONTENT / "categories" / "_index.md").write_text(
        "\n".join(
            [
                "+++",
                'title = "Categories"',
                "+++",
                "",
                "Category landing pages generated from Hugo taxonomies.",
                "",
            ]
        )
    )

    for tool in tools:
        slug = f"{slugify(tool['name'])}-{tool['id']}"
        (CONTENT / "tools" / f"{slug}.md").write_text(frontmatter(tool))


if __name__ == "__main__":
    main()
