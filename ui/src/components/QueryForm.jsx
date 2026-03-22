function QueryForm({
  value,
  onChange,
  onSubmit,
  loading,
  error,
  samplePrompts,
  onPickSample,
}) {
  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit();
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onSubmit();
    }
  };

  return (
    <section className="app-card">
      <div className="app-card__body stack">
        <div>
          <h2 className="section-title" style={{ marginBottom: "6px" }}>
            Ask a question
          </h2>
          <p className="muted" style={{ margin: 0 }}>
            Enter submits. Use Shift+Enter for a multiline question.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="stack">
          <textarea
            aria-label="Question"
            className="query-input"
            disabled={loading}
            onChange={(event) => onChange(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about the exam guide, Anthropic Courses, or a multi-hop comparison..."
            rows={5}
            value={value}
          />

          <div className="query-actions">
            <button
              className="query-submit"
              disabled={loading || !value.trim()}
              type="submit"
            >
              {loading ? "Running query..." : "Run query"}
            </button>
            <span className="muted">
              The UI normalizes final_answer, routes, tier, cache, and trace fields.
            </span>
          </div>
        </form>

        {error ? <div className="error-banner">{error}</div> : null}

        <div className="stack">
          <h3 className="section-title" style={{ marginBottom: "0" }}>
            Sample prompts
          </h3>
          <div className="pill-list">
            {samplePrompts.map((prompt) => (
              <button
                className="sample-chip"
                key={prompt}
                onClick={() => onPickSample(prompt)}
                type="button"
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export default QueryForm;
