# GitHub Commit Notifier

A lightweight Flask server that listens for GitHub webhook events (pushes
and pull requests) and prints a clean, formatted notification straight to
your terminal — in real time, with no manual checking required.

```
GitHub Repo Event → GitHub Webhook → Cloudflare Tunnel → Flask Server → Terminal Notification
```

---

## What it does

Every time something happens on a watched GitHub repository — a push, a
pull request opening — GitHub sends an event payload to this server.
The server reads the payload, extracts the useful details (who pushed,
which branch, the commit messages, the PR title), and prints a
formatted notification to the terminal the moment it arrives.

**Example output:**

```
============================================================
🔔 NEW PUSH EVENT — 2026-09-07 14:32:10
============================================================
Repository : your-username/github-commit-notifier
Branch     : main
Pushed by  : your-username
Commits    : 1
------------------------------------------------------------
  [a1b2c3d] Add error handling to webhook route  (by Your Name)
============================================================
```

---

## Tech stack

| Component | Purpose |
|---|---|
| **Python + Flask** | Receives and parses incoming webhook payloads |
| **GitHub Webhooks** | Sends event data (push, pull_request, ping) whenever something happens on the repo |
| **Cloudflare Tunnel** | Exposes the local Flask server to the public internet, since GitHub can't reach `localhost` directly |

---

## Getting started

### Prerequisites

- Python 3.8+
- A GitHub repository you have admin access to (to add a webhook)
- [cloudflared](https://github.com/cloudflare/cloudflared/releases/latest) — Cloudflare's tunnel tool (no account required for quick tunnels)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/github-commit-notifier.git
cd github-commit-notifier
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
python app.py
```

You should see:

```
Starting GitHub Commit Notifier...
Local URL: http://localhost:5000/webhook
```

Leave this terminal running.

### 4. Start a Cloudflare Tunnel

In a **separate** terminal, from the same folder:

```bash
cloudflared tunnel --url http://localhost:5000
```

Cloudflare will print a public URL that looks like:

```
https://your-random-subdomain.trycloudflare.com
```

Copy it — this is what GitHub will send events to. Leave this terminal
running too.

> **Note:** Free "quick tunnels" generate a new URL every time you
> restart `cloudflared`. If you restart it, you'll need to update the
> webhook URL on GitHub to match.

### 5. Add the webhook on GitHub

1. Go to your repository → **Settings** → **Webhooks** → **Add webhook**
2. **Payload URL**: your Cloudflare URL + `/webhook`, e.g.
   `https://your-random-subdomain.trycloudflare.com/webhook`
3. **Content type**: `application/json`
4. **Which events?**: select **Pushes** and **Pull requests**
   (or "Send me everything" if you want to see all event types)
5. Click **Add webhook**

GitHub immediately sends a test `ping` event. Check your `python app.py`
terminal — you should see:

```
✅ Webhook successfully connected! GitHub sent a ping event.
```

### 6. Test it

Push a commit (or open a pull request) on the repository. Watch your
terminal — a formatted notification should print the moment the event
arrives on GitHub's end.

---

## Project structure

```
github-commit-notifier/
├── app.py              # Flask server + webhook event handler
├── requirements.txt    # Python dependencies
├── .gitignore           # Keeps local environment files out of the repo
└── README.md            # This file
```

---

## Troubleshooting

| Problem | Likely cause |
|---|---|
| Nothing prints in the terminal | The Payload URL is missing `/webhook` at the end, or the Cloudflare Tunnel URL changed after a restart and GitHub is still using the old one |
| `405` error in GitHub's delivery log | Same as above — the request landed on `/` instead of `/webhook` |
| `ModuleNotFoundError: No module named 'flask'` | Dependencies weren't installed in the Python environment actually running the script — try `python -m pip install -r requirements.txt` |
| Cloudflare Tunnel won't start | Make sure `python app.py` is already running first — the tunnel needs something on port 5000 to connect to |

---

## Possible next steps

- Send notifications to Slack or Discord instead of (or alongside) the terminal
- Log events to a small SQLite database for history
- Verify GitHub's webhook signature for added security
- Extend to handle additional event types like `issues` or `release`

---

## Why I built this

This started as a way to understand how GitHub webhooks, tunnels, and a
receiving server actually connect end to end — not just in theory, but
wired together and tested with a real push event. It's a small project,
but every piece of it (the webhook, the tunnel, the parsing logic) is
something I set up and debugged myself.
