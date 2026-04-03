# VuePress variant

This folder contains a prebuilt static AI-tools listing variant for **VuePress**.

- Generator: `VuePress`
- Jamstack source: https://jamstack.org/generators/
- Render service name: `taaft-vuepress`
- Static output path: `dist/`

Notes:

- Typical static build: vuepress build docs producing docs/.vuepress/dist/.
- The current batch uses shared TAAFT-derived content and a prebuilt static output so each variant can deploy cleanly to Render from a single monorepo.
