from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Connect to MongoDB using environment variable
client = MongoClient(os.environ["MONGO_URI"])
db = client["webhook_db"]
collection = db["events"]

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    event_type = request.headers.get("X-GitHub-Event")
    payload = {}

    if event_type == "push":
        payload["event_type"] = "push"
        payload["author"] = data["pusher"]["name"]
        payload["to_branch"] = data["ref"].split("/")[-1]
        payload["timestamp"] = datetime.utcnow().isoformat()
    elif event_type == "pull_request":
        payload["event_type"] = "pull_request"
        payload["author"] = data["sender"]["login"]
        payload["from_branch"] = data["pull_request"]["head"]["ref"]
        payload["to_branch"] = data["pull_request"]["base"]["ref"]
        payload["timestamp"] = datetime.utcnow().isoformat()
    elif event_type == "pull_request" and data["action"] == "closed" and data["pull_request"]["merged"]:
        payload["event_type"] = "merge"
        payload["author"] = data["sender"]["login"]
        payload["from_branch"] = data["pull_request"]["head"]["ref"]
        payload["to_branch"] = data["pull_request"]["base"]["ref"]
        payload["timestamp"] = datetime.utcnow().isoformat()
    else:
        return jsonify({"msg": "Unsupported event"}), 400

    collection.insert_one(payload)
    return jsonify({"status": "success"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    results = list(collection.find({}, {"_id": 0}))
    return jsonify(results)
