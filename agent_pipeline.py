import os
from openai import OpenAI
from frame_utils import extract_frames
from transcript_utils import transcribe_audio
from audio_events import detect_audio_events
from prompt_utils import analyze_video_with_gpt
from subtitle_utils import save_srt
from video_cutter import cut_highlight_segments
from post_processing import apply_music_and_overlay
from tracking_utils import log_event
from video_metadata import get_video_metadata
from video_downloader import download_video

def process_video(video_id, video_path=None, output_base="outputs", interval_sec=3,
                  gpt_model="gpt-4o", music_path=None, overlay_img_path=None,
                  max_shorts=5, youtube_api_key=None):

    output_dir = os.path.join(output_base, video_id)
    os.makedirs(output_dir, exist_ok=True)

    log_event(output_dir, {
        "type": "video_start",
        "video_id": video_id,
        "input_video_path": video_path,
    })

    try:
        # Baixar o vídeo se não estiver salvo localmente
        if not video_path or not os.path.exists(video_path):
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_path = os.path.join(output_dir, "original.mp4")
            download_video(video_url, video_path, output_dir=output_dir)

        # Metadados (opcional)
        metadata = None
        if youtube_api_key:
            metadata = get_video_metadata(youtube_api_key, video_id, output_dir)

        # Transcrição
        transcript, segments, language = transcribe_audio(video_path, output_dir)
        save_srt(segments, os.path.join(output_dir, "subtitles.srt"), output_dir=output_dir)

        # Frames + Áudio
        frames = extract_frames(video_path, output_dir, interval_sec=interval_sec)
        audio_events = detect_audio_events(os.path.join(output_dir, "audio.mp3"), output_dir)

        duration = int(segments[-1].end) if segments else 0

        # Análise com GPT
        highlights = analyze_video_with_gpt(
            client=OpenAI(),
            transcript=transcript,
            frames=frames,
            duration_sec=duration,
            audio_events=audio_events,
            output_dir=output_dir,
            model=gpt_model
        )

        # Corte dos Shorts
        cut_highlight_segments(video_path, highlights, output_dir, max_segments=max_shorts)

        # Pós-processamento dos cortes
        shorts_dir = os.path.join(output_dir, "shorts")
        processed_dir = os.path.join(output_dir, "processed")
        os.makedirs(processed_dir, exist_ok=True)

        for f in os.listdir(shorts_dir):
            if f.endswith(".mp4"):
                short_path = os.path.join(shorts_dir, f)
                out_path = os.path.join(processed_dir, f)
                apply_music_and_overlay(
                    short_path,
                    music_path,
                    out_path,
                    output_dir,
                    image_overlay=overlay_img_path
                )

        log_event(output_dir, {
            "type": "video_pipeline_complete",
            "video_id": video_id,
            "highlights_used": len(highlights),
            "shorts_created": len(os.listdir(processed_dir)),
            "language": language,
            "metadata": metadata
        })

    except Exception as e:
        log_event(output_dir, {
            "type": "pipeline_failed",
            "video_id": video_id,
            "error": str(e)
        })
        raise
