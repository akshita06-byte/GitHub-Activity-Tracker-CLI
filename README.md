<div align="center">
  <h1>📈 GitHub Activity Tracker</h1>
  <p><i>A feature-rich CLI tool to generate beautiful, insightful GitHub profiles right in your favorite terminal.</i></p>
  
  [![Python version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
  [![Rich framework](https://img.shields.io/badge/UI-Rich-magenta.svg)](https://github.com/Textualize/rich)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
</div>

---

## ⚡ Overview

GitHub Activity Tracker turns standard GitHub API data into a highly visual dashboard for your terminal. Easily fetch a user's stats, most used programming languages, contribution streaks, and an interactive GitHub contribution graph without leaving the command line.

## ✨ Key Features

- **📊 Comprehensive Stats**: View followers, following, total stars earned, forks, and public repositories at a glance.
- **💻 Language Insights**: A horizontal bar chart showcasing the developer's top programming languages based on repository usage.
- **🔥 Streak Analytics**: Automatically calculates the user's current push streak, longest historical streak, and total active days.
- **📈 Contribution Graph**: A visual grid mirroring the classic GitHub contribution heatmap. Displays 365 days of data via GraphQL (with a 90-day fallback model for unauthenticated requests).
- **💾 Export Mode**: Easily save generated reports to a plain-text file for simple sharing or archiving.
- **🎨 Beautiful UI**: Powered by `rich`, featuring sleek panels, responsive tables, and elegant colors.

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/github-activity-tracker.git
   cd github-activity-tracker
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Authentication (High Rate Limits & 365-day Graph)**:
   Copy the example environment variables file and insert your GitHub token.
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and replace the placeholder with your 
   [GitHub Personal Access Token](https://github.com/settings/tokens) (Requires `read:user` and `public_repo` scopes).

> **Note**: While the app will run without a token, GitHub REST API rate limits apply more strictly, and the detailed 365-day graph will default to a 90-day event-based approximation.

---

## 🚀 Usage

You can run the script interactively or pass the username directly as an argument.

**Interactive Mode:**
If you run without arguments, the script will prompt you for a username.
```bash
python main.py
```

**Direct Mode:**
Target a specific user immediately using the `--user` flag.
```bash
python main.py --user torvalds
```

**Export Data:**
Want to save a copy? Add the `--export` flag to dump the output into a `{username}_report.txt` file.
```bash
python main.py --user torvalds --export
```

---

## ⚙️ Tech Stack & Architecture

- **Language**: Core Python 3
- **Network**: `requests` for interacting with both the standard REST API and the newer v4 GraphQL API endpoints.
- **Environment**: `python-dotenv` for local `.env` secret management.
- **UI Engine**: `rich` handles drawing tables, panels, bar charts, colors, and progress spinners to `stdout`.

### How it operates internally:
The tracker runs retrievals to the REST API (`/users/`, `/users/.../repos`, `/users/.../events`) and issues a specialized request to the v4 GraphQL endpoint for the calendar block. Data is then efficiently normalized and rendered cleanly on the terminal canvas.
