from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return "yt-dlp server running"

@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return jsonify({"status": "downloaded"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
