from flask import Blueprint, jsonify, request
from datetime import datetime, timezone, timedelta
from app.extensions import mongo

events = Blueprint("events", __name__)


@events.route("/")
def get_events():
    try:
        if mongo.db is None:
            return jsonify({"error": "MongoDB not connected", "events": []}), 503
        
        # Get last_seen and validate
        last_seen_str = request.args.get("last_seen")
        query = {}
        
        if last_seen_str:
            try:
                from dateutil import parser
                last_seen = parser.isoparse(last_seen_str)
                query["timestamp"] = {"$gt": last_seen}
            except:
                pass
        
        # Always limit to last 24 hours
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        
        if "timestamp" not in query:
            query["timestamp"] = {"$gt": cutoff}
        
        events_cursor = mongo.db.events.find(query).sort("timestamp", -1).limit(50)
        
        events_list = []
        for event in events_cursor:
            events_list.append({
                "id": str(event["_id"]),
                "request_id": event.get("request_id"),
                "author": event.get("author"),
                "action": event.get("action"),
                "from_branch": event.get("from_branch"),
                "to_branch": event.get("to_branch"),
                "timestamp": event.get("timestamp").isoformat() if event.get("timestamp") else None,
                "display_time": event.get("display_time"),
                "message": format_event_message(event)
            })
        
        return jsonify({
            "events": events_list,
            "count": len(events_list),
            "server_time": datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "events": []}), 500


def format_event_message(event):
    """Format event into human-readable message."""
    action = event.get("action")
    author = event.get("author")
    from_branch = event.get("from_branch")
    to_branch = event.get("to_branch")
    display_time = event.get("display_time", "")
    
    if action == "PUSH":
        return f'{author} pushed to "{to_branch}" on {display_time}'
    
    elif action == "PULL_REQUEST":
        return f'{author} submitted a pull request from "{from_branch}" to "{to_branch}" on {display_time}'
    
    elif action == "MERGE":
        return f'{author} merged branch "{from_branch}" to "{to_branch}" on {display_time}'
    
    return f"Unknown event by {author}"