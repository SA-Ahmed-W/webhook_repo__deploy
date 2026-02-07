from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from app.extensions import mongo

health = Blueprint("health", __name__)


@health.route("/")
def index():
    # Send a ping to confirm a successful connection
    try:
        mongo.db.command("ping")
        return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}), 500