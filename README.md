# GitHub Commit Notifier

A tiny Flask server that listens for GitHub webhook events (pushes and pull
requests) and prints a clean, formatted notification straight to your
terminal in real time.

Built as a fast, practical extension of a GitHub webhook + ngrok + agent
pipeline — same core wiring, applied to a simpler, instantly demoable use
case.

---

## How it works

1. GitHub sends a `POST` request to this server every time something
   happens on your repo (a push, a pull request opening, etc.).
2. The server reads the JSON payload and pulls out the useful details —
   who pushed, which branch, the commit messages, PR title, and so on.
3. It prints a formatted notification to your terminal the moment the
   event arrives.

```
Repo Event → GitHub Webhook → ngrok tunnel → Flask server → Terminal notification
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
python app.py
```

You should see:

```
Starting GitHub Commit Notifier...
Local URL: http://localhost:5000/webhook
Run 'ngrok http 5000' in another terminal to get a public URL.
```

### 3. Expose it publicly with ngrok

In a separate terminal:

```bash
ngrok http 5000
```

Copy the `https://xxxxx.ngrok-free.app` URL it gives you.

### 4. Add the webhook on GitHub

1. Go to your repository → **Settings** → **Webhooks** → **Add webhook**
2. **Payload URL**: `https://xxxxx.ngrok-free.app/webhook`
3. **Content type**: `application/json`
4. **Which events?**: choose "Just the push event" or "Let me select
   individual events" and check `Pushes` and `Pull requests`
5. Click **Add webhook**

GitHub will immediately send a `ping` event — check your terminal, you
should see:

```
✅ Webhook successfully connected! GitHub sent a ping event.
```

### 5. Test it

Push a commit to the repo (or open a pull request) and watch your
terminal print a formatted notification instantly.

---

## Example output

```
============================================================
🔔 NEW PUSH EVENT — 2026-09-07 14:32:10
============================================================
Repository : Hafsa-Anwar65/github-commit-notifier
Branch     : main
Pushed by  : Hafsa-Anwar65
Commits    : 1
------------------------------------------------------------
  [a1b2c3d] Add error handling to webhook route  (by Hafsa Anwar)
============================================================
```

---

## Project structure

```
github-commit-notifier/
├── app.py              # Flask server + webhook handler
├── requirements.txt    # Dependencies
└── README.md           # This file
```

---

## Possible next steps

- Send notifications to Slack or Discord instead of (or in addition to)
  the terminal
- Store events in a small SQLite log for history
- Add signature verification using GitHub's webhook secret for security
- Extend to handle `issues` or `release` events
