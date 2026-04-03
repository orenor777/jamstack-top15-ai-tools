# Jamstack Top 15 AI Tools Batch

This repo batch contains **15 static AI-tools directory variants** based on top Jamstack site generators selected from the current Jamstack generator rankings.

Each variant:

- lists 500 tools selected from the local TAAFT dataset
- ships as a plain static site
- is intended to deploy as an independent Render static site

## Selected generators

- `Next.js`: `sites/nextjs/dist/` -> Render service `taaft-nextjs`
- `Hugo`: `sites/hugo/dist/` -> Render service `taaft-hugo`
- `Docusaurus`: `sites/docusaurus/dist/` -> Render service `taaft-docusaurus`
- `Nuxt`: `sites/nuxt/dist/` -> Render service `taaft-nuxt`
- `Gatsby`: `sites/gatsby/dist/` -> Render service `taaft-gatsby`
- `Astro`: `sites/astro/dist/` -> Render service `taaft-astro`
- `Hexo`: `sites/hexo/dist/` -> Render service `taaft-hexo`
- `VuePress`: `sites/vuepress/dist/` -> Render service `taaft-vuepress`
- `MkDocs`: `sites/mkdocs/dist/` -> Render service `taaft-mkdocs`
- `mdBook`: `sites/mdbook/dist/` -> Render service `taaft-mdbook`
- `Eleventy`: `sites/eleventy/dist/` -> Render service `taaft-eleventy`
- `Zola`: `sites/zola/dist/` -> Render service `taaft-zola`
- `VitePress`: `sites/vitepress/dist/` -> Render service `taaft-vitepress`
- `Pelican`: `sites/pelican/dist/` -> Render service `taaft-pelican`
- `Sphinx`: `sites/sphinx/dist/` -> Render service `taaft-sphinx`

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
