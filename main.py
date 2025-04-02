from flask import Flask, request, jsonify
from scheduler import check_schedule, current_events
import os
import json
import base64
import tempfile
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']
GOOGLE_CREDENTIALS_B64 = os.environ.get("GOOGLE_CREDENTIALS_B64")
CALENDAR_ID = "0d99fafbf4dd933f0f27214b0c476cbdd4d5f306c5305226dea75a0159dce950@group.calendar.google.com"
_calendar_service = None

def get_calendar_service():
    global _calendar_service
    if _calendar_service:
        return _calendar_service

    if not GOOGLE_CREDENTIALS_B64:
        raise RuntimeError("Missing GOOGLE_CREDENTIALS_B64 environment variable")

    creds_data = base64.b64decode(GOOGLE_CREDENTIALS_B64)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(creds_data)
        temp_file.flush()
        credentials = service_account.Credentials.from_service_account_file(
            temp_file.name, scopes=SCOPES
        )
        _calendar_service = build('calendar', 'v3', credentials=credentials)
        return _calendar_service

def add_event_to_calendar(event_data, calendar_id=CALENDAR_ID):
    service = get_calendar_service()
    event = {
        'summary': event_data['title'],
        'start': {'dateTime': event_data['start'], 'timeZone': 'Europe/Paris'},
        'end': {'dateTime': event_data['end'], 'timeZone': 'Europe/Paris'},
    }
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print("Создано событие:", created_event.get("id"))
    return created_event

def get_upcoming_events(calendar_id=CALENDAR_ID, max_results=10):
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId=calendar_id,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

@app.route("/api/bloom/schedule", methods=["POST"])
def schedule():
    data = request.json
    if "events" not in data:
        return jsonify({"error": "Missing 'events' field in request."}), 400

    results = []
    check_results = check_schedule(data["events"])

    for event, result in zip(data["events"], check_results):
        if result["status"] == "confirmed":
            added_event = add_event_to_calendar(event)
            result["google_event_id"] = added_event.get("id")
        results.append({"event": event, "result": result})

    return jsonify({"results": results})

@app.route("/api/bloom/schedule", methods=["GET"])
def schedule_info():
    return jsonify({
        "message": "Current schedule",
        "events": current_events
    })

@app.route("/api/bloom/calendar", methods=["GET"])
def calendar_events():
    try:
        events = get_upcoming_events(max_results=10)
        return jsonify({"events": events})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Bloom Scheduler API is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

