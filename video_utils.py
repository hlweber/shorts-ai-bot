import ffmpeg
import os

def get_video_duration(video_path):
    """
    Retorna a duração do vídeo em segundos.
    """
    try:
        probe = ffmpeg.probe(video_path)
        duration = float(probe["format"]["duration"])
        return duration
    except Exception as e:
        print(f"Erro ao obter duração do vídeo: {e}")
        return 0.0

def is_vertical(video_path):
    """
    Checa se o vídeo é vertical (ideal para Shorts).
    """
    try:
        probe = ffmpeg.probe(video_path)
        video_streams = [s for s in probe["streams"] if s["codec_type"] == "video"]
        if not video_streams:
            return False
        width = int(video_streams[0]["width"])
        height = int(video_streams[0]["height"])
        return height > width
    except Exception as e:
        print(f"Erro ao checar orientação do vídeo: {e}")
        return False
