import argparse
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from api.github_client import GitHubClient
from features.stats import get_basic_stats
from features.languages import get_top_languages
from features.streak import get_streak
from features.graph import render_contribution_graph
from utils.display import display_profile, get_export_text

console = Console()

def main():
    parser = argparse.ArgumentParser(description="GitHub Activity Tracker CLI")
    parser.add_argument("--user", required=False, help="GitHub username")
    parser.add_argument("--export", action="store_true", help="Export to {username}_report.txt")
    
    args = parser.parse_args()
    
    if args.user:
        username = args.user
    else:
        username = input("Enter a GitHub username to track (e.g. torvalds): ").strip()
        if not username:
             console.print("[red]Error: Username cannot be blank.[/red]")
             sys.exit(1)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=f"⏳ Fetching GitHub data for @{username}...", total=None)
            
            client = GitHubClient(username)
            
            user_data = client.get_user()
            if not user_data or ("message" in user_data and user_data["message"] == "Not Found"):
                 console.print(f"[red]Error: User @{username} not found.[/red]")
                 sys.exit(1)
                 
            repos_data = client.get_repos()
            events_data = client.get_events()
            calendar_data = client.get_contribution_calendar()
            
            stats = get_basic_stats(user_data, repos_data)
            languages = get_top_languages(repos_data)
            streak_data = get_streak(events_data)
            graph_data = render_contribution_graph(calendar_data, events_data)
            
        display_profile(stats, languages, streak_data, graph_data)
        
        if args.export:
            filename = f"{username}_report.txt"
            export_text = get_export_text(stats, languages, streak_data, graph_data)
            with open(filename, "w", encoding="utf-8") as f:
                 f.write(export_text)
            console.print(f"\n✅ Report saved to [bold green]{filename}[/bold green]")
            
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        sys.exit(1)
        
    print("\n✅ PROJECT COMPLETE!\n")
    print("To use with your real GitHub token:")
    print("1. Open github-activity-tracker/.env")
    print("2. Replace \"your_github_personal_access_token_here\" with your real token")
    print("   (Get one at: https://github.com/settings/tokens → needs read:user and public_repo scopes)")
    print("3. Run: python main.py --user YOUR_GITHUB_USERNAME\n")
    print("Optional: python main.py --user YOUR_GITHUB_USERNAME --export")
    print("(saves a report.txt file)")

if __name__ == "__main__":
    main()
