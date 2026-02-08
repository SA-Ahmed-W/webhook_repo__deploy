from app.utils.timezone import format_timestamp

def format_event_message(event, timezone="UTC"):
    """Format event into human-readable message with timezone"""
    action = event.get("action")
    author = event.get("author")
    from_branch = event.get("from_branch")
    to_branch = event.get("to_branch")
    
    # Use raw timestamp and format with timezone
    raw_timestamp = event.get("timestamp")
    display_time = format_timestamp(raw_timestamp, timezone)
    
    if action == "PUSH":
        return f'{author} pushed to "{to_branch}" on {display_time}'
    
    elif action == "PULL_REQUEST":
        return f'{author} submitted a pull request from "{from_branch}" to "{to_branch}" on {display_time}'
    
    elif action == "MERGE":
        return f'{author} merged branch "{from_branch}" to "{to_branch}" on {display_time}'
    
    return f"Unknown event by {author}"