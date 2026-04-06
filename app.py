from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

API_SECRET = "mysecret123"

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "yt-dlp server running"

@app.route("/download", methods=["POST"])
def download():
    if request.headers.get("Authorization") != API_SECRET:
        return jsonify({"error": "Unauthorized"}), 403

    url = request.json.get("url")
    filename = "video.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'format': 'best',
        'outtmpl': filepath
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return jsonify({
        "status": "success",
        "video_url": f"https://yt-dlp-server-jxvq.onrender.com/video/{filename}"
    })

@app.route("/video/<filename>")
def serve_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
