import os
import ffmpeg
from tracking_utils import log_event, timed_step

@timed_step(output_dir=None, step_name="post_process_short")
def apply_music_and_overlay(short_path, music_path, output_path, output_dir, image_overlay=None):
    """
    Adiciona trilha sonora e opcionalmente uma imagem overlay ao short.
    """
    try:
        input_video = ffmpeg.input(short_path)
        input_audio = ffmpeg.input(music_path)

        filters = []
        if image_overlay:
            filters.append(f"movie={image_overlay}[overlay];[0:v][overlay]overlay=10:10")

        stream = ffmpeg.concat(
            input_video.video.filter_("scale", 720, 1280),
            input_audio.audio,
            v=1, a=1
        )

        if filters:
            stream = stream.filter_multi_output(filters)

        stream.output(output_path, acodec="aac", vcodec="libx264", crf=23, preset="ultrafast").run(overwrite_output=True, quiet=True)

        log_event(output_dir, {
            "type": "post_process_success",
            "input": short_path,
            "music": music_path,
            "output": output_path,
            "overlay": image_overlay
        })

    except Exception as e:
        log_event(output_dir, {
            "type": "post_process_failed",
            "input": short_path,
            "error": str(e)
        })
        raise
