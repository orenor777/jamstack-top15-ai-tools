# Reproducible Framework Build Playbook

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

## Astro

- Source folder: `sites/astro`
- Static output: `sites/astro/dist`
- Docker base image: `node:20-alpine`
- Dockerfile: `sites/astro/Dockerfile`
- Current reproducible build command:

```bash
docker build -t astro-taaft -f sites/astro/Dockerfile sites/astro
docker run --rm -p 1805:80 astro-taaft
```

- Generator note: Typical static build: astro build producing dist/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Docusaurus

- Source folder: `sites/docusaurus`
- Static output: `sites/docusaurus/dist`
- Docker base image: `node:20-alpine`
- Dockerfile: `sites/docusaurus/Dockerfile`
- Current reproducible build command:

```bash
docker build -t docusaurus-taaft -f sites/docusaurus/Dockerfile sites/docusaurus
docker run --rm -p 1810:80 docusaurus-taaft
```

- Generator note: Typical static build: docusaurus build producing build/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Eleventy

- Source folder: `sites/eleventy`
- Static output: `sites/eleventy/dist`
- Docker base image: `node:20-alpine`
- Dockerfile: `sites/eleventy/Dockerfile`
- Current reproducible build command:

```bash
docker build -t eleventy-taaft -f sites/eleventy/Dockerfile sites/eleventy
docker run --rm -p 1808:80 eleventy-taaft
```

- Generator note: Typical static build: eleventy producing _site/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Gatsby

- Source folder: `sites/gatsby`
- Static output: `sites/gatsby/dist`
- Docker base image: `node:20-alpine`
- Dockerfile: `sites/gatsby/Dockerfile`
- Current reproducible build command:

```bash
docker build -t gatsby-taaft -f sites/gatsby/Dockerfile sites/gatsby
docker run --rm -p 1806:80 gatsby-taaft
```

- Generator note: Typical static build: gatsby build producing public/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Hexo

- Source folder: `sites/hexo`
- Static output: `sites/hexo/dist`
- Docker base image: `node:20-alpine`
- Dockerfile: `sites/hexo/Dockerfile`
- Current reproducible build command:

```bash
docker build -t hexo-taaft -f sites/hexo/Dockerfile sites/hexo
docker run --rm -p 1804:80 hexo-taaft
```

- Generator note: Typical static build: hexo generate producing public/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Hugo

- Source folder: `sites/hugo`
- Static output: `sites/hugo/dist`
- Docker base image: `golang:1.21-alpine`
- Dockerfile: `sites/hugo/Dockerfile`
- Current reproducible build command:

```bash
docker build -t hugo-taaft -f sites/hugo/Dockerfile sites/hugo
docker run --rm -p 1804:80 hugo-taaft
```

- Generator note: Typical static build: hugo --minify producing public/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## mdBook

- Source folder: `sites/mdbook`
- Static output: `sites/mdbook/dist`
- Docker base image: `rust:1.94-slim`
- Dockerfile: `sites/mdbook/Dockerfile`
- Current reproducible build command:

```bash
docker build -t mdbook-taaft -f sites/mdbook/Dockerfile sites/mdbook
docker run --rm -p 1806:80 mdbook-taaft
```

- Generator note: Typical static build: mdbook build producing book/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## MkDocs

- Source folder: `sites/mkdocs`
- Static output: `sites/mkdocs/dist`
- Docker base image: `python:3.11-slim`
- Dockerfile: `sites/mkdocs/Dockerfile`
- Current reproducible build command:

```bash
docker build -t mkdocs-taaft -f sites/mkdocs/Dockerfile sites/mkdocs
docker run --rm -p 1806:80 mkdocs-taaft
```

- Generator note: Typical static build: mkdocs build producing site/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Next.js

- Source folder: `sites/nextjs`
- Static output: `sites/nextjs/dist`
- Docker base image: `node:20-alpine`
- Dockerfile: `sites/nextjs/Dockerfile`
- Current reproducible build command:

```bash
docker build -t nextjs-taaft -f sites/nextjs/Dockerfile sites/nextjs
docker run --rm -p 1806:80 nextjs-taaft
```

- Generator note: Typical static build: next build with output export or next export depending on app structure.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Nuxt

- Source folder: `sites/nuxt`
- Static output: `sites/nuxt/dist`
- Docker base image: `node:20-alpine`
- Dockerfile: `sites/nuxt/Dockerfile`
- Current reproducible build command:

```bash
docker build -t nuxt-taaft -f sites/nuxt/Dockerfile sites/nuxt
docker run --rm -p 1804:80 nuxt-taaft
```

- Generator note: Typical static build: nuxi generate producing .output/public/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Pelican

- Source folder: `sites/pelican`
- Static output: `sites/pelican/dist`
- Docker base image: `python:3.11-slim`
- Dockerfile: `sites/pelican/Dockerfile`
- Current reproducible build command:

```bash
docker build -t pelican-taaft -f sites/pelican/Dockerfile sites/pelican
docker run --rm -p 1807:80 pelican-taaft
```

- Generator note: Typical static build: pelican content -o output -s pelicanconf.py.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Sphinx

- Source folder: `sites/sphinx`
- Static output: `sites/sphinx/dist`
- Docker base image: `python:3.11-slim`
- Dockerfile: `sites/sphinx/Dockerfile`
- Current reproducible build command:

```bash
docker build -t sphinx-taaft -f sites/sphinx/Dockerfile sites/sphinx
docker run --rm -p 1806:80 sphinx-taaft
```

- Generator note: Typical static build: sphinx-build -b html source build.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## VitePress

- Source folder: `sites/vitepress`
- Static output: `sites/vitepress/dist`
- Docker base image: `node:20-alpine`
- Dockerfile: `sites/vitepress/Dockerfile`
- Current reproducible build command:

```bash
docker build -t vitepress-taaft -f sites/vitepress/Dockerfile sites/vitepress
docker run --rm -p 1809:80 vitepress-taaft
```

- Generator note: Typical static build: vitepress build docs producing docs/.vitepress/dist/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## VuePress

- Source folder: `sites/vuepress`
- Static output: `sites/vuepress/dist`
- Docker base image: `node:20-alpine`
- Dockerfile: `sites/vuepress/Dockerfile`
- Current reproducible build command:

```bash
docker build -t vuepress-taaft -f sites/vuepress/Dockerfile sites/vuepress
docker run --rm -p 1808:80 vuepress-taaft
```

- Generator note: Typical static build: vuepress build docs producing docs/.vuepress/dist/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.


## Zola

- Source folder: `sites/zola`
- Static output: `sites/zola/dist`
- Docker base image: `rust:1.94-slim`
- Dockerfile: `sites/zola/Dockerfile`
- Current reproducible build command:

```bash
docker build -t zola-taaft -f sites/zola/Dockerfile sites/zola
docker run --rm -p 1804:80 zola-taaft
```

- Generator note: Typical static build: zola build producing public/.
- Current implementation note: this batch commits the static output so the container validates and serves the artifact deterministically. Native framework build steps can be swapped in later without changing the deployment shape.

