from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from app.extensions import mongo
from app.libs.logger import get_logger
from app.utils.timezone import format_timestamp, get_cutoff_seconds
from .utils import format_event_message

logger = get_logger()
events = Blueprint("events", __name__)


@events.route("/")
def get_events():
    try:
        if mongo.db is None:
            logger.warning("MongoDB not connected")
            return jsonify({"error": "MongoDB not connected", "events": []}), 503
        
        # Get query parameters
        last_seen_str = request.args.get("last_seen")
        timezone_param = request.args.get("timezone", "UTC").upper()
        window_param = request.args.get("window", "24h")
        
        logger.debug("Request params: timezone=%s, window=%s", timezone_param, window_param)
        
        query = {}
        
        # Set cutoff based on window (15s or 24h)
        cutoff_delta = get_cutoff_seconds(window_param)
        cutoff = datetime.now(timezone.utc) - cutoff_delta
        
        # Handle last_seen for polling
        if last_seen_str:
            try:
                from dateutil import parser
                last_seen = parser.isoparse(last_seen_str)
                
                if last_seen.tzinfo is None:
                    last_seen = last_seen.replace(tzinfo=timezone.utc)
                else:
                    last_seen = last_seen.astimezone(timezone.utc)

                effective_cutoff = max(last_seen, cutoff)
                query["timestamp"] = {"$gt": effective_cutoff}
                
            except Exception as e:
                logger.warning("Invalid last_seen format: %s", e)
                # Fallback to just cutoff
                query["timestamp"] = {"$gt": cutoff}
        else:
            # No last_seen, use cutoff only
            query["timestamp"] = {"$gt": cutoff}
        
        events_cursor = mongo.db.events.find(query).sort("timestamp", -1).limit(50)
        
        events_list = []
        for event in events_cursor:
            raw_timestamp = event.get("timestamp")
            
            # Format display_time based on requested timezone
            display_time = format_timestamp(raw_timestamp, timezone_param)
            
            events_list.append({
                "id": str(event["_id"]),
                "request_id": event.get("request_id"),
                "author": event.get("author"),
                "action": event.get("action"),
                "from_branch": event.get("from_branch"),
                "to_branch": event.get("to_branch"),
                "timestamp": raw_timestamp.isoformat() if raw_timestamp else None,
                "display_time": display_time,
                "message": format_event_message(event, timezone_param)
            })

        logger.debug("Fetched %d events with window=%s", len(events_list), window_param)
        
        return jsonify({
            "events": events_list,
            "count": len(events_list),
            "timezone": timezone_param,
            "window": window_param,
            "server_time": datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        logger.exception("Error fetching events")
        return jsonify({"error": str(e), "events": []}), 500