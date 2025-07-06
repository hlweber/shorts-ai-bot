import os
from openai import OpenAI
from frame_utils import extract_frames
from transcript_utils import transcribe_audio
from audio_events import detect_audio_events
from prompt_utils import analyze_video_with_gpt
from tracking_utils import log_event

def process_video(video_id, video_path, output_base="outputs", interval_sec=3, gpt_model="gpt-4o"):
    output_dir = os.path.join(output_base, video_id)
    os.makedirs(output_dir, exist_ok=True)

    log_event(output_dir, {
        "type": "video_start",
        "video_id": video_id,
        "video_path": video_path
    })

    try:
        # Transcrição
        transcript, segments, language = transcribe_audio(video_path, output_dir)

        # Frames e áudio
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

        log_event(output_dir, {
            "type": "video_processed",
            "video_id": video_id,
            "highlights_total": len(highlights),
            "language": language
        })

    except Exception as e:
        log_event(output_dir, {
            "type": "video_processing_failed",
            "video_id": video_id,
            "error": str(e)
        })
        raise
