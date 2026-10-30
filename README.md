# Production-Minded AI Research Agent

A structured, resilient agentic research system designed for evaluating tools and technologies. Built as part of the AI Startup Intern Assignment.

## Demo Video
- Link:https://drive.google.com/file/d/1p3pASnpWZnVb-3UxqSHzREHf49gpPR5B/view?usp=drive_link)

---

## Architecture Overview
The system follows a deterministic **Planner-Executor-Synthesizer** design pattern:
1. **Planner:** Decomposes the user prompt into targeted sub-queries and external asset identifiers using structured Pydantic models.
2. **Executor:** Coordinates tool calls (`web_search` and `benchmarks`/`github_stats`) with built-in retry policies, timeouts, and noise filtering.
3. **Synthesizer:** Ingests cleaned tool telemetry and produces a strictly typed final report conforming to the required schema.

```
User Query ---> [Planner] ---> Sub-tasks & Queries
                                   |
                +------------------+------------------+
                |                                     |
        [Web Search Tool]                     [Benchmark / GitHub API]
        (Tavily with noise filter)             (5s timeout + Tenacity retry)
                |                                     |
                +------------------+------------------+
                                   |
                          Filtered Results
                                   |
                          [Synthesizer LLM]
                                   |
                      Structured Pydantic Report
```

---

## Technical Tradeoffs & Design Decisions

### 1. Why an Agentic Approach?
Standard LLM responses rely on static training cuts, leading to hallucinations about model versions, pricing, and updated benchmarks. A multi-step agent decomposes comparative requests, queries external real-time sources, validates data, and grounds output in verifiable citations.

### 2. Planner-Executor vs. Open ReAct Loop
- **Choice:** Sequential Planner-Executor.
- **Tradeoff:** While ReAct loops provide greater autonomy, they are non-deterministic, prone to infinite token loops, and introduce unpredictable latency. A Planner-Executor guarantees bound execution time (~5-10s) and predictable cost.

### 3. Noise Filtering & Bad Tool Results
- **Filtering:** Results under 60 characters or empty snippets are pruned before synthesis.
- **Failures & Timeouts:** External API calls are wrapped in `tenacity` retries (exponential backoff) with strict 5-second timeouts. If a tool fails (e.g., 404 or missing API), the agent does not crash; instead, it passes an error note to the synthesizer, which automatically sets `confidence_level` to `Medium` or `Low` and notes the limitation.

### 4. Hallucination Reduction
Outputs are constrained by Pydantic JSON schemas. Every key finding is instructed to map directly to retrieved context and verified URLs.

---

## Setup & Running

```bash
# 1. Clone repository
git clone <your-repo-link>
cd ai-research-agent

# 2. Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env with your OPENAI_API_KEY and TAVILY_API_KEY

# 5. Run the CLI
python main.py "Compare Google Gemini, ChatGPT, and Claude AI"
```
