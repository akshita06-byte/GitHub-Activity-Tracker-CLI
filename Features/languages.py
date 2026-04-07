from collections import Counter

def get_top_languages(repos_data):
    if not repos_data:
        return []
    
    language_counts = Counter()
    for repo in repos_data:
        lang = repo.get("language")
        if lang:
            language_counts[lang] += 1
            
    # return top 6
    return language_counts.most_common(6)
