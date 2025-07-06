import yt_dlp
import os
from tracking_utils import log_event

def download_video(video_url, output_path, output_dir=None):
    """
    Faz o download do vídeo do YouTube e salva no caminho especificado.
    Usa yt-dlp com merge de vídeo + áudio.
    """
    try:
        ydl_opts = {
            "outtmpl": output_path,
            "quiet": True,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        if output_dir:
            log_event(output_dir, {
                "type": "download_success",
                "url": video_url,
                "output": output_path
            })

        return output_path

    except Exception as e:
        if output_dir:
            log_event(output_dir, {
                "type": "download_failed",
                "url": video_url,
                "error": str(e)
            })
        raise
