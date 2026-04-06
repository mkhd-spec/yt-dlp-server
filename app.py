from flask import Flask, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)

API_SECRET = "mysecret123"

@app.route("/")
def home():
    return "yt-dlp server running"

@app.route("/download", methods=["POST"])
def download():
    # 🔒 check secret
    if request.headers.get("Authorization") != API_SECRET:
        return jsonify({"error": "Unauthorized"}), 403

    url = request.json.get("url")
    filename = "video.mp4"

    ydl_opts = {
        'format': 'best',
        'outtmpl': filename
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
