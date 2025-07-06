import os
import ffmpeg
from openai import OpenAI
from tracking_utils import log_event, timed_step

client = OpenAI()

def extract_audio(video_path, audio_path):
    ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True, quiet=True)
    return audio_path

@timed_step(output_dir=None, step_name="transcribe_audio")
def transcribe_audio(video_path, output_dir, model="whisper-1"):
    """
    Extrai o áudio do vídeo e gera transcrição com o modelo Whisper.
    Salva o texto e registra no log.
    """
    audio_path = os.path.join(output_dir, "audio.mp3")
    extract_audio(video_path, audio_path)

    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model=model,
            file=f,
            response_format="verbose_json"
        )

    text = transcript.text
    segments = transcript.segments
    language = transcript.language

    with open(os.path.join(output_dir, "transcript.txt"), "w", encoding="utf-8") as f:
        f.write(text)

    log_event(output_dir, {
        "type": "transcription",
        "language": language,
        "segments": len(segments),
        "length_text": len(text)
    })

    return text, segments, language
