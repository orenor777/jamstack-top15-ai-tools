import fs from "node:fs";
import path from "node:path";

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "item";
}

const dataPath = path.join(process.cwd(), "data", "tools.json");
const payload = JSON.parse(fs.readFileSync(dataPath, "utf8"));
function sanitizeDescription(description, name) {
  if (!description) {
    return `${name} is included in this AI tools directory.`;
  }

  return description
    .replace(/ is listed in the local TAAFT dataset\./g, " is included in this AI tools directory.")
    .replace(/ is an AI tool discovered from the local TAAFT scrape\./g, " is featured in this AI tools directory.");
}

const tools = payload.tools.map((tool) => ({
  ...tool,
  description: sanitizeDescription(tool.description, tool.name),
  toolSlug: `${slugify(tool.name)}-${tool.id}`,
  categorySlug: slugify(tool.category),
}));
export const siteUrl = "https://taaft-nextjs-static.onrender.com";

export function getTools() {
  return tools;
}

export function getCategories() {
  const counts = new Map();
  for (const tool of tools) {
    counts.set(tool.category, (counts.get(tool.category) || 0) + 1);
  }
  return [...counts.entries()]
    .map(([name, count]) => ({ name, count, slug: slugify(name) }))
    .sort((left, right) => left.name.localeCompare(right.name));
}

export function getToolsByCategory(categorySlug) {
  return tools.filter((tool) => tool.categorySlug === categorySlug);
}

export function getToolBySlug(toolSlug) {
  return tools.find((tool) => tool.toolSlug === toolSlug);
}
