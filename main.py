from flask import Flask, request, jsonify
from scheduler import check_schedule
import os

app = Flask(__name__)

@app.route("/api/bloom/schedule", methods=["POST"])
def schedule():
    data = request.json
    result = check_schedule(data)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

