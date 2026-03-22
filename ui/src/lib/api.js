const DEFAULT_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.trim() || "http://localhost:8000";

const ENDPOINT_CANDIDATES = ["/query", "/adaptive-query", "/api/query"];

function joinUrl(baseUrl, path) {
  return `${baseUrl.replace(/\/+$/, "")}${path}`;
}

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function firstString(...values) {
  return values.find((value) => typeof value === "string" && value.trim()) || "";
}

function formatTierLabel(tier) {
  const labels = {
    tier_0: "Tier 0 - LLM direct",
    tier_1: "Tier 1 - single-route RAG",
    tier_2: "Tier 2 - multi-hop RAG",
  };

  return labels[tier] || "Unknown tier";
}

function buildContextKey(context, index) {
  const metadata = context?.metadata || {};
  return (
    context?.id ||
    metadata.parent_id ||
    [metadata.source, metadata.section_title, metadata.page, context?.content]
      .filter(Boolean)
      .join("::") ||
    `context-${index}`
  );
}

function previewText(text, limit = 260) {
  const value = (text || "").replace(/\s+/g, " ").trim();
  if (!value) {
    return "";
  }

  return value.length > limit ? `${value.slice(0, limit - 1)}...` : value;
}

function normalizeContext(context, index) {
  if (typeof context === "string") {
    return {
      id: `context-${index}`,
      source: "",
      title: "",
      preview: previewText(context),
      text: context,
      metadata: {},
    };
  }

  const metadata = context?.metadata || {};
  const text = firstString(
    context?.content,
    context?.page_content,
    context?.text,
    metadata?.content,
  );

  return {
    id: buildContextKey(context, index),
    source: firstString(metadata.source, metadata.file_name),
    title: firstString(metadata.section_title, metadata.title, metadata.page_label),
    preview: previewText(text),
    text,
    metadata,
  };
}

function normalizeSubquestion(subquestion, index) {
  if (typeof subquestion === "string") {
    return {
      id: `subquestion-${index + 1}`,
      question: subquestion,
      routeHint: "",
    };
  }

  return {
    id: `subquestion-${index + 1}`,
    question: firstString(subquestion?.question, subquestion?.text),
    routeHint: firstString(subquestion?.route_hint, subquestion?.routeHint),
  };
}

function inferTier({ finalRoute, planType, subResults, subquestions }) {
  if (planType === "multi" || subResults.length > 1 || subquestions.length > 1) {
    return "tier_2";
  }

  if (finalRoute === "llm_direct") {
    return "tier_0";
  }

  return "tier_1";
}

function normalizeSubResult(result, index) {
  const citations = asArray(result?.citations).filter(Boolean);
  const retrievedContexts = asArray(
    result?.retrieved_contexts ?? result?.retrievedContexts,
  ).map(normalizeContext);

  const tier =
    firstString(result?.tier, result?.tier_key) ||
    inferTier({
      finalRoute: firstString(result?.final_route, result?.route, result?.initial_route),
      planType: "single",
      subResults: [],
      subquestions: [],
    });

  return {
    id: `sub-result-${index + 1}`,
    question: firstString(result?.question),
    answer: firstString(result?.answer, result?.final_answer, result?.response),
    tier,
    tierLabel: firstString(result?.tier_label) || formatTierLabel(tier),
    initialRoute: firstString(result?.initial_route, result?.route),
    finalRoute: firstString(result?.final_route, result?.route),
    plannedRouteHint: firstString(result?.planned_route_hint, result?.route_hint),
    retrievalQuery: firstString(result?.retrieval_query),
    rewrittenQuestion: firstString(result?.rewritten_question),
    routeReason: firstString(result?.route_reason),
    retrievalAttempt: result?.retrieval_attempt ?? null,
    relevantDocCount: result?.relevant_doc_count ?? null,
    hallucinationGrade: firstString(result?.hallucination_grade),
    answerQualityGrade: firstString(result?.answer_quality_grade),
    citations,
    retrievedContexts,
    retrievedContextCount:
      result?.retrieved_context_count ?? retrievedContexts.length,
  };
}

