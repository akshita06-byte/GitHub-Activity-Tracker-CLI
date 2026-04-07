from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def display_profile(stats, languages, streak_data, graph_data):
    if not stats:
         console.print("[red]No user data to display.[/red]")
         return
         
    # 1. Bold cyan Panel header
    header_text = f"[bold cyan]{stats.get('name')} (@{stats.get('username')})[/bold cyan]\n"
    if stats.get('bio'):
         header_text += f"{stats.get('bio')}\n"
    header_text += f"[dim]📍 {stats.get('location')} | 📅 Joined {stats.get('account_created')}[/dim]"
    
    console.print(Panel(header_text, expand=False))
    
    # 2. Table titled "📊 GitHub Stats"
    table = Table(title="📊 GitHub Stats", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="green")
    
    c_streak, total_days, l_streak = streak_data
    
    table.add_row("Followers", str(stats.get('followers')))
    table.add_row("Following", str(stats.get('following')))
    table.add_row("Public Repos", str(stats.get('public_repos')))
    table.add_row("Total Stars ⭐", str(stats.get('total_stars')))
    table.add_row("Total Forks 🍴", str(stats.get('total_forks')))
    table.add_row("Current Streak 🔥", f"{c_streak} days")
    table.add_row("Longest Streak 📈", f"{l_streak} days")
    table.add_row("Total Active Days 📅", str(total_days))
    
    console.print(table)
    console.print()
    
    # 3. Top languages bar chart
    if languages:
        console.print("[bold magenta]Top Languages:[/bold magenta]")
        max_count = max(count for _, count in languages)
        
        color_map = {
             "Python": "blue",
             "JavaScript": "yellow",
             "Java": "red",
             "C++": "magenta"
        }
        
        for lang, count in languages:
            color = color_map.get(lang, "green")
            bar_len = int((count / max_count) * 25) if max_count > 0 else 0
            bar = "█" * bar_len
            console.print(f"[{color}]{lang:<12} | {bar} ({count} repos)[/{color}]")
    else:
        console.print("[dim]No language data found.[/dim]")
    
    console.print()
    
    # 4. Contribution graph
    graph_str, is_fallback = graph_data
    
    graph_panel = Panel(graph_str, title="📈 Contribution Graph", border_style="blue", expand=False)
    console.print(graph_panel)
    
    if is_fallback:
        console.print("[yellow]⚠️ Showing last 90 days only. Add GITHUB_TOKEN to .env for full 365-day graph.[/yellow]")
        
    # 5. Bottom note
    console.print(f"\n[dim]Data fetched from GitHub API • github.com/{stats.get('username')}[/dim]")

def get_export_text(stats, languages, streak_data, graph_data):
    lines = []
    lines.append(f"GitHub Report for {stats.get('name')} (@{stats.get('username')})")
    lines.append("=" * 40)
    lines.append(f"Bio: {stats.get('bio')}")
    lines.append(f"Location: {stats.get('location')}")
    lines.append(f"Joined: {stats.get('account_created')}")
    lines.append("-" * 40)
    lines.append("STATS")
    lines.append(f"Followers: {stats.get('followers')}")
    lines.append(f"Following: {stats.get('following')}")
    lines.append(f"Public Repos: {stats.get('public_repos')}")
    lines.append(f"Total Stars: {stats.get('total_stars')}")
    lines.append(f"Total Forks: {stats.get('total_forks')}")
    
    c_streak, total_days, l_streak = streak_data
    lines.append(f"Current Streak: {c_streak} days")
    lines.append(f"Longest Streak: {l_streak} days")
    lines.append(f"Total Active Days: {total_days}")
    
    lines.append("-" * 40)
    lines.append("TOP LANGUAGES")
    for lang, count in languages:
        lines.append(f"{lang}: {count} repos")
        
    lines.append("-" * 40)
    lines.append("CONTRIBUTION GRAPH")
    lines.append(graph_data[0].replace("⬜", "[ ]").replace("🟩", "[1]").replace("🟨", "[2]").replace("🟧", "[3]").replace("🟥", "[4]"))
    
    return "\n".join(lines)
