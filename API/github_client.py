import os
import requests
from dotenv import load_dotenv
from rich.console import Console

console = Console()

class GitHubClient:
    def __init__(self, username):
        self.username = username
        self.authenticated = False
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        
        load_dotenv()
        token = os.getenv("GITHUB_TOKEN")
        
        if not token or token == "your_github_personal_access_token_here":
            console.print("[yellow]Warning: GITHUB_TOKEN not found or is a placeholder. Using unauthenticated requests (lower rate limits).[/yellow]")
        else:
            self.headers["Authorization"] = f"bearer {token}"
            self.authenticated = True

    def _get(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error fetching {url}: {e}[/red]")
            return None

    def get_user(self):
        return self._get(f"https://api.github.com/users/{self.username}")

    def get_repos(self):
        return self._get(f"https://api.github.com/users/{self.username}/repos?per_page=100&sort=updated")

    def get_events(self):
        return self._get(f"https://api.github.com/users/{self.username}/events?per_page=100")

    def get_contribution_calendar(self):
        if not self.authenticated:
            return None
        
        query = """
        query($login: String!) {
          user(login: $login) {
            contributionsCollection {
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    date
                    contributionCount
                  }
                }
              }
            }
          }
        }
        """
        
        try:
            response = requests.post(
                "https://api.github.com/graphql",
                json={"query": query, "variables": {"login": self.username}},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            if "errors" in data:
                console.print(f"[red]GraphQL Error: {data['errors']}[/red]")
                return None
            return data.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("contributionCalendar")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error fetching contribution calendar: {e}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]Unexpected error fetching contribution calendar: {e}[/red]")
            return None
