from datetime import datetime, timedelta

def get_streak(events_data):
    if not events_data:
        return (0, 0, 0)
        
    active_days = set()
    for event in events_data:
        if event.get("type") == "PushEvent":
            created_at = event.get("created_at")
            if created_at:
                try:
                    date_str = created_at.split("T")[0]
                    active_days.add(date_str)
                except Exception:
                    pass
                    
    total_active_days = len(active_days)
    if total_active_days == 0:
        return (0, 0, 0)
        
    sorted_days = sorted(list(active_days), reverse=True)
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    current_streak = 0
    date_to_check = today
    
    if today.strftime("%Y-%m-%d") in active_days:
        current_streak = 1
        date_to_check = yesterday
    elif yesterday.strftime("%Y-%m-%d") in active_days:
        current_streak = 1
        date_to_check = yesterday - timedelta(days=1)
    
    if current_streak > 0:
        while date_to_check.strftime("%Y-%m-%d") in active_days:
            current_streak += 1
            date_to_check -= timedelta(days=1)
            
    longest_streak = 1 if len(active_days) > 0 else 0
    temp_streak = 1
    
    if len(sorted_days) > 1:
        for i in range(len(sorted_days) - 1):
            curr_date = datetime.strptime(sorted_days[i], "%Y-%m-%d").date()
            prev_date = datetime.strptime(sorted_days[i+1], "%Y-%m-%d").date()
            if (curr_date - prev_date).days == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
                
    return (current_streak, total_active_days, longest_streak)