function normalizeResponse(rawPayload) {
  const payload = rawPayload?.result ?? rawPayload?.data ?? rawPayload ?? {};
  const subquestions = asArray(payload?.subquestions).map(normalizeSubquestion);
  const subResults = asArray(payload?.sub_results ?? payload?.subResults).map(
    normalizeSubResult,
  );
  const retrievedContexts = asArray(
    payload?.retrieved_contexts ?? payload?.retrievedContexts ?? payload?.contexts,
  ).map(normalizeContext);

  const finalRoute = firstString(
    payload?.final_route,
    payload?.route,
    payload?.finalRoute,
    payload?.initial_route,
  );
  const initialRoute = firstString(
    payload?.initial_route,
    payload?.initialRoute,
    payload?.route,
    finalRoute,
  );
  const planType =
    firstString(payload?.plan_type, payload?.planType) ||
    (subResults.length > 1 || subquestions.length > 1 ? "multi" : "single");
  const tier =
    firstString(payload?.tier, payload?.tier_key) ||
    inferTier({ finalRoute, planType, subResults, subquestions });

  return {
    raw: payload,
    answer: firstString(payload?.final_answer, payload?.answer, payload?.response),
    citations: asArray(payload?.citations).filter(Boolean),
    tier,
    tierLabel: firstString(payload?.tier_label, payload?.tierLabel) || formatTierLabel(tier),
    planType,
    planReason: firstString(payload?.plan_reason, payload?.planReason),
    initialRoute,
    finalRoute,
    cacheHit: Boolean(payload?.cache_hit ?? payload?.cacheHit),
    cacheAllowed: Boolean(payload?.cache_allowed ?? payload?.cacheAllowed),
    cacheEnabled: Boolean(payload?.cache_enabled ?? payload?.cacheEnabled),
    cacheSimilarity: payload?.cache_similarity ?? null,
    cacheSourceQuestion: firstString(payload?.cache_source_question),
    chunkingStrategy: firstString(payload?.chunking_strategy, payload?.chunkingStrategy),
    subquestions,
    subResults,
    retrievedContexts,
    retrievedContextCount:
      payload?.retrieved_context_count ?? retrievedContexts.length,
    error: firstString(payload?.error),
  };
}

async function parseResponse(response) {
  const text = await response.text();
  if (!text) {
    return {};
  }

  try {
    return JSON.parse(text);
  } catch {
    throw new Error(
      `Backend returned ${response.status} but did not send valid JSON.`,
    );
  }
}

export async function submitQuestion(question, { signal } = {}) {
  const trimmedQuestion = question.trim();
  if (!trimmedQuestion) {
    throw new Error("Enter a question before submitting.");
  }

  let lastError = null;

  for (const path of ENDPOINT_CANDIDATES) {
    const endpoint = joinUrl(DEFAULT_BASE_URL, path);

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: trimmedQuestion }),
        signal,
      });

      if ([404, 405].includes(response.status)) {
        lastError = new Error(`Endpoint not found at ${endpoint}`);
        continue;
      }

      const payload = await parseResponse(response);

      if (!response.ok) {
        throw new Error(
          firstString(payload?.error, payload?.message) ||
            `Backend request failed with ${response.status}.`,
        );
      }

      return normalizeResponse(payload);
    } catch (error) {
      lastError = error;
      if (error.name === "AbortError") {
        throw error;
      }
    }
  }

  throw new Error(
    lastError?.message ||
      `Unable to reach the backend at ${DEFAULT_BASE_URL}. Check VITE_API_BASE_URL.`,
  );
}

export { DEFAULT_BASE_URL, formatTierLabel, normalizeResponse, previewText };
