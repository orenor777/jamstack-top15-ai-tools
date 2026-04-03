import fs from "node:fs";
import path from "node:path";

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "item";
}

const dataPath = path.join(process.cwd(), "data", "tools.json");
const payload = JSON.parse(fs.readFileSync(dataPath, "utf8"));
const tools = payload.tools.map((tool) => ({
  ...tool,
  toolSlug: `${slugify(tool.name)}-${tool.id}`,
  categorySlug: slugify(tool.category),
}));

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
