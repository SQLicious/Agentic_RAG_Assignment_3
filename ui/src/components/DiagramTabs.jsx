import { useState } from "react";

const TAB_KEYS = [
  { id: "summary", label: "Run Summary" },
  { id: "adaptive", label: "Adaptive Flow" },
  { id: "graph", label: "Graph View" },
];

function DiagramTabs({ result }) {
  const [activeTab, setActiveTab] = useState("summary");
  const [brokenImages, setBrokenImages] = useState({});

  const markBroken = (key) => {
    setBrokenImages((current) => ({ ...current, [key]: true }));
  };

  const renderImagePanel = (key, src, alt, caption) => {
    if (brokenImages[key]) {
      return (
        <div className="empty-state">
          {caption}
          <div style={{ marginTop: "8px" }}>Image file is missing or empty in ui/public.</div>
        </div>
      );
    }

    return (
      <div className="diagram-panel">
        <img
          alt={alt}
          className="diagram-image"
          onError={() => markBroken(key)}
          src={src}
        />
        <p className="muted" style={{ margin: "10px 0 0" }}>
          {caption}
        </p>
      </div>
    );
  };

  return (
    <section className="app-card">
      <div className="app-card__body stack">
        <div className="badge-row">
          {TAB_KEYS.map((tab) => (
            <button
              className={`tab-chip ${tab.id === activeTab ? "tab-chip--active" : ""}`}
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              type="button"
            >
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab === "summary" ? (
          <div className="stack">
            <h2 className="section-title">Run summary</h2>
            {result ? (
              <div className="meta-grid">
                <div className="meta-tile">
                  <span className="meta-tile__label">Tier</span>
                  <span className="meta-tile__value">{result.tierLabel}</span>
                </div>
                <div className="meta-tile">
                  <span className="meta-tile__label">Planner</span>
                  <span className="meta-tile__value">{result.planType || "Unknown"}</span>
                </div>
                <div className="meta-tile">
                  <span className="meta-tile__label">Contexts</span>
                  <span className="meta-tile__value">{result.retrievedContextCount}</span>
                </div>
                <div className="meta-tile">
                  <span className="meta-tile__label">Cache</span>
                  <span className="meta-tile__value">{result.cacheHit ? "Hit" : "Miss"}</span>
                </div>
              </div>
            ) : (
              <div className="empty-state">
                Run a question to see a compact summary of the live backend output.
              </div>
            )}
          </div>
        ) : null}

        {activeTab === "adaptive"
          ? renderImagePanel(
              "adaptive",
              "/architecture_aws.png",
              "Adaptive RAG architecture diagram",
              "Reference architecture panel for the adaptive wrapper and route selection flow.",
            )
          : null}

        {activeTab === "graph"
          ? renderImagePanel(
              "graph",
              "/langgraph-baseline.avif",
              "Graph execution diagram",
              "Reference graph panel for corrective and self-RAG execution inside the single-question pipeline.",
            )
          : null}
      </div>
    </section>
  );
}

export default DiagramTabs;
