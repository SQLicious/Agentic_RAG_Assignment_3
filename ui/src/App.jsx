import { useMemo, useState } from "react";
import "./App.css";
import AnswerPanel from "./components/AnswerPanel";
import ChecklistPanel from "./components/ChecklistPanel";
import DiagramTabs from "./components/DiagramTabs";
import Header from "./components/Header";
import QueryForm from "./components/QueryForm";
import TracePanel from "./components/TracePanel";
import { submitQuestion } from "./lib/api";

const SAMPLE_PROMPTS = [
  "What does the Claude Certified Architect - Foundations Certification Exam Guide cover?",
  "Is Claude Code in Action currently listed on Anthropic Courses, and what does its course page say it covers?",
  "How do Claude 101 and Claude Code in Action differ in focus?",
];

function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const diagnostics = useMemo(() => {
    if (!result) {
      return null;
    }

    const retrievalUsed =
      result.retrievedContextCount > 0 ||
      ["vectorstore", "web_search"].includes(result.finalRoute);

    return {
      answered: Boolean(result.answer),
      tier: result.tierLabel || result.tier || "Unknown",
      routeChosen: result.finalRoute || result.initialRoute || "Unknown",
      retrievalUsed,
      multiHopUsed: result.planType === "multi" || result.subResults.length > 1,
      cacheUsed: Boolean(result.cacheHit),
    };
  }, [result]);

  const handleSubmit = async (nextValue = query) => {
    const question = nextValue.trim();
    if (!question || loading) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const payload = await submitQuestion(question);
      setResult(payload);
      setQuery(question);
    } catch (caughtError) {
      setResult(null);
      setError(caughtError.message || "Unable to complete the request.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Header apiBaseUrl={import.meta.env.VITE_API_BASE_URL} />
      <main className="app-grid">
        <section className="app-column app-main">
          <QueryForm
            error={error}
            loading={loading}
            onChange={setQuery}
            onPickSample={setQuery}
            onSubmit={handleSubmit}
            samplePrompts={SAMPLE_PROMPTS}
            value={query}
          />
          <AnswerPanel loading={loading} result={result} />
          <TracePanel loading={loading} result={result} />
        </section>

        <aside className="app-column app-side">
          <ChecklistPanel diagnostics={diagnostics} result={result} />
          <DiagramTabs result={result} />
        </aside>
      </main>
    </div>
  );
}

export default App;
