import os
import json
from googleapiclient.discovery import build
from tracking_utils import log_event, timed_step

@timed_step(output_dir=None, step_name="fetch_channel_videos")
def fetch_recent_videos(api_key, channel_ids, output_dir, max_results=10):
    """
    Busca os vídeos mais recentes de canais especificados.
    Retorna uma lista de video_ids ainda não processados.
    """
    youtube = build("youtube", "v3", developerKey=api_key)

    processed_file = os.path.join(output_dir, "videos_processados.json")
    if os.path.exists(processed_file):
        with open(processed_file, "r") as f:
            processed_ids = set(json.load(f))
    else:
        processed_ids = set()

    new_video_ids = []

    for channel_id in channel_ids:
        try:
            res = youtube.search().list(
                channelId=channel_id,
                part="id",
                order="date",
                maxResults=max_results
            ).execute()

            for item in res.get("items", []):
                if item["id"]["kind"] != "youtube#video":
                    continue
                video_id = item["id"]["videoId"]
                if video_id not in processed_ids:
                    new_video_ids.append(video_id)
        except Exception as e:
            log_event(output_dir, {
                "type": "channel_fetch_failed",
                "channel_id": channel_id,
                "error": str(e)
            })

    log_event(output_dir, {
        "type": "crawler_results",
        "channels_scanned": len(channel_ids),
        "new_videos_found": len(new_video_ids),
        "new_video_ids": new_video_ids
    })

    return new_video_ids, processed_file, processed_ids

def update_processed_list(video_ids, processed_file, processed_ids):
    """
    Atualiza a lista local de vídeos processados.
    """
    processed_ids.update(video_ids)
    with open(processed_file, "w") as f:
        json.dump(list(processed_ids), f, indent=2)
