# Sphinx variant

This folder contains a prebuilt static AI-tools listing variant for **Sphinx**.

- Generator: `Sphinx`
- Jamstack source: https://jamstack.org/generators/
- Render service name: `taaft-sphinx`
- Static output path: `dist/`

Notes:

- Typical static build: sphinx-build -b html source build.
- The current batch uses shared TAAFT-derived content and a prebuilt static output so each variant can deploy cleanly to Render from a single monorepo.
