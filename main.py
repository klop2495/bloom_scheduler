from flask import Flask, request, jsonify
from scheduler import check_schedule

app = Flask(__name__)

@app.route("/api/bloom/schedule", methods=["POST"])
def schedule():
    data = request.json
    result = check_schedule(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
