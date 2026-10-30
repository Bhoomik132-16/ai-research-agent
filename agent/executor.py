from agent.schemas import ResearchPlan
from tools.web_search import search_web
from tools.benchmarks import query_benchmarks, get_github_repo_stats

def execute_plan(plan: ResearchPlan) -> dict:
    """Executes the planned steps, calling tools and gathering structured context."""
    execution_context = {
        "web_results": [],
        "benchmarks": [],
        "github_stats": [],
        "errors_encountered": []
    }

    for model in plan.target_models:
        bench = query_benchmarks(model)
        if bench.get("status") == "success":
            execution_context["benchmarks"].append(bench)
        else:
            execution_context["errors_encountered"].append(f"Benchmark lookup failed: {bench.get('message')}")

    for repo in plan.github_repos:
        stats = get_github_repo_stats(repo)
        if stats.get("status") == "success":
            execution_context["github_stats"].append(stats)
        else:
            execution_context["errors_encountered"].append(f"GitHub repo error on {repo}: {stats.get('error')}")

    for query_item in plan.search_queries:
        try:
            results = search_web(query_item.query)
            for res in results:
                execution_context["web_results"].append(res)
        except Exception as e:
            execution_context["errors_encountered"].append(f"Web search error for '{query_item.query}': {str(e)}")

    return execution_context
