#!/usr/bin/env python3

from __future__ import annotations

import html
import json
import random
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path("/root/src/chrome-gpt-backend/big_websites_massive/website/sites/jamstack-top15-ai-tools")
SITES_DIR = ROOT / "sites"
PRIMARY = Path("/root/data/scraperli/taaft.results.jsonl")
SECONDARY = Path("/root/data/scraperli/alphabetical_results.jsonlines")
MAX_TOOLS = 500
RANDOM_SEED = 42

GENERATORS = [
    {
        "slug": "nextjs",
        "name": "Next.js",
        "stars": 133884,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "React-based static export build",
        "notes": "Typical static build: next build with output export or next export depending on app structure.",
        "render_name": "taaft-nextjs",
    },
    {
        "slug": "hugo",
        "name": "Hugo",
        "stars": 82968,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Go-powered static site generator",
        "notes": "Typical static build: hugo --minify producing public/.",
        "render_name": "taaft-hugo",
    },
    {
        "slug": "docusaurus",
        "name": "Docusaurus",
        "stars": 61371,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Docs-oriented React static site",
        "notes": "Typical static build: docusaurus build producing build/.",
        "render_name": "taaft-docusaurus",
    },
    {
        "slug": "nuxt",
        "name": "Nuxt",
        "stars": 57969,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Vue-based static generation",
        "notes": "Typical static build: nuxi generate producing .output/public/.",
        "render_name": "taaft-nuxt",
    },
    {
        "slug": "gatsby",
        "name": "Gatsby",
        "stars": 55916,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "React static data site",
        "notes": "Typical static build: gatsby build producing public/.",
        "render_name": "taaft-gatsby",
    },
    {
        "slug": "astro",
        "name": "Astro",
        "stars": 52942,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Content-heavy site generator with low JS output",
        "notes": "Typical static build: astro build producing dist/.",
        "render_name": "taaft-astro",
    },
    {
        "slug": "hexo",
        "name": "Hexo",
        "stars": 40669,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Node-based fast blog and content generator",
        "notes": "Typical static build: hexo generate producing public/.",
        "render_name": "taaft-hexo",
    },
    {
        "slug": "vuepress",
        "name": "VuePress",
        "stars": 22796,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Vue-powered documentation-style static site",
        "notes": "Typical static build: vuepress build docs producing docs/.vuepress/dist/.",
        "render_name": "taaft-vuepress",
    },
    {
        "slug": "mkdocs",
        "name": "MkDocs",
        "stars": 20907,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Markdown-driven Python docs generator",
        "notes": "Typical static build: mkdocs build producing site/.",
        "render_name": "taaft-mkdocs",
    },
    {
        "slug": "mdbook",
        "name": "mdBook",
        "stars": 20174,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Rust-based static documentation builder",
        "notes": "Typical static build: mdbook build producing book/.",
        "render_name": "taaft-mdbook",
    },
    {
        "slug": "eleventy",
        "name": "Eleventy",
        "stars": 18662,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Flexible JavaScript static site generator",
        "notes": "Typical static build: eleventy producing _site/.",
        "render_name": "taaft-eleventy",
    },
    {
        "slug": "zola",
        "name": "Zola",
        "stars": 15770,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Single-binary Rust static site generator",
        "notes": "Typical static build: zola build producing public/.",
        "render_name": "taaft-zola",
    },
    {
        "slug": "vitepress",
        "name": "VitePress",
        "stars": 15553,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Vite-based docs-style static site generator",
        "notes": "Typical static build: vitepress build docs producing docs/.vitepress/dist/.",
        "render_name": "taaft-vitepress",
    },
    {
        "slug": "pelican",
        "name": "Pelican",
        "stars": 12985,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Python static publishing workflow",
        "notes": "Typical static build: pelican content -o output -s pelicanconf.py.",
        "render_name": "taaft-pelican",
    },
    {
        "slug": "sphinx",
        "name": "Sphinx",
        "stars": 7305,
        "source_url": "https://jamstack.org/generators/",
        "tagline": "Python documentation build system adapted for static publishing",
        "notes": "Typical static build: sphinx-build -b html source build.",
        "render_name": "taaft-sphinx",
    },
]

FALLBACK_CATEGORIES = [
    "Writing",
    "Research",
    "Coding",
    "Marketing",
    "Image",
    "Video",
    "Voice",
    "Productivity",
    "Education",
    "Analytics",
    "Automation",
    "Design",
]

