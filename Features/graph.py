from datetime import datetime, timedelta

def get_color(count):
    if count == 0: return "⬜"
    elif 1 <= count <= 2: return "🟩"
    elif 3 <= count <= 5: return "🟨"
    elif 6 <= count <= 9: return "🟧"
    else: return "🟥"

def render_contribution_graph(calendar_data, events_data):
    grid = [[] for _ in range(7)]
    months = [] 
    is_fallback = False
    
    if calendar_data and "weeks" in calendar_data:
        weeks = calendar_data["weeks"]
        for week_idx, week in enumerate(weeks):
            days = week.get("contributionDays", [])
            
            for i in range(7):
                day_data = None
                for d in days:
                    date_obj = datetime.strptime(d["date"], "%Y-%m-%d")
                    if date_obj.weekday() == i:
                        day_data = d
                        if date_obj.day <= 7 and i == 0:
                            months.append((week_idx, date_obj.strftime("%b")))
                        break
                
                if day_data:
                    grid[i].append(get_color(day_data["contributionCount"]))
                else:
                    grid[i].append("  ")
                    
    else:
        is_fallback = True
        today = datetime.utcnow().date()
        start_date = today - timedelta(days=90)
        
        push_counts = {}
        if events_data:
            for event in events_data:
                if event.get("type") == "PushEvent":
                    created_at = event.get("created_at")
                    if created_at:
                        try:
                            date_str = created_at.split("T")[0]
                            push_counts[date_str] = push_counts.get(date_str, 0) + 1
                        except:
                            pass
                            
        curr_date = start_date
        while curr_date.weekday() != 0:
            curr_date -= timedelta(days=1)
            
        week_idx = 0
        while curr_date <= today:
            for i in range(7):
                if curr_date > today or curr_date < start_date:
                    grid[i].append("  ")
                else:
                    count = push_counts.get(curr_date.strftime("%Y-%m-%d"), 0)
                    grid[i].append(get_color(count))
                    
                    if curr_date.day <= 7 and i == 0:
                        months.append((week_idx, curr_date.strftime("%b")))
                
                curr_date += timedelta(days=1)
            week_idx += 1
            
    # Format graph
    header = ["  "] * len(grid[0]) if grid[0] else []
    for week_idx, month_name in months:
        if week_idx < len(header):
            header[week_idx] = month_name[:2]
            
    header_str = "    " + "".join(f"{h:<2}" for h in header) + "\n"
    
    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    body_str = ""
    for i in range(7):
        row_str = "".join(grid[i])
        body_str += f"{day_labels[i]} {row_str}\n"
        
    legend = "⬜ None  🟩 1-2  🟨 3-5  🟧 6-9  🟥 10+"
    
    full_graph = header_str + body_str + "\n" + legend
    return full_graph, is_fallback
