def format_timestamp(dt):
    """Format datetime to required string format: 1st April 2021 - 9:30 PM UTC"""
    day = dt.day
    if 11 <= day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    
    formatted = dt.strftime(f"{day}{suffix} %B %Y - %I:%M %p UTC")
    return formatted