import os
from tracking_utils import log_event, timed_step

def format_timestamp(seconds):
    """Converte segundos para timestamp SRT (HH:MM:SS,mmm)"""
    ms = int((seconds % 1) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

@timed_step(output_dir=None, step_name="save_srt")
def save_srt(segments, output_path, output_dir=None):
    """
    Salva legendas no formato SRT a partir dos segmentos transcritos.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for i, s in enumerate(segments, 1):
            try:
                start = format_timestamp(s.start)
                end = format_timestamp(s.end)
                text = s.text.strip().replace("-->", "→")
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
            except Exception as e:
                log_event(output_dir, {
                    "type": "srt_segment_error",
                    "index": i,
                    "error": str(e)
                })

    log_event(output_dir, {
        "type": "srt_saved",
        "path": output_path,
        "segments_count": len(segments)
    })
