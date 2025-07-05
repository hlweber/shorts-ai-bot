from googleapiclient.discovery import build
import isodate
import os

def get_video_metadata(video_id):
    api_key = os.getenv("YOUTUBE_API_KEY")
    yt = build("youtube", "v3", developerKey=api_key)
    res = yt.videos().list(
        part="snippet,contentDetails",
        id=video_id
    ).execute()

    if not res["items"]:
        return {}

    info = res["items"][0]
    snippet = info["snippet"]
    duration_iso = info["contentDetails"]["duration"]
    duration_sec = int(isodate.parse_duration(duration_iso).total_seconds())

    return {
        "video_id": video_id,
        "title": snippet["title"],
        "channel": snippet["channelTitle"],
        "description": snippet.get("description", ""),
        "upload_date": snippet["publishedAt"],
        "duration_sec": duration_sec
    }
