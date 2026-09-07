"""
GitHub Commit Notifier
-----------------------
A tiny Flask server that receives GitHub webhook events (push, pull_request)
and prints a clean, formatted notification straight to your terminal.

How it works:
1. GitHub sends a POST request to this server every time a configured
   event happens on your repo (e.g. a push).
2. This server reads the JSON payload and pulls out the useful bits
   (who pushed, which branch, commit messages, etc.).
3. It prints a formatted notification to the terminal in real time.

Run locally with:
    python app.py

Then expose it publicly with ngrok:
    ngrok http 5000

Use the ngrok URL (e.g. https://abcd1234.ngrok-free.app/webhook) as your
GitHub webhook's Payload URL.
"""

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


def print_divider():
    print("=" * 60)


def format_push_event(payload):
    """Pretty-print a GitHub 'push' event."""
    pusher = payload.get("pusher", {}).get("name", "unknown")
    repo_name = payload.get("repository", {}).get("full_name", "unknown-repo")
    branch = payload.get("ref", "unknown-branch").split("/")[-1]
    commits = payload.get("commits", [])

    print_divider()
    print(f"🔔 NEW PUSH EVENT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_divider()
    print(f"Repository : {repo_name}")
    print(f"Branch     : {branch}")
    print(f"Pushed by  : {pusher}")
    print(f"Commits    : {len(commits)}")
    print("-" * 60)

    for commit in commits:
        commit_id = commit.get("id", "")[:7]
        message = commit.get("message", "").splitlines()[0]
        author = commit.get("author", {}).get("name", "unknown")
        print(f"  [{commit_id}] {message}  (by {author})")

    print_divider()
    print()


def format_pull_request_event(payload):
    """Pretty-print a GitHub 'pull_request' event."""
    action = payload.get("action", "unknown")
    pr = payload.get("pull_request", {})
    title = pr.get("title", "unknown")
    number = pr.get("number", "?")
    user = pr.get("user", {}).get("login", "unknown")
    repo_name = payload.get("repository", {}).get("full_name", "unknown-repo")

    print_divider()
    print(f"🔔 PULL REQUEST {action.upper()} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_divider()
    print(f"Repository : {repo_name}")
    print(f"PR #{number}     : {title}")
    print(f"Opened by  : {user}")
    print_divider()
    print()


@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event", "unknown")
    payload = request.get_json(silent=True) or {}

    if event_type == "push":
        format_push_event(payload)
    elif event_type == "pull_request":
        format_pull_request_event(payload)
    elif event_type == "ping":
        print_divider()
        print("✅ Webhook successfully connected! GitHub sent a ping event.")
        print_divider()
        print()
    else:
        print_divider()
        print(f"ℹ️  Received unhandled event type: {event_type}")
        print_divider()
        print()

    return jsonify({"status": "received", "event": event_type}), 200


@app.route("/", methods=["GET"])
def home():
    return "GitHub Commit Notifier is running. Point your webhook to /webhook."


if __name__ == "__main__":
    print("Starting GitHub Commit Notifier...")
    print("Local URL: http://localhost:5000/webhook")
    print("Run 'ngrok http 5000' in another terminal to get a public URL.")
    print()
    app.run(host="0.0.0.0", port=5000, debug=True)
