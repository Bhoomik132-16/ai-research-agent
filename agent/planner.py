import os
from openai import OpenAI
from agent.schemas import ResearchPlan

def create_plan(user_query: str) -> ResearchPlan:
    """Decomposes the user query into sub-tasks and tool invocations."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "mock-key"))
    
    prompt = f"""You are a research planning agent. Given the user query, output a structured research plan.
User Query: "{user_query}"

Identify:
1. Target models / tools to compare.
2. Specific GitHub repos (owner/repo) if open-source software is involved.
3. 2-3 focused web search queries to retrieve benchmarks, pricing, and key features.
"""

    if not os.getenv("OPENAI_API_KEY"):
        return ResearchPlan(
            target_models=["Google Gemini", "ChatGPT (OpenAI)", "Claude (Anthropic)"],
            github_repos=[],
            search_queries=[
                {"query": "Gemini 1.5 Pro vs GPT-4o vs Claude 3.5 Sonnet comparison", "target_aspect": "overall"},
                {"query": "LLM API pricing per 1M tokens Gemini GPT Claude", "target_aspect": "pricing"}
            ]
        )

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert research planner."},
            {"role": "user", "content": prompt}
        ],
        response_format=ResearchPlan
    )
    return response.choices[0].message.parsed
