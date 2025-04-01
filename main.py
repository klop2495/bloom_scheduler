from flask import Flask, request, jsonify, abort
from scheduler import check_schedule
import os

app = Flask(__name__)

@app.route("/api/bloom/schedule", methods=["POST"])
def schedule():
    data = request.get_json()
    if not data or "events" not in data:
        abort(400, description="Missing 'events' list in request body.")

    try:
        result = check_schedule(data["events"])
        return jsonify({"results": result})
    except Exception as e:
        abort(400, description=f"Processing error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

