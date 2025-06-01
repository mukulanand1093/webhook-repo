# webhook-repo

This repository receives GitHub webhook events (from `action-repo`) and stores them in MongoDB. It also provides a minimal UI to poll and display the latest repository actions every 15 seconds.

---

## 📌 Features

* Flask server to receive GitHub webhooks
* MongoDB integration to persist webhook data
* REST API:

  * `POST /webhook` → receive and store webhook event
  * `GET /events` → fetch all events
* Frontend that polls `/events` every 15 seconds

---

## 🧱 MongoDB Schema

Each webhook event is stored with the following fields:

```json
{
  "author": "Travis",
  "event_type": "push",
  "from_branch": "staging",
  "to_branch": "master",
  "timestamp": "2025-06-01T12:00:00Z"
}
```

---

## 🐳 Docker Compose Setup

This repo includes a `docker-compose.yml` to run:

* Flask app
* MongoDB

```bash
docker-compose up --build
```

---

## 🧪 Testing Webhooks

* Run with ngrok or deploy to a public server
* Add webhook URL to GitHub `action-repo` settings
* Trigger actions like `push`, `pull_request`, `merge`

---

## 🌐 UI

* Auto-refreshing frontend
* Polls events every 15 seconds and shows minimal, clean display of activity

---

## 🔗 Pair Repository

[action-repo](https://github.com/your-username/action-repo)
