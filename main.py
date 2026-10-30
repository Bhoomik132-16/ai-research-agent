import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent.planner import create_plan
from agent.executor import execute_plan
from agent.synthesizer import synthesize_report

load_dotenv()
console = Console()

def run_agent(question: str):
    console.print(Panel(f"[bold cyan]Research Question:[/bold cyan] {question}", title="AI Research Agent"))

    with console.status("[bold green]Step 1/3: Creating research plan...[/bold green]"):
        plan = create_plan(question)
    console.print(f"[green]✓[/green] Planned targets: {plan.target_models}")
    console.print(f"[green]✓[/green] Search queries: {[q.query for q in plan.search_queries]}")

    with console.status("[bold yellow]Step 2/3: Executing tools (Web Search & Benchmarks)...[/bold yellow]"):
        context = execute_plan(plan)
    console.print(f"[yellow]✓[/yellow] Retrieved {len(context['web_results'])} sources & {len(context['benchmarks'])} benchmark sets.")
    if context["errors_encountered"]:
        console.print(f"[red]! Warnings encountered:[/red] {context['errors_encountered']}")

    with console.status("[bold magenta]Step 3/3: Synthesizing final structured report...[/bold magenta]"):
        report = synthesize_report(question, context)

    console.print("\n[bold underline]=== FINAL RESEARCH REPORT ===[/bold underline]\n")
    console.print(f"[bold]Short Answer:[/bold] {report.short_answer}\n")

    table = Table(title="Key Findings")
    table.add_column("#", style="dim", width=4)
    table.add_column("Insight", style="white")
    for idx, finding in enumerate(report.key_findings, 1):
        table.add_row(str(idx), finding)
    console.print(table)

    console.print(f"\n[bold]Confidence Level:[/bold] [bold green]{report.confidence_level}[/bold green]")
    console.print(f"[bold]Sources Used:[/bold] {', '.join(report.sources_used)}")
    console.print(f"[bold]Limitations / Assumptions:[/bold] {report.limitations_or_assumptions}")
    console.print(f"[bold]Suggested Next Steps:[/bold] {report.suggested_next_steps}\n")

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Compare Google Gemini, ChatGPT, and Claude AI for enterprise use."
    run_agent(query)
