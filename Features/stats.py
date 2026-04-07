from datetime import datetime

def get_basic_stats(user_data, repos_data):
    if not user_data:
        return {}
    
    total_stars = 0
    total_forks = 0
    total_repos = user_data.get("public_repos", 0)
    
    if repos_data:
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
        total_forks = sum(repo.get("forks_count", 0) for repo in repos_data)
        
    created_at = user_data.get("created_at")
    account_created = ""
    if created_at:
        try:
             account_created = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %Y")
        except ValueError:
             account_created = created_at
             
    name = user_data.get("name")
    if not name:
        name = user_data.get("login", "Unknown")
        
    return {
        "name": name,
        "username": user_data.get("login", "Unknown"),
        "bio": user_data.get("bio", ""),
        "location": user_data.get("location", ""),
        "followers": user_data.get("followers", 0),
        "following": user_data.get("following", 0),
        "public_repos": total_repos,
        "total_stars": total_stars,
        "total_forks": total_forks,
        "account_created": account_created
    }
