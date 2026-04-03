#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "tools.json"
DOCS = ROOT / "docs"
SITE_URL = "https://taaft-mkdocs-static.onrender.com"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "item"


def sanitize_description(description: str, name: str) -> str:
    if not description:
        return f"{name} is included in this AI tools directory."

    return (
        description.replace(" is listed in the local TAAFT dataset.", " is included in this AI tools directory.")
        .replace(" is an AI tool discovered from the local TAAFT scrape.", " is featured in this AI tools directory.")
    )


def card(tool: dict) -> str:
    return card_with_prefix(tool, "")


def card_with_prefix(tool: dict, prefix: str) -> str:
    slug = f"{slugify(tool['name'])}-{tool['id']}"
    category_slug = slugify(tool["category"])
    return f"""
<article class="tool-card">
  <div class="tool-top">
    <a class="tool-category" href="{prefix}categories/{category_slug}/">{tool["category"]}</a>
    <span class="tool-pricing">{tool["pricing"]}</span>
  </div>
  <h3><a href="{prefix}tools/{slug}/">{tool["name"]}</a></h3>
  <p>{sanitize_description(tool["description"], tool["name"])}</p>
  <div class="tool-footer">
    <span>{tool["domain"] or "Unknown domain"}</span>
    <a class="tool-link" href="{prefix}tools/{slug}/">View details</a>
  </div>
</article>
""".strip()


def main() -> None:
    payload = json.loads(DATA.read_text())
    tools = payload["tools"]
    if DOCS.exists():
        shutil.rmtree(DOCS)
    (DOCS / "categories").mkdir(parents=True, exist_ok=True)
    (DOCS / "tools").mkdir(parents=True, exist_ok=True)
    (DOCS / "styles").mkdir(parents=True, exist_ok=True)

    categories: dict[str, list[dict]] = {}
    for tool in tools:
        categories.setdefault(tool["category"], []).append(tool)

    category_links = "\n".join(
        f'<a class="pill" href="categories/{slugify(name)}/">{name}</a>' for name in sorted(categories)
    )
    all_cards = "\n".join(card(tool) for tool in tools)

    (DOCS / "index.md").write_text(
        f"""# MkDocs for a static _AI tools directory_

This site is built natively by MkDocs and published as plain static HTML. It includes 500 tools, category pages, and dedicated tool pages.

<div class="category-pills">
{category_links}
</div>

## All tools

<div class="tool-grid">
{all_cards}
</div>
"""
    )

    (DOCS / "styles" / "extra.css").write_text(
        """:root {
  --background: #f5f0e8;
  --foreground: #1f2430;
  --muted: #6d727f;
  --surface: rgba(255, 255, 255, 0.78);
  --border: rgba(31, 36, 48, 0.1);
  --accent: #d1693f;
  --accent-2: #2f6b56;
}
body { background: linear-gradient(180deg, #f6f1e8 0%, #efe7da 100%); }
.md-main__inner { max-width: 1200px; }
.tool-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
.tool-card { display: flex; flex-direction: column; gap: 14px; min-height: 220px; padding: 20px; border-radius: 22px; background: rgba(255,255,255,0.88); border: 1px solid var(--border); }
.tool-top, .tool-footer { display: flex; justify-content: space-between; gap: 12px; align-items: center; }
.tool-category, .tool-pricing, .pill { display: inline-flex; align-items: center; border-radius: 999px; padding: 7px 12px; font-size: 12px; font-weight: 600; text-decoration: none; }
.tool-category, .pill { background: rgba(209, 105, 63, 0.12); color: #9b4f30; }
.tool-pricing { background: rgba(47, 107, 86, 0.12); color: var(--accent-2); }
.tool-card h3 { margin: 0; }
.tool-card p { flex: 1; margin: 0; }
.tool-footer { font-size: 12px; color: var(--muted); }
.tool-link { min-height: 40px; padding: 0 14px; border-radius: 14px; display: inline-flex; align-items: center; justify-content: center; background: var(--foreground); color: #fff !important; text-decoration: none; font-weight: 600; }
.category-pills { display: flex; flex-wrap: wrap; gap: 10px; margin: 18px 0 24px; }
@media (max-width: 980px) { .tool-grid { grid-template-columns: 1fr; } }
"""
    )

    sitemap_entries = [SITE_URL]

    for category, items in categories.items():
        slug = slugify(category)
        sitemap_entries.append(f"{SITE_URL}/categories/{slug}/")
        cards = "\n".join(card_with_prefix(tool, "../") for tool in items)
        (DOCS / "categories" / f"{slug}.md").write_text(
            f"""# {category} _AI tools_

[Home](../)

{len(items)} tools in this category, all rendered into static HTML by MkDocs.

<div class="tool-grid">
{cards}
</div>
"""
        )

    for tool in tools:
        tool_slug = f"{slugify(tool['name'])}-{tool['id']}"
        category_slug = slugify(tool["category"])
        sitemap_entries.append(f"{SITE_URL}/tools/{tool_slug}/")
        (DOCS / "tools" / f"{tool_slug}.md").write_text(
            f"""# {tool['name']}

[Home](../) / [{tool['category']}](../categories/{category_slug}/)

{sanitize_description(tool['description'], tool['name'])}

## Details

- Category: [{tool['category']}](../categories/{category_slug}/)
- Pricing: {tool['pricing']}
- Domain: {tool['domain'] or 'Unknown domain'}

[Visit tool]({tool['url']})
"""
        )

    (DOCS / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    )
    (DOCS / "sitemap.xml").write_text(
        "\n".join(
            [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
                *[f"  <url><loc>{entry}</loc></url>" for entry in sitemap_entries],
                "</urlset>",
                "",
            ]
        )
    )


if __name__ == "__main__":
    main()
