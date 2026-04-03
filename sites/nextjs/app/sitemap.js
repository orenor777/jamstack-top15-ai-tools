import { getCategories, getTools, siteUrl } from "../lib/tools";

export const dynamic = "force-static";

export default function sitemap() {
  const categories = getCategories().map((category) => ({
    url: `${siteUrl}/categories/${category.slug}`,
  }));
  const tools = getTools().map((tool) => ({
    url: `${siteUrl}/tools/${tool.toolSlug}`,
  }));

  return [{ url: siteUrl }, ...categories, ...tools];
}
