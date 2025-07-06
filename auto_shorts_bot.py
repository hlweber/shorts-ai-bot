import os
from agent_pipeline import process_video
from youtube_crawler import fetch_recent_videos, update_processed_list
from tracking_utils import log_event

def run_bot(youtube_api_key, channel_ids, base_dir="outputs", max_videos=2, **kwargs):
    """
    Executa o pipeline completo:
    - Busca vídeos novos
    - Processa cada vídeo
    - Atualiza lista de vídeos já processados
    """
    os.makedirs(base_dir, exist_ok=True)
    output_dir = os.path.join(base_dir, "_log")
    os.makedirs(output_dir, exist_ok=True)

    new_ids, processed_file, processed_ids = fetch_recent_videos(
        api_key=youtube_api_key,
        channel_ids=channel_ids,
        output_dir=output_dir,
        max_results=max_videos
    )

    for video_id in new_ids[:max_videos]:
        try:
            video_path = f"https://www.youtube.com/watch?v={video_id}"
            log_event(output_dir, {
                "type": "start_processing_video",
                "video_id": video_id,
                "source": video_path
            })

            process_video(video_id=video_id, video_path=video_path, output_base=base_dir, **kwargs)

        except Exception as e:
            log_event(output_dir, {
                "type": "video_processing_exception",
                "video_id": video_id,
                "error": str(e)
            })

    update_processed_list(new_ids[:max_videos], processed_file, processed_ids)
