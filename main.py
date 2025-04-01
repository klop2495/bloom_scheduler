from flask import Flask, request, jsonify
from google_calendar import create_event
from scheduler import check_schedule, current_events
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Bloom Scheduler API is running"

@app.route("/api/bloom/schedule", methods=["POST"])
def schedule():
    data = request.json
    if "events" not in data:
        return jsonify({"error": "Missing 'events' field in request."}), 400

    results = []
    for event in data["events"]:
        result = check_schedule(event)
        results.append({"event": event, "result": result})

    return jsonify({"results": results})

@app.route("/api/bloom/schedule", methods=["GET"])
def schedule_info():
    return jsonify({
        "message": "Current schedule",
        "events": current_events
    })

@app.route("/api/bloom/create", methods=["POST"])
def create_calendar_event():
    data = request.json

    try:
        created = create_event(data)
        return jsonify(created), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
