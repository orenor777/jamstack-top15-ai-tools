#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "Building astro..."
docker build -t astro-taaft -f "sites/astro/Dockerfile" "sites/astro"

echo "Building docusaurus..."
docker build -t docusaurus-taaft -f "sites/docusaurus/Dockerfile" "sites/docusaurus"

echo "Building eleventy..."
docker build -t eleventy-taaft -f "sites/eleventy/Dockerfile" "sites/eleventy"

echo "Building gatsby..."
docker build -t gatsby-taaft -f "sites/gatsby/Dockerfile" "sites/gatsby"

echo "Building hexo..."
docker build -t hexo-taaft -f "sites/hexo/Dockerfile" "sites/hexo"

echo "Building hugo..."
docker build -t hugo-taaft -f "sites/hugo/Dockerfile" "sites/hugo"

echo "Building mdbook..."
docker build -t mdbook-taaft -f "sites/mdbook/Dockerfile" "sites/mdbook"

echo "Building mkdocs..."
docker build -t mkdocs-taaft -f "sites/mkdocs/Dockerfile" "sites/mkdocs"

echo "Building nextjs..."
docker build -t nextjs-taaft -f "sites/nextjs/Dockerfile" "sites/nextjs"

echo "Building nuxt..."
docker build -t nuxt-taaft -f "sites/nuxt/Dockerfile" "sites/nuxt"

echo "Building pelican..."
docker build -t pelican-taaft -f "sites/pelican/Dockerfile" "sites/pelican"

echo "Building sphinx..."
docker build -t sphinx-taaft -f "sites/sphinx/Dockerfile" "sites/sphinx"

echo "Building vitepress..."
docker build -t vitepress-taaft -f "sites/vitepress/Dockerfile" "sites/vitepress"

echo "Building vuepress..."
docker build -t vuepress-taaft -f "sites/vuepress/Dockerfile" "sites/vuepress"

echo "Building zola..."
docker build -t zola-taaft -f "sites/zola/Dockerfile" "sites/zola"

