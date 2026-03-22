const DEFAULT_ITEMS = [
  { label: "Answered", value: "No run yet" },
  { label: "Tier assigned", value: "Not available" },
  { label: "Route chosen", value: "Not available" },
  { label: "Retrieval used", value: "Not available" },
  { label: "Multi-hop used", value: "Not available" },
  { label: "Cache used", value: "Not available" },
];

function ChecklistPanel({ diagnostics, result }) {
  const items = diagnostics
    ? [
        { label: "Answered", value: diagnostics.answered ? "Yes" : "No" },
        { label: "Tier assigned", value: diagnostics.tier },
        { label: "Route chosen", value: diagnostics.routeChosen },
        { label: "Retrieval used", value: diagnostics.retrievalUsed ? "Yes" : "No" },
        { label: "Multi-hop used", value: diagnostics.multiHopUsed ? "Yes" : "No" },
        { label: "Cache used", value: diagnostics.cacheUsed ? "Yes" : "No" },
      ]
    : DEFAULT_ITEMS;

  return (
    <section className="app-card">
      <div className="app-card__body stack">
        <h2 className="section-title">Run diagnostics</h2>
        <ul className="list-reset diagnostics-list">
          {items.map((item) => (
            <li className="diagnostics-item" key={item.label}>
              <span className="diagnostics-label">{item.label}</span>
              <span className="diagnostics-value">{item.value}</span>
            </li>
          ))}
        </ul>
        {result?.cacheSourceQuestion ? (
          <div className="meta-tile">
            <span className="meta-tile__label">Cache source question</span>
            <span className="meta-tile__value">{result.cacheSourceQuestion}</span>
          </div>
        ) : null}
      </div>
    </section>
  );
}

export default ChecklistPanel;
