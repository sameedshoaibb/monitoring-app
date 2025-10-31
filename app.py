import os
import time
import threading
from datetime import datetime
from flask import Flask, render_template, jsonify

# Create Flask app
app = Flask(__name__)

# Simple dictionary to track app state
stats = {
    "start_time": datetime.now(),
    "counter": 0,
    "last_activity": datetime.now(),
    "requests": 0,
    "env": {}
}

# Background worker: runs every 10 seconds
def background_worker():
    while True:
        stats["counter"] += 1
        stats["last_activity"] = datetime.now()
        print(f"[Background] Counter = {stats['counter']}")
        time.sleep(10)

# Start background thread
threading.Thread(target=background_worker, daemon=True).start()

@app.route("/")
def home():
    """Render dashboard page"""
    stats["requests"] += 1
    uptime = datetime.now() - stats["start_time"]

    return render_template(
        "index.html",
        app_name=stats["env"].get("APP_NAME", "SimplePythonApp"),
        stats=stats,
        uptime=str(uptime).split(".")[0],
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route("/api/stats")
def api_stats():
    """Return app stats in JSON"""
    stats["requests"] += 1
    uptime_seconds = (datetime.now() - stats["start_time"]).total_seconds()
    return jsonify({
        "app_name": stats["env"].get("APP_NAME", "SimplePythonApp"),
        "counter": stats["counter"],
        "uptime_seconds": uptime_seconds,
        "requests": stats["requests"],
        "last_activity": stats["last_activity"].isoformat(),
        "current_time": datetime.now().isoformat(),
        "environment": stats["env"].get("ENVIRONMENT", "development"),
        "debug": stats["env"].get("DEBUG", "false")
    })

@app.route("/health")
def health():
    """Basic health check"""
    return jsonify({
        "status": "healthy",
        "time": datetime.now().isoformat(),
        "uptime_seconds": (datetime.now() - stats["start_time"]).total_seconds()
    })

@app.route("/env")
def show_env():
    """Return safe environment variables"""
    stats["requests"] += 1
    safe_env = {k: v for k, v in stats["env"].items()
                if not any(s in k.lower() for s in ["password", "secret", "key", "token"])}
    return jsonify(safe_env)

if __name__ == "__main__":
    stats["env"] = {
        "APP_NAME": os.getenv("APP_NAME", "SimplePythonApp"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
        "PORT": os.getenv("PORT", "8000"),
        "DEBUG": os.getenv("DEBUG", "false")
    }

    port = int(stats["env"]["PORT"])
    debug = stats["env"]["DEBUG"].lower() == "true"

    print(f"🚀 Starting {stats['env']['APP_NAME']} at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
