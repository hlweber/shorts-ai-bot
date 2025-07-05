import json
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import isodate

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)

def get_channel_videos(channel_id, max_results=10):
    """Pega os últimos vídeos de um canal"""
    res = YOUTUBE.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        type="video",
        order="date"
    ).execute()

    videos = []
    for item in res["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        videos.append({"video_id": video_id, "title": title})
    return videos

def get_video_duration(video_id):
    """Retorna a duração do vídeo (em segundos)"""
    res = YOUTUBE.videos().list(
        part="contentDetails",
        id=video_id
    ).execute()
    duration = res["items"][0]["contentDetails"]["duration"]
    return isodate.parse_duration(duration).total_seconds()

def get_new_videos_from_channels(channels_file="channels.json"):
    """Retorna vídeos novos e longos (60s+) de todos os canais"""
    with open(channels_file) as f:
        channel_ids = json.load(f)

    all_videos = []
    for channel_id in channel_ids:
        videos = get_channel_videos(channel_id)
        for video in videos:
            duration = get_video_duration(video["video_id"])
            if duration > 60:
                all_videos.append({
                    "video_id": video["video_id"],
                    "title": video["title"],
                    "duration_sec": duration
                })
    return all_videos
