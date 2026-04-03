import Link from "next/link";
import { getCategories, getToolsByCategory } from "../../../lib/tools";

export function generateStaticParams() {
  return getCategories().map((category) => ({ categorySlug: category.slug }));
}

export default async function CategoryPage({ params }) {
  const { categorySlug } = await params;
  const category = getCategories().find((item) => item.slug === categorySlug);
  const tools = getToolsByCategory(categorySlug);

  if (!category) {
    return <div>Category not found.</div>;
  }

  return (
    <div className="page-shell">
      <header className="site-header">
        <div className="brand-block">
          <div className="brand-mark">N</div>
          <div>
            <div><strong>AI Tools Directory</strong></div>
            <div className="meta-note">Browse tools by category</div>
          </div>
        </div>
        <Link href="/">All tools</Link>
      </header>

      <main>
        <section className="category-page">
          <div className="breadcrumb">
            <Link href="/">Home</Link>
            <span>/</span>
            <span>{category.name}</span>
          </div>
          <div className="badge">Category page</div>
          <h1>
            {category.name} <span>AI tools</span>
          </h1>
          <p className="meta-note">
            {tools.length} tools in this category, all rendered into static HTML by Next.js.
          </p>
          <div className="button-row">
            <Link className="button button-secondary" href="/">
              Back to all tools
            </Link>
          </div>
        </section>

        <section className="directory">
          <div className="tool-grid">
            {tools.map((tool) => (
              <article key={tool.toolSlug} className="tool-card">
                <div className="tool-top">
                  <span className="tool-category">{tool.category}</span>
                  <span className="tool-pricing">{tool.pricing}</span>
                </div>
                <h3>{tool.name}</h3>
                <p>{tool.description}</p>
                <div className="tool-footer">
                  <span>{tool.domain || "Unknown domain"}</span>
                  <Link className="tool-link" href={`/tools/${tool.toolSlug}`}>
                    View details
                  </Link>
                </div>
              </article>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