CATEGORY_RULES = [
    ("Image", ["image", "photo", "avatar", "visual", "art", "logo", "design", "gif", "animation"]),
    ("Video", ["video", "film", "youtube", "subtitle", "editing"]),
    ("Voice", ["audio", "voice", "speech", "transcription", "podcast", "music"]),
    ("Writing", ["writing", "essay", "copy", "blog", "headline", "email", "caption", "translation", "grammar"]),
    ("Coding", ["coding", "code", "developer", "devops", "programming", "api", "software", "sql"]),
    ("Research", ["research", "analysis", "academic", "papers", "search", "document", "summaries"]),
    ("Marketing", ["marketing", "seo", "ads", "social", "sales", "branding", "reviews"]),
    ("Productivity", ["calendar", "meeting", "assistant", "workflow", "productivity", "scheduling"]),
    ("Automation", ["automation", "agents", "integration", "process", "ops"]),
    ("Business", ["business", "finance", "legal", "contracts", "hr", "consulting", "kpi"]),
    ("Education", ["lesson", "tutor", "learning", "study", "preparation", "coach"]),
    ("Lifestyle", ["health", "fitness", "travel", "food", "career", "fashion", "dating", "wellness"]),
]


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "item"


def category_from_task(task: str) -> str:
    lowered = normalize_text(task).lower()
    if not lowered:
        return ""
    for category, keywords in CATEGORY_RULES:
        if any(keyword in lowered for keyword in keywords):
            return category
    return ""


def external_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def load_primary_records() -> dict[str, dict]:
    records: dict[str, dict] = {}
    if not PRIMARY.exists():
        return records
    with PRIMARY.open() as handle:
        for line in handle:
            row = json.loads(line)
            name = normalize_text(row.get("data_name"))
            description = normalize_text(row.get("description")) or f"{name} is an AI tool discovered from the local TAAFT scrape."
            external_url = normalize_text(row.get("external_url") or row.get("data_url"))
            if not name or not external_url:
                continue
            key = external_url.lower()
            if key in records:
                continue
            records[key] = {
                "name": name,
                "description": description,
                "external_url": external_url,
                "source_page": normalize_text(row.get("data_url")),
            }
    return records


def merge_secondary(records: dict[str, dict]) -> None:
    if not SECONDARY.exists():
        return
    with SECONDARY.open() as handle:
        for line in handle:
            row = json.loads(line)
            external_url = normalize_text(row.get("external_url") or row.get("page_url"))
            if not external_url:
                continue
            key = external_url.lower()
            task = category_from_task(row.get("task", ""))
            item = records.get(key)
            if item is None:
                name = normalize_text(row.get("name"))
                if not name:
                    continue
                item = {
                    "name": name,
                    "description": f"{name} is listed in the local TAAFT dataset.",
                    "external_url": external_url,
                    "source_page": normalize_text(row.get("page_url")),
                }
                records[key] = item
            if task and not item.get("category"):
                item["category"] = task
            if row.get("pricing") and not item.get("pricing"):
                item["pricing"] = normalize_text(row.get("pricing"))


def materialize_tools() -> list[dict]:
    random.seed(RANDOM_SEED)
    records = load_primary_records()
    merge_secondary(records)
    items = list(records.values())
    random.shuffle(items)
    tools: list[dict] = []
    for index, item in enumerate(items[:MAX_TOOLS], start=1):
        category = normalize_text(item.get("category")) or random.choice(FALLBACK_CATEGORIES)
        pricing = normalize_text(item.get("pricing")) or random.choice(["Free", "Freemium", "Paid", "Contact for pricing"])
        description = normalize_text(item.get("description")) or f"{item['name']} is an AI tool in the {category} category."
        tools.append(
            {
                "id": index,
                "name": item["name"],
                "description": description,
                "category": category,
                "pricing": pricing,
                "url": item["external_url"],
                "domain": external_domain(item["external_url"]),
            }
        )
    return tools


def build_cards(tools: list[dict]) -> str:
    cards = []
    for tool in tools:
        cards.append(
            f"""
          <article class="tool-card">
            <div class="tool-top">
              <span class="tool-category">{esc(tool['category'])}</span>
              <span class="tool-pricing">{esc(tool['pricing'])}</span>
            </div>
            <h3>{esc(tool['name'])}</h3>
            <p>{esc(tool['description'])}</p>
            <div class="tool-footer">
              <span>{esc(tool['domain'] or 'Unknown domain')}</span>
              <a href="{esc(tool['url'])}" target="_blank" rel="noreferrer">Visit</a>
            </div>
          </article>""".rstrip()
        )
    return "\n".join(cards)


def build_category_pills(tools: list[dict]) -> str:
    categories = sorted({tool["category"] for tool in tools})
    return "\n".join(f'<span class="pill">{esc(category)}</span>' for category in categories)


