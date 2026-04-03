# mdBook variant

This folder contains a prebuilt static AI-tools listing variant for **mdBook**.

- Generator: `mdBook`
- Jamstack source: https://jamstack.org/generators/
- Render service name: `taaft-mdbook`
- Static output path: `dist/`

Notes:

- Typical static build: mdbook build producing book/.
- The current batch uses shared TAAFT-derived content and a prebuilt static output so each variant can deploy cleanly to Render from a single monorepo.
