# Hugo variant

This folder contains a prebuilt static AI-tools listing variant for **Hugo**.

- Generator: `Hugo`
- Jamstack source: https://jamstack.org/generators/
- Render service name: `taaft-hugo`
- Static output path: `dist/`

Notes:

- Typical static build: hugo --minify producing public/.
- The current batch uses shared TAAFT-derived content and a prebuilt static output so each variant can deploy cleanly to Render from a single monorepo.
