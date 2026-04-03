# Pelican variant

This folder contains a prebuilt static AI-tools listing variant for **Pelican**.

- Generator: `Pelican`
- Jamstack source: https://jamstack.org/generators/
- Render service name: `taaft-pelican`
- Static output path: `dist/`

Notes:

- Typical static build: pelican content -o output -s pelicanconf.py.
- The current batch uses shared TAAFT-derived content and a prebuilt static output so each variant can deploy cleanly to Render from a single monorepo.
