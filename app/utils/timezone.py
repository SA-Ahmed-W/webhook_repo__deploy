from datetime import datetime, timedelta, timezone

def convert_to_ist(utc_dt):
    """Convert UTC datetime to IST (UTC+5:30)"""
    if utc_dt is None:
        return None
    ist_offset = timedelta(hours=5, minutes=30)
    ist_dt = utc_dt.replace(tzinfo=timezone.utc) + ist_offset
    return ist_dt

def format_timestamp(dt, tz="UTC"):
    """Format datetime to required string format"""
    if dt is None:
        return ""

    if tz.upper() == "IST":
        dt = convert_to_ist(dt)
        tz_suffix = "IST"
    else:
        tz_suffix = "UTC"
    
    day = dt.day
    if 11 <= day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    
    formatted = dt.strftime(f"{day}{suffix} %B %Y - %I:%M %p {tz_suffix}")
    return formatted

def get_cutoff_seconds(window="24h"):
    """Get cutoff timedelta based on window parameter"""
    if window == "15s":
        return timedelta(seconds=15)
    return timedelta(hours=24)  # default