def render_index(generator: dict, tools: list[dict]) -> str:
    cards = build_cards(tools)
    pills = build_category_pills(tools)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{esc(generator['name'])} × TAAFT AI Tools</title>
    <meta
      name="description"
      content="{esc(generator['name'])} demo site listing 500 AI tools selected from the local TAAFT dataset."
    />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <div class="brand-block">
          <div class="brand-mark">{esc(generator['name'][0])}</div>
          <div>
            <div class="brand-title">{esc(generator['name'])} × TAAFT</div>
            <div class="brand-subtitle">{esc(generator['tagline'])}</div>
          </div>
        </div>
        <a class="header-link" href="#directory">Browse 500 tools</a>
      </header>

      <main>
        <section class="hero">
          <div class="hero-copy">
            <div class="hero-badge">Top Jamstack generator batch</div>
            <h1>{esc(generator['name'])} for a static <span>AI tools directory</span></h1>
            <p>
              This page is part of a 15-generator batch inspired by the current Jamstack generator rankings.
              It renders 500 tools selected from the local TAAFT scrape dataset and ships as plain static assets.
            </p>
            <div class="hero-meta">
              <div class="meta-card">
                <div class="meta-label">Jamstack stars</div>
                <div class="meta-value">{generator['stars']:,}</div>
              </div>
              <div class="meta-card">
                <div class="meta-label">Tool count</div>
                <div class="meta-value">{len(tools)}</div>
              </div>
              <div class="meta-card accent-card">
                <div class="meta-label">Render deploy</div>
                <div class="meta-value">Static</div>
              </div>
            </div>
          </div>
          <div class="hero-panel">
            <h2>Build notes</h2>
            <p>{esc(generator['notes'])}</p>
            <p>
              Source list: <a href="{esc(generator['source_url'])}" target="_blank" rel="noreferrer">Jamstack generators</a>
            </p>
          </div>
        </section>

        <section class="category-strip">
          <div class="section-head">
            <h2>Categories</h2>
            <p>Shared bucket taxonomy derived from the TAAFT task data.</p>
          </div>
          <div class="pill-row">
{pills}
          </div>
        </section>

        <section class="directory" id="directory">
          <div class="section-head">
            <h2>All 500 tools</h2>
            <p>Static HTML listing for crawlability and lightweight hosting.</p>
          </div>
          <div class="tool-grid">
{cards}
          </div>
        </section>
      </main>
    </div>
  </body>
</html>
"""


def site_readme(generator: dict) -> str:
    return f"""# {generator['name']} variant

This folder contains a prebuilt static AI-tools listing variant for **{generator['name']}**.

- Generator: `{generator['name']}`
- Jamstack source: {generator['source_url']}
- Render service name: `{generator['render_name']}`
- Static output path: `dist/`

Notes:

- {generator['notes']}
- The current batch uses shared TAAFT-derived content and a prebuilt static output so each variant can deploy cleanly to Render from a single monorepo.
"""


def shared_styles() -> str:
    return """:root {
  --background: #f5f0e8;
  --foreground: #1f2430;
  --muted: #6d727f;
  --surface: rgba(255, 255, 255, 0.78);
  --surface-strong: rgba(255, 255, 255, 0.95);
  --border: rgba(31, 36, 48, 0.1);
  --accent: #d1693f;
  --accent-2: #2f6b56;
  --shadow: 0 22px 60px rgba(44, 37, 27, 0.12);
}

* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Inter", sans-serif;
  color: var(--foreground);
  background:
    radial-gradient(circle at top left, rgba(209, 105, 63, 0.18), transparent 28%),
    radial-gradient(circle at top right, rgba(47, 107, 86, 0.18), transparent 26%),
    linear-gradient(180deg, #f6f1e8 0%, #efe7da 100%);
}

a { color: inherit; }

.page-shell {
  width: min(1220px, calc(100% - 32px));
  margin: 0 auto;
  padding: 24px 0 72px;
}

.site-header,
.hero,
.category-strip,
.directory {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 28px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(18px);
}

.site-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  padding: 18px 22px;
  margin-bottom: 20px;
}

.brand-block {
  display: flex;
  gap: 14px;
  align-items: center;
}

.brand-mark {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, var(--accent), #efb08f);
  color: #fff;
  font-weight: 700;
}

.brand-title { font-weight: 700; }
.brand-subtitle, .section-head p, .hero p, .hero-panel p, .tool-card p { color: var(--muted); }
.header-link { text-decoration: none; font-weight: 600; }

.hero {
  display: grid;
  grid-template-columns: 1.4fr 0.8fr;
  gap: 24px;
  padding: 34px;
  margin-bottom: 20px;
}

.hero-badge,
.tool-category,
.tool-pricing,
.pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 7px 12px;
  font-size: 12px;
  font-weight: 600;
}

.hero-badge, .tool-category, .pill {
  background: rgba(209, 105, 63, 0.12);
  color: #9b4f30;
}

