import Link from "next/link";
import { getToolBySlug, getTools } from "../../../lib/tools";

export function generateStaticParams() {
  return getTools().map((tool) => ({ toolSlug: tool.toolSlug }));
}

export default async function ToolPage({ params }) {
  const { toolSlug } = await params;
  const tool = getToolBySlug(toolSlug);

  if (!tool) {
    return <div>Tool not found.</div>;
  }

  return (
    <div className="page-shell">
      <header className="site-header">
        <div className="brand-block">
          <div className="brand-mark">N</div>
          <div>
            <div><strong>AI Tools Directory</strong></div>
            <div className="meta-note">Tool details and category navigation</div>
          </div>
        </div>
        <Link href="/">All tools</Link>
      </header>

      <main>
        <section className="tool-detail">
          <div className="breadcrumb">
            <Link href="/">Home</Link>
            <span>/</span>
            <Link href={`/categories/${tool.categorySlug}`}>{tool.category}</Link>
            <span>/</span>
            <span>{tool.name}</span>
          </div>
          <div className="badge">Tool page</div>
          <h1>{tool.name}</h1>
          <div className="detail-copy">
            <p>{tool.description}</p>
          </div>
          <div className="detail-meta">
            <div className="detail-row">
              <span className="detail-label">Category</span>
              <Link href={`/categories/${tool.categorySlug}`}>{tool.category}</Link>
            </div>
            <div className="detail-row">
              <span className="detail-label">Pricing</span>
              <span>{tool.pricing}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Domain</span>
              <span>{tool.domain || "Unknown domain"}</span>
            </div>
          </div>
          <div className="detail-actions">
            <a className="button button-primary" href={tool.url} target="_blank" rel="noreferrer">
              Visit tool
            </a>
            <Link className="button button-secondary" href={`/categories/${tool.categorySlug}`}>
              More {tool.category} tools
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}
