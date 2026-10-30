from pydantic import BaseModel, Field
from typing import List, Literal

class SearchSubQuery(BaseModel):
    query: str = Field(description="Search sub-query to run via Tavily")
    target_aspect: str = Field(description="Aspect being researched, e.g., 'pricing', 'benchmarks'")

class ResearchPlan(BaseModel):
    target_models: List[str] = Field(description="List of AI models or tools to compare")
    github_repos: List[str] = Field(default=[], description="GitHub repositories to inspect (owner/repo)")
    search_queries: List[SearchSubQuery] = Field(description="List of search queries to gather required facts")

class ResearchReport(BaseModel):
    user_question: str
    short_answer: str
    key_findings: List[str]
    sources_used: List[str]
    confidence_level: Literal["High", "Medium", "Low"]
    limitations_or_assumptions: List[str]
    suggested_next_steps: List[str]
