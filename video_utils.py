import cv2
import ffmpeg
import os
from datetime import timedelta

def timestamp_to_seconds(ts):
    """Converte timestamp tipo 'MM:SS' ou 'HH:MM:SS' em segundos"""
    parts = list(map(int, ts.strip().split(":")))
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0

def extract_frames(video_path, interval_sec=3):
    """Extrai frames a cada X segundos"""
    frames = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if i % frame_interval == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(rgb)
        i += 1
    cap.release()
    return frames

def cut_and_format_highlight(input_path, start_ts, end_ts, output_path, subtitle_path=None):
    """Corta o vídeo, aplica crop para 9:16 e insere legendas se houver"""

    start_sec = timestamp_to_seconds(start_ts)
    duration = timestamp_to_seconds(end_ts) - start_sec

    probe = ffmpeg.probe(input_path)
    video_stream = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
    width = int(video_stream["width"])
    height = int(video_stream["height"])

    # Crop central para 9:16
    target_height = height
    target_width = int(height * 9 / 16)
    crop_x = int((width - target_width) / 2)

    filters = [f"crop={target_width}:{target_height}:{crop_x}:0"]
    if subtitle_path:
        filters.append(f"subtitles={subtitle_path}")

    (
        ffmpeg
        .input(input_path, ss=start_sec, t=duration)
        .output(output_path, vf=",".join(filters), vcodec="libx264", acodec="aac")
        .run(overwrite_output=True)
    )
