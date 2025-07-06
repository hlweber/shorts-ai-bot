import os
import ffmpeg
from tracking_utils import log_event, timed_step

@timed_step(output_dir=None, step_name="cut_highlight_segments")
def cut_highlight_segments(video_path, highlights, output_dir, max_segments=5):
    """
    Corta os trechos do vídeo com base nos highlights.
    Salva como short_000.mp4, short_001.mp4, etc.
    """
    shorts_dir = os.path.join(output_dir, "shorts")
    os.makedirs(shorts_dir, exist_ok=True)

    created = 0
    for i, h in enumerate(highlights):
        if "start" not in h or "end" not in h:
            continue

        start = float(h["start"])
        end = float(h["end"])
        duration = end - start

        out_path = os.path.join(shorts_dir, f"short_{i:03}.mp4")
        try:
            ffmpeg.input(video_path, ss=start, t=duration).output(
                out_path,
                vf="scale=720:1280",  # força vertical
                acodec="aac",
                vcodec="libx264",
                preset="ultrafast",
                crf=23
            ).run(overwrite_output=True, quiet=True)

            log_event(output_dir, {
                "type": "short_created",
                "index": i,
                "start": start,
                "end": end,
                "duration": duration,
                "file": out_path
            })
            created += 1
        except Exception as e:
            log_event(output_dir, {
                "type": "short_creation_failed",
                "index": i,
                "start": start,
                "end": end,
                "error": str(e)
            })

        if created >= max_segments:
            break

    return created
