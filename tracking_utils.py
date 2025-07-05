import os
import json
from datetime import datetime

def make_output_dir(video_id):
    out_dir = os.path.join("outputs", video_id)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

def save_transcript(transcript_text, output_dir):
    with open(os.path.join(output_dir, "transcript.txt"), "w", encoding="utf-8") as f:
        f.write(transcript_text)

def save_audio_events(events, output_dir):
    with open(os.path.join(output_dir, "audio_events.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(events))

def save_metadata(video_meta, highlights, output_dir):
    data = {
        **video_meta,
        "processed_at": datetime.utcnow().isoformat(),
        "highlights": highlights
    }
    with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def log_event(message, output_dir):
    log_path = os.path.join(output_dir, "execution.log")
    timestamp = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")

def append_processed_video(video_id):
    DB_PATH = "processed_videos.json"
    try:
        with open(DB_PATH, "r") as f:
            data = json.load(f)
    except:
        data = []

    if video_id not in data:
        data.append(video_id)
        with open(DB_PATH, "w") as f:
            json.dump(data, f)
