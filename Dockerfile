FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir yt-dlp flask gunicorn

WORKDIR /app
COPY app.py .

EXPOSE 10000
CMD ["gunicorn", "-b", "0.0.0.0:10000", "-w", "2", "--timeout", "120", "app:app"]
