function renderValue(value, fallback = "Not reported") {
  if (value === null || value === undefined || value === "") {
    return fallback;
  }

  return value;
}

function TracePanel({ result, loading }) {
  if (!result && !loading) {
    return null;
  }

  return (
    <section className="app-card app-trace">
      <div className="app-card__body stack">
        <div>
          <h2 className="section-title">Execution trace</h2>
          <p className="muted" style={{ margin: 0 }}>
            Planner, routing, retrieval, grading, and sub-question details.
          </p>
        </div>

        <div className="meta-grid">
          <div className="meta-tile">
            <span className="meta-tile__label">Plan type</span>
            <span className="meta-tile__value">{renderValue(result?.planType)}</span>
          </div>
          <div className="meta-tile">
            <span className="meta-tile__label">Plan reason</span>
            <span className="meta-tile__value">{renderValue(result?.planReason)}</span>
          </div>
          <div className="meta-tile">
            <span className="meta-tile__label">Initial route</span>
            <span className="meta-tile__value">{renderValue(result?.initialRoute)}</span>
          </div>
          <div className="meta-tile">
            <span className="meta-tile__label">Final route</span>
            <span className="meta-tile__value">{renderValue(result?.finalRoute)}</span>
          </div>
        </div>

        {result?.subquestions?.length ? (
          <div className="stack">
            <h3 className="section-title" style={{ marginBottom: 0 }}>
              Planned sub-questions
            </h3>
            <ul className="list-reset trace-list">
              {result.subquestions.map((subquestion) => (
                <li className="trace-item" key={subquestion.id}>
                  <strong>{subquestion.question || "Unnamed sub-question"}</strong>
                  <div className="muted">
                    Route hint: {renderValue(subquestion.routeHint, "None")}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ) : null}

        {result?.subResults?.length ? (
          <div className="stack">
            <h3 className="section-title" style={{ marginBottom: 0 }}>
              Sub-results
            </h3>
            {result.subResults.map((subResult) => (
              <details className="subresult-card" key={subResult.id} open>
                <summary>
                  <span>{subResult.question || "Sub-result"}</span>
                  <span className="muted">
                    {subResult.finalRoute || subResult.initialRoute || "No route"}
                  </span>
                </summary>
                <div className="subresult-body stack">
                  <div className="badge-row">
                    {subResult.tierLabel ? <span className="badge">{subResult.tierLabel}</span> : null}
                    {subResult.plannedRouteHint ? (
                      <span className="badge">Hint: {subResult.plannedRouteHint}</span>
                    ) : null}
                    {subResult.retrievalAttempt ? (
                      <span className="badge">Retrieval attempt {subResult.retrievalAttempt}</span>
                    ) : null}
                    {subResult.relevantDocCount !== null ? (
                      <span className="badge">Relevant docs: {subResult.relevantDocCount}</span>
                    ) : null}
                  </div>
                  <div className="meta-grid">
                    <div className="meta-tile">
                      <span className="meta-tile__label">Route reason</span>
                      <span className="meta-tile__value">
                        {renderValue(subResult.routeReason)}
                      </span>
                    </div>
                    <div className="meta-tile">
                      <span className="meta-tile__label">Rewrite</span>
                      <span className="meta-tile__value">
                        {renderValue(subResult.rewrittenQuestion)}
                      </span>
                    </div>
                    <div className="meta-tile">
                      <span className="meta-tile__label">Retrieval query</span>
                      <span className="meta-tile__value">
                        {renderValue(subResult.retrievalQuery)}
                      </span>
                    </div>
                    <div className="meta-tile">
                      <span className="meta-tile__label">Grades</span>
                      <span className="meta-tile__value">
                        Hallucination: {renderValue(subResult.hallucinationGrade)} | Quality:{" "}
                        {renderValue(subResult.answerQualityGrade)}
                      </span>
                    </div>
                  </div>
                  <div className="trace-answer">{subResult.answer || "No sub-answer returned."}</div>
                </div>
              </details>
            ))}
          </div>
        ) : null}

        <div className="stack">
          <h3 className="section-title" style={{ marginBottom: 0 }}>
            Retrieved evidence
          </h3>
          {result?.retrievedContexts?.length ? (
            <ul className="list-reset context-list">
              {result.retrievedContexts.map((context) => (
                <li className="context-item" key={context.id}>
                  <div className="context-title">
                    {context.title || context.source || "Retrieved context"}
                  </div>
                  <div className="muted context-source">
                    {context.source || "Unknown source"}
                  </div>
                  <div className="context-preview">
                    {context.preview || "No preview available."}
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <div className="empty-state">
              No retrieved contexts were returned for this run. Tier 0 direct answers
              will normally show no retrieval evidence here.
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default TracePanel;
