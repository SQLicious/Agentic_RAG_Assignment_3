function AnswerPanel({ result, loading }) {
  if (!result && !loading) {
    return (
      <section className="app-card">
        <div className="app-card__body">
          <div className="empty-state">
            <strong>No run yet.</strong>
            <div style={{ marginTop: "8px" }}>
              Submit a query to inspect the final answer, tier assignment, route,
              cache status, and evidence summary.
            </div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="app-card">
      <div className="app-card__body stack">
        <div className="badge-row">
          {result?.tierLabel ? (
            <span className="badge badge--accent">{result.tierLabel}</span>
          ) : null}
          {result?.initialRoute ? (
            <span className="badge">Initial: {result.initialRoute}</span>
          ) : null}
          {result?.finalRoute ? (
            <span className="badge">Final: {result.finalRoute}</span>
          ) : null}
          {result?.planType ? (
            <span className="badge">Plan: {result.planType}</span>
          ) : null}
          {result?.cacheHit ? (
            <span className="badge badge--accent">Cache hit</span>
          ) : (
            <span className="badge">Cache miss</span>
          )}
        </div>

        <div>
          <h2 className="section-title">Final answer</h2>
          <div className="answer-copy">
            {loading ? "Waiting for backend response..." : result?.answer || "No answer returned."}
          </div>
        </div>

        <div className="meta-grid">
          <div className="meta-tile">
            <span className="meta-tile__label">Retrieved contexts</span>
            <span className="meta-tile__value">
              {result?.retrievedContextCount ?? 0}
            </span>
          </div>
          <div className="meta-tile">
            <span className="meta-tile__label">Sub-results</span>
            <span className="meta-tile__value">{result?.subResults?.length ?? 0}</span>
          </div>
          <div className="meta-tile">
            <span className="meta-tile__label">Chunking</span>
            <span className="meta-tile__value">
              {result?.chunkingStrategy || "Not reported"}
            </span>
          </div>
        </div>

        {result?.citations?.length ? (
          <div className="stack">
            <h3 className="section-title" style={{ marginBottom: 0 }}>
              Citations
            </h3>
            <ul className="list-reset citation-list">
              {result.citations.map((citation) => (
                <li className="citation-item" key={citation}>
                  {citation}
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>
    </section>
  );
}

export default AnswerPanel;
