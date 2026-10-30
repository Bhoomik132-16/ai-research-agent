# Evaluation Framework & Test Queries

| # | Test Query | Expected Behavior | Observed Result & Status |
|---|---|---|---|
| 1 | **Compare Gemini, ChatGPT, and Claude for enterprise use** | Happy path: Decomposes query, retrieves benchmarks, outputs comparative report with high confidence. | ✅ PASSED: Structured report generated with LMSYS/MMLU specs and verified URLs. |
| 2 | **Compare Qdrant vs Chroma for RAG vector search** | Identifies GitHub repos, fetches stars/commit recency, aggregates feature docs. | ✅ PASSED: Tool correctly extracts GitHub telemetry and combines with web search. |
| 3 | **Compare OpenAI GPT-4o with NonExistentModelXYZ** | Edge/Failure case: Handles 404 gracefully, does not hallucinate specs, lowers confidence to 'Low'. | ✅ PASSED: Tool catches missing data; synthesizer reports limitation explicitly. |
| 4 | **Simulate web search timeout during high load** | Resilience test: Triggers retry logic, fails over after timeout without crashing agent. | ✅ PASSED: Agent gracefully absorbs HTTP error and relies on remaining tool signals. |
| 5 | **Pros and cons of multi-agent architectures** | Planner test: Recognizes non-model query, skips repo checks, relies purely on conceptual search. | ✅ PASSED: Planner selects only web search tool without redundant GitHub calls. |
