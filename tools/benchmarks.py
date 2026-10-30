import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

STATIC_MODEL_BENCHMARKS = {
    "gemini": {
        "provider": "Google",
        "latest_flagship": "Gemini 1.5 Pro / Ultra",
        "context_window": "Up to 2,000,000 tokens",
        "chatbot_arena_elo": "~1300+",
        "mmlu_score": "85.9%",
        "best_for": "Large context, Google Workspace integration, multimodal tasks"
    },
    "chatgpt": {
        "provider": "OpenAI",
        "latest_flagship": "GPT-4o / GPT-4.5",
        "context_window": "128,000 tokens",
        "chatbot_arena_elo": "~1310+",
        "mmlu_score": "88.7%",
        "best_for": "All-round versatility, custom GPT ecosystem, voice conversation"
    },
    "claude": {
        "provider": "Anthropic",
        "latest_flagship": "Claude 3.5 Sonnet / Opus",
        "context_window": "200,000 tokens",
        "chatbot_arena_elo": "~1330+",
        "mmlu_score": "88.3%",
        "best_for": "Software engineering, nuanced writing, complex reasoning"
    }
}

def query_benchmarks(model_name: str) -> dict:
    """Retrieves standardized benchmark metrics for frontier LLMs."""
    key = model_name.lower().strip()
    for k in STATIC_MODEL_BENCHMARKS:
        if k in key:
            return {"status": "success", "model": k, "data": STATIC_MODEL_BENCHMARKS[k]}
    return {"status": "error", "message": f"Model '{model_name}' not found in benchmark catalog."}

@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=1, max=4))
def get_github_repo_stats(owner_repo: str) -> dict:
    """Fetches live repository stats from GitHub REST API."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    url = f"https://api.github.com/repos/{owner_repo}"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 404:
            return {"status": "not_found", "repo": owner_repo, "error": "Repository does not exist."}
        resp.raise_for_status()
        data = resp.json()
        return {
            "status": "success",
            "repo": owner_repo,
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "open_issues": data.get("open_issues_count", 0),
            "license": data.get("license", {}).get("spdx_id", "Unknown"),
            "last_updated": data.get("pushed_at")
        }
    except Exception as e:
        return {"status": "error", "repo": owner_repo, "error": str(e)}
