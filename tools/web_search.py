import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
def search_web(query: str, max_results: int = 3) -> list:
    """
    Searches the web using Tavily API.
    Filters out noisy or weak results under 60 characters.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return [{
            "url": "https://example.com/fallback-data",
            "content": f"Simulated search findings for query: '{query}'. Set TAVILY_API_KEY for live results."
        }]

    endpoint = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results
    }
    
    response = requests.post(endpoint, json=payload, timeout=8)
    response.raise_for_status()
    data = response.json()
    
    results = []
    for item in data.get("results", []):
        content = item.get("content", "").strip()
        if len(content) >= 60:
            results.append({
                "url": item.get("url"),
                "content": content
            })
    return results
