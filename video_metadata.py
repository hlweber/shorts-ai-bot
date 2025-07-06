from googleapiclient.discovery import build
from tracking_utils import log_event

def get_video_metadata(youtube_api_key, video_id, output_dir):
    """
    Busca metadados do vídeo via API do YouTube.
    """
    try:
        youtube = build("youtube", "v3", developerKey=youtube_api_key)
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        if not response["items"]:
            raise ValueError("Vídeo não encontrado")

        item = response["items"][0]
        snippet = item["snippet"]

        metadata = {
            "title": snippet.get("title"),
            "channel": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "description": snippet.get("description"),
            "tags": snippet.get("tags", []),
            "category_id": snippet.get("categoryId"),
            "duration": item["contentDetails"]["duration"],
            "view_count": item["statistics"].get("viewCount")
        }

        log_event(output_dir, {
            "type": "video_metadata",
            "video_id": video_id,
            "metadata": metadata
        })

        return metadata

    except Exception as e:
        log_event(output_dir, {
            "type": "video_metadata_failed",
            "video_id": video_id,
            "error": str(e)
        })
        return None
