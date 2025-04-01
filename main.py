from flask import Flask, request, jsonify
from scheduler import check_schedule, current_events
from google_calendar import add_event_to_calendar
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bloom Scheduler API is running"

@app.route("/api/bloom/schedule", methods=["POST"])
def bloom_schedule():
    data = request.get_json()
    if not data or "events" not in data:
        return jsonify({"error": "No 'events' field provided"}), 400

    results = []
    for event in data["events"]:
        result = check_schedule(event)
        if result["status"] == "confirmed":
            add_event_to_calendar(event)
        results.append({"event": event, "result": result})

    return jsonify({"results": results}), 200

@app.route("/api/bloom/schedule", methods=["GET"])
def schedule_info():
    return jsonify({
        "message": "Current schedule",
        "events": current_events
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
