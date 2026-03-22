function Header({ apiBaseUrl }) {
  const resolvedBaseUrl = apiBaseUrl?.trim() || "http://localhost:8000";

  return (
    <header className="app-card" style={{ marginBottom: "20px" }}>
      <div className="app-card__body stack">
        <div className="badge-row">
          <span className="badge badge--accent">Adaptive RAG demo</span>
          <span className="badge">Hierarchical retrieval</span>
          <span className="badge">Semantic cache aware</span>
        </div>
        <div>
          <h1 style={{ margin: "0 0 8px", fontSize: "2rem", lineHeight: 1.1 }}>
            Claude Certification Knowledge Assistant
          </h1>
          <p className="muted" style={{ margin: 0, maxWidth: "70ch" }}>
            Run a question through the 3-tier router, inspect the final answer,
            and review the execution trace without digging through raw JSON.
          </p>
        </div>
        <div className="meta-grid">
          <div className="meta-tile">
            <span className="meta-tile__label">Backend base URL</span>
            <span className="meta-tile__value">{resolvedBaseUrl}</span>
          </div>
          <div className="meta-tile">
            <span className="meta-tile__label">Expected endpoint</span>
            <span className="meta-tile__value">POST /query</span>
          </div>
          <div className="meta-tile">
            <span className="meta-tile__label">Fallback endpoints</span>
            <span className="meta-tile__value">/adaptive-query, /api/query</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
