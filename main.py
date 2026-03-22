import uuid

from dotenv import load_dotenv
from langgraph.types import Command
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.rule import Rule

from linkedin_post_automation.graph import build_graph

load_dotenv()

console = Console()


def display_posts(posts: list[dict]) -> None:
    console.print()
    console.print(Rule("[bold]Generated Posts[/bold]"))
    console.print()

    for i, post in enumerate(posts, 1):
        hashtags = " ".join(f"#{tag}" for tag in post["hashtags"])
        body = f"[bold]{post['title']}[/bold]\n\n{post['content']}\n\n[dim]{hashtags}[/dim]"
        console.print(Panel(body, title=f"Post {i}", border_style="cyan", expand=False))
        console.print()


def main():
    console.print(
        Panel(
            "[bold]LinkedIn Post Automation[/bold]\n"
            "Generate AI-powered posts and publish them to LinkedIn",
            border_style="blue",
        )
    )
    console.print()

    topic = Prompt.ask("[bold green]Enter a topic for your LinkedIn post[/bold green]")

    if not topic.strip():
        console.print("[red]Topic cannot be empty.[/red]")
        return

    console.print()
    console.print("[yellow]Generating 3 post suggestions...[/yellow]")

    graph = build_graph()
    thread_config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    result = graph.invoke({"topic": topic}, config=thread_config)

    state = graph.get_state(thread_config)
    if not state.next:
        console.print("[red]Unexpected: graph completed without review step.[/red]")
        return

    interrupt_value = state.tasks[0].interrupts[0].value
    display_posts(interrupt_value["posts"])

    selection = IntPrompt.ask(
        "[bold green]Select a post to publish (1-3)[/bold green]",
        choices=["1", "2", "3"],
    )
    selected_index = selection - 1

    console.print()
    console.print("[yellow]Publishing to LinkedIn...[/yellow]")

    result = graph.invoke(
        Command(resume=selected_index),
        config=thread_config,
    )

    publish_result = result.get("result", {})
    if publish_result.get("success"):
        console.print()
        console.print(
            Panel(
                f"[bold green]{publish_result['message']}[/bold green]\n"
                f"Post ID: {publish_result.get('post_id', 'N/A')}",
                title="Success",
                border_style="green",
            )
        )
    else:
        console.print()
        console.print(
            Panel(
                f"[bold red]Failed to publish[/bold red]\n"
                f"{publish_result.get('message', 'Unknown error')}",
                title="Error",
                border_style="red",
            )
        )


if __name__ == "__main__":
    main()
