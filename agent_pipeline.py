import os
import yt_dlp
from openai import OpenAI
from transcript_utils import transcribe_audio, save_srt
from video_utils import extract_frames, cut_and_format_highlight
from prompt_utils import analyze_video_with_gpt4o
from uploader import upload_short
from audio_events import detect_audio_events
from segment_transcript import segment_transcript, block_to_text, block_start_end
from video_metadata import get_video_metadata
from tracking_utils import *

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def download_video(video_id, output_path):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {"format": "best", "outtmpl": output_path}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

def process_video(video_id):
    video_meta = get_video_metadata(video_id)
    output_dir = make_output_dir(video_id)

    log_event(f"Iniciando processamento do vídeo: {video_meta.get('title', video_id)}", output_dir)

    video_path = download_video(video_id, os.path.join(output_dir, "original.mp4"))

    transcript_text, segments = transcribe_audio(video_path)
    save_transcript(transcript_text, output_dir)
    save_srt(segments, os.path.join(output_dir, "subtitles.srt"))

    audio_events = detect_audio_events(video_path)
    save_audio_events(audio_events, output_dir)

    blocks = segment_transcript(segments, max_duration=600)
    frames = extract_frames(video_path, interval_sec=5)

    all_highlights = []

    for b_idx, block in enumerate(blocks):
        block_text = block_to_text(block)
        start_sec, end_sec = block_start_end(block)
        duration = end_sec - start_sec

        relevant_frames = frames[b_idx*2:(b_idx*2)+10]  # aproximação visual
        highlights = analyze_video_with_gpt4o(client, block_text, relevant_frames, duration, audio_events)

        for i, h in enumerate(highlights):
            highlight_file = f"highlight_{b_idx+1}_{i+1}.mp4"
            output_path = os.path.join(output_dir, highlight_file)

            sound_path = f"sounds/{h['soundtrack'].lower()}.mp3"
            overlay_path = f"overlays/{h['overlay'].strip().lower()}.png"

            cut_and_format_highlight(
                input_path=video_path,
                start_ts=h["start"],
                end_ts=h["end"],
                output_path=output_path,
                subtitle_path=os.path.join(output_dir, "subtitles.srt"),
                soundtrack_path=sound_path if os.path.exists(sound_path) else None,
                overlay_path=overlay_path if os.path.exists(overlay_path) else None
            )

            try:
                url = upload_short(output_path, h["title"], description=h["title"] + " #shorts")
                log_event(f"Upload realizado com sucesso: {url}", output_dir)
            except Exception as e:
                url = None
                log_event(f"Erro no upload: {e}", output_dir)

            h.update({
                "file": highlight_file,
                "youtube_url": url
            })

            all_highlights.append(h)

    save_metadata(video_meta, all_highlights, output_dir)
    append_processed_video(video_id)
    log_event("✅ Processamento concluído.", output_dir)