.hero h1, .section-head h2 {
  margin: 12px 0;
  font-family: "Instrument Serif", serif;
  font-weight: 400;
  line-height: 0.98;
}

.hero h1 {
  font-size: clamp(2.9rem, 6vw, 5rem);
}

.hero h1 span { font-style: italic; }
.hero p { max-width: 640px; line-height: 1.75; }

.hero-meta {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  margin-top: 24px;
}

.meta-card {
  padding: 18px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid var(--border);
}

.accent-card {
  background: linear-gradient(135deg, rgba(47, 107, 86, 0.9), rgba(33, 53, 63, 0.92));
  color: #fff;
}

.meta-label {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.meta-value {
  margin-top: 8px;
  font-size: 1.8rem;
  font-weight: 700;
}

.hero-panel {
  padding: 24px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--border);
}

.hero-panel h2 {
  margin-top: 0;
  font-size: 1.1rem;
}

.category-strip, .directory {
  padding: 28px;
  margin-top: 20px;
}

.section-head {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: end;
  margin-bottom: 18px;
}

.pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tool-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.tool-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 240px;
  padding: 20px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid var(--border);
}

.tool-top, .tool-footer {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.tool-card h3 {
  margin: 0;
  font-size: 1.15rem;
}

.tool-card p {
  flex: 1;
  margin: 0;
  line-height: 1.7;
}

.tool-pricing {
  background: rgba(47, 107, 86, 0.12);
  color: var(--accent-2);
}

.tool-footer {
  font-size: 12px;
  color: var(--muted);
}

.tool-footer a {
  min-height: 40px;
  padding: 0 14px;
  border-radius: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--foreground);
  color: #fff;
  text-decoration: none;
  font-weight: 600;
}

@media (max-width: 980px) {
  .hero, .tool-grid, .hero-meta {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .page-shell {
    width: min(100% - 20px, 1220px);
  }

  .site-header, .section-head, .tool-top, .tool-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .hero, .category-strip, .directory {
    padding: 22px;
  }
}
"""


def root_readme() -> str:
    generator_lines = "\n".join(
        f"- `{generator['name']}`: `sites/{generator['slug']}/dist/` -> Render service `{generator['render_name']}`"
        for generator in GENERATORS
    )
    return f"""# Jamstack Top 15 AI Tools Batch

This repo batch contains **15 static AI-tools directory variants** based on top Jamstack site generators selected from the current Jamstack generator rankings.

Each variant:

- lists 500 tools selected from the local TAAFT dataset
- ships as a plain static site
- is intended to deploy as an independent Render static site

## Selected generators

{generator_lines}

## Data source

- `/root/data/scraperli/taaft.results.jsonl`
- `/root/data/scraperli/alphabetical_results.jsonlines`

## Generate locally

```bash
cd /root/src/chrome-gpt-backend/big_websites_massive/website/sites/jamstack-top15-ai-tools
python3 scripts/generate_batch_sites.py
python3 -m http.server 8041
```

## Render

This repo includes a `render.yaml` Blueprint spec that defines 15 static sites.
"""


def render_yaml() -> str:
    blocks = []
    for generator in GENERATORS:
        blocks.append(
            f"""  - type: web
    runtime: static
    name: {generator['render_name']}
    autoDeployTrigger: off
    rootDir: sites/{generator['slug']}
    buildCommand: echo "prebuilt static site"
    staticPublishPath: ./sites/{generator['slug']}/dist"""
        )
    return "services:\n" + "\n".join(blocks) + "\n"


def reset_sites_dir() -> None:
    if SITES_DIR.exists():
        shutil.rmtree(SITES_DIR)
    SITES_DIR.mkdir(parents=True, exist_ok=True)


def write_site(generator: dict, tools: list[dict]) -> None:
    site_dir = SITES_DIR / generator["slug"]
    dist_dir = site_dir / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    (dist_dir / "styles.css").write_text(shared_styles())
    (dist_dir / "index.html").write_text(render_index(generator, tools))
    (site_dir / "README.md").write_text(site_readme(generator))
    (site_dir / "metadata.json").write_text(json.dumps(generator, indent=2))


def main() -> None:
    tools = materialize_tools()
    reset_sites_dir()
    for generator in GENERATORS:
        write_site(generator, tools)

    (ROOT / "README.md").write_text(root_readme())
    (ROOT / "render.yaml").write_text(render_yaml())
    (ROOT / "selected-tools.json").write_text(json.dumps({"count": len(tools), "tools": tools}, indent=2))
    print(f"Wrote {len(GENERATORS)} static site variants with {len(tools)} tools each into {SITES_DIR}")


if __name__ == "__main__":
    main()
