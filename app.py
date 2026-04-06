import os, json, subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET = os.environ.get("API_SECRET", "mysecret123")

@app.route("/")
def home():
    return jsonify({"status": "ok"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/get-url", methods=["POST"])
def get_url():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {SECRET}":
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json() or {}
    video_id = data.get("videoId", "")
    if not video_id:
        return jsonify({"error": "videoId required"}), 400

    try:
        result = subprocess.run(
            ["yt-dlp", "--no-download", "-j", "-f",
             "best[ext=mp4][height<=720]/best[ext=mp4]",
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            return jsonify({"error": result.stderr.strip()[:500]}), 500

        info = json.loads(result.stdout)
        return jsonify({
            "url": info.get("url"),
            "title": info.get("title"),
            "duration": info.get("duration"),
            "quality": info.get("format_note"),
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
