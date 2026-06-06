"""
Command-line interface for GitChronicle.

Provides an intuitive CLI for generating changelogs, stories, and release notes.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from gitchronicle.git_parser import GitParser, GitChronicleError
from gitchronicle.narrative import NarrativeEngine
from gitchronicle import __version__


console = Console()


def print_banner():
    """Print the application banner."""
    banner = Text()
    banner.append("📜 ", style="bold yellow")
    banner.append("GitChronicle", style="bold cyan")
    banner.append(f" v{__version__}", style="dim")
    console.print(Panel(banner, border_style="cyan"))


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show version and exit.")
@click.pass_context
def main(ctx, version):
    """📝 GitChronicle - Turn your git history into stories and changelogs."""
    if version:
        console.print(f"GitChronicle {__version__}")
        sys.exit(0)

    if ctx.invoked_subcommand is None:
        print_banner()
        console.print()
        console.print("[dim]Run 'gitchronicle --help' for usage information.[/dim]")


@main.command()
@click.option(
    "--repo", "-r",
    default=".",
    help="Path to the git repository.",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.option(
    "--since", "-s",
    help="Start date (e.g., '2024-01-01', '1 week ago').",
)
@click.option(
    "--until", "-u",
    help="End date (e.g., '2024-12-31', 'today').",
)
@click.option(
    "--author", "-a",
    help="Filter by author name or email.",
)
@click.option(
    "--output", "-o",
    help="Output file path (default: stdout).",
    type=click.Path(),
)
@click.option(
    "--format", "-f",
    type=click.Choice(["markdown", "json", "html"], case_sensitive=False),
    default="markdown",
    help="Output format.",
)
@click.option(
    "--style", "-S",
    type=click.Choice(["hero", "journal", "adventure"], case_sensitive=False),
    default="journal",
    help="Narrative style for story mode.",
)
@click.option(
    "--max", "-n",
    type=int,
    help="Maximum number of commits to include.",
)
def changelog(repo, since, until, author, output, format, style, max):
    """📋 Generate a structured changelog."""
    print_banner()

    try:
        parser = GitParser(repo)
        commits = parser.get_commits(
            since=since,
            until=until,
            author=author,
            max_count=max,
        )

        if not commits:
            console.print("[yellow]⚠️ No commits found matching the criteria.[/yellow]")
            return

        engine = NarrativeEngine(style=style)
        content = engine.generate_changelog(commits)

        if output:
            Path(output).write_text(content, encoding="utf-8")
            console.print(f"[green]✅ Changelog written to {output}[/green]")
        else:
            console.print(content)

        # Print summary
        table = Table(title="Summary", show_header=False, border_style="dim")
        table.add_row("Commits", str(len(commits)))
        table.add_row("Authors", str(len(set(c.author for c in commits))))
        table.add_row("Style", style)
        console.print(table)

    except GitChronicleError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option(
    "--repo", "-r",
    default=".",
    help="Path to the git repository.",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.option(
    "--since", "-s",
    help="Start date.",
)
@click.option(
    "--until", "-u",
    help="End date.",
)
@click.option(
    "--output", "-o",
    help="Output file path.",
    type=click.Path(),
)
@click.option(
    "--style", "-S",
    type=click.Choice(["hero", "journal", "adventure"], case_sensitive=False),
    default="journal",
    help="Narrative style.",
)
@click.option(
    "--title", "-t",
    help="Custom story title.",
)
@click.option(
    "--max", "-n",
    type=int,
    help="Maximum number of commits.",
)
def story(repo, since, until, output, style, title, max):
    """📖 Generate an engaging story from commit history."""
    print_banner()

    try:
        parser = GitParser(repo)
        commits = parser.get_commits(
            since=since,
            until=until,
            max_count=max,
        )

        if not commits:
            console.print("[yellow]⚠️ No commits found to tell a story.[/yellow]")
            return

        engine = NarrativeEngine(style=style)
        content = engine.generate_story(commits, title=title)

        if output:
            Path(output).write_text(content, encoding="utf-8")
            console.print(f"[green]✅ Story written to {output}[/green]")
        else:
            console.print(content)

    except GitChronicleError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option(
    "--repo", "-r",
    default=".",
    help="Path to the git repository.",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.option(
    "--version", "-v",
    required=True,
    help="Version number (e.g., 'v1.2.3').",
)
@click.option(
    "--since", "-s",
    help="Start date for commits to include.",
)
@click.option(
    "--output", "-o",
    help="Output file path.",
    type=click.Path(),
)
@click.option(
    "--compare-url",
    help="URL for full changelog comparison.",
)
def release(repo, version, since, output, compare_url):
    """🚀 Generate release notes for a version."""
    print_banner()

    try:
        parser = GitParser(repo)
        commits = parser.get_commits(since=since)

        if not commits:
            console.print("[yellow]⚠️ No commits found for this release.[/yellow]")
            return

        engine = NarrativeEngine()
        content = engine.generate_release_notes(
            commits,
            version=version,
            compare_url=compare_url,
        )

        if output:
            Path(output).write_text(content, encoding="utf-8")
            console.print(f"[green]✅ Release notes written to {output}[/green]")
        else:
            console.print(content)

    except GitChronicleError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option(
    "--repo", "-r",
    default=".",
    help="Path to the git repository.",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.option(
    "--since", "-s",
    help="Start date.",
)
@click.option(
    "--until", "-u",
    help="End date.",
)
@click.option(
    "--max", "-n", "max_count",
    type=int,
    default=20,
    help="Maximum commits to show.",
)
def stats(repo, since, until, max_count):
    """📊 Show commit statistics."""
    print_banner()

    try:
        parser = GitParser(repo)
        commits = parser.get_commits(
            since=since,
            until=until,
            max_count=max_count,
        )

        if not commits:
            console.print("[yellow]⚠️ No commits found.[/yellow]")
            return

        git_stats = parser.get_stats(commits)

        # Overall stats
        table = Table(title="📊 Commit Statistics", border_style="cyan")
        table.add_column("Metric", style="bold")
        table.add_column("Value", style="green")

        table.add_row("Total Commits", str(git_stats.get("total_commits", 0)))
        table.add_row("Unique Authors", str(git_stats.get("unique_authors", 0)))
        table.add_row("Top Contributor", git_stats.get("top_author", "N/A"))
        table.add_row("Files Touched", str(git_stats.get("unique_files", 0)))

        date_range = git_stats.get("date_range", {})
        if date_range:
            first = date_range.get("first")
            last = date_range.get("last")
            if first and last:
                table.add_row(
                    "Date Range",
                    f"{first.strftime('%Y-%m-%d')} ~ {last.strftime('%Y-%m-%d')}"
                )

        console.print(table)

        # Category breakdown
        categories = git_stats.get("categories", {})
        if categories:
            cat_table = Table(title="📁 By Category", border_style="dim")
            cat_table.add_column("Category", style="bold")
            cat_table.add_column("Count", style="yellow")
            cat_table.add_column("Bar", style="cyan")

            max_count = max(categories.values()) if categories else 1
            for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
                bar_len = int((count / max_count) * 20)
                bar = "█" * bar_len
                cat_table.add_row(cat, str(count), bar)

            console.print(cat_table)

        # Author breakdown
        authors = git_stats.get("author_commits", {})
        if authors:
            auth_table = Table(title="👥 By Author", border_style="dim")
            auth_table.add_column("Author", style="bold")
            auth_table.add_column("Commits", style="yellow")
            auth_table.add_column("Bar", style="magenta")

            max_auth = max(authors.values()) if authors else 1
            for author, count in sorted(authors.items(), key=lambda x: -x[1])[:10]:
                bar_len = int((count / max_auth) * 20)
                bar = "█" * bar_len
                auth_table.add_row(author, str(count), bar)

            console.print(auth_table)

    except GitChronicleError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)


@main.command()
@click.option(
    "--repo", "-r",
    default=".",
    help="Path to the git repository.",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
def init(repo):
    """🔧 Initialize GitChronicle configuration."""
    print_banner()

    config_path = Path(repo) / ".gitchronicle.yml"
    config_content = """# GitChronicle Configuration
# https://github.com/longhao666/GitChronicle

# Default narrative style: hero, journal, adventure
style: journal

# Output settings
output:
  format: markdown
  filename: CHANGELOG.md

# Categories mapping (override defaults if needed)
# categories:
#   feat: "✨ Features"
#   fix: "🐛 Bug Fixes"

# Ignore patterns for commits
ignore:
  - "^Merge branch"
  - "^Merge pull request"
  - "^WIP"

# Authors to exclude
# exclude_authors:
#   - "dependabot"
"""

    if config_path.exists():
        console.print(f"[yellow]⚠️ Config already exists at {config_path}[/yellow]")
        if not click.confirm("Overwrite?"):
            return

    config_path.write_text(config_content, encoding="utf-8")
    console.print(f"[green]✅ Config created at {config_path}[/green]")


if __name__ == "__main__":
    main()
