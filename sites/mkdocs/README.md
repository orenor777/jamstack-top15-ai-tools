# MkDocs variant

This folder contains a prebuilt static AI-tools listing variant for **MkDocs**.

- Generator: `MkDocs`
- Jamstack source: https://jamstack.org/generators/
- Render service name: `taaft-mkdocs`
- Static output path: `dist/`

Notes:

- Typical static build: mkdocs build producing site/.
- The current batch uses shared TAAFT-derived content and a prebuilt static output so each variant can deploy cleanly to Render from a single monorepo.
