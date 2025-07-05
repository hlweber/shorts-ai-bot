import ffmpeg
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_audio(video_path, audio_path="audio.mp3"):
    ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True, quiet=True)
    return audio_path

def transcribe_audio(video_path):
    """Transcreve áudio com Whisper e retorna texto + segmentos"""
    audio_path = extract_audio(video_path)
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json"
        )
    return transcript["text"], transcript["segments"]

def format_timestamp(seconds):
    """Formata timestamp para padrão SRT: HH:MM:SS,ms"""
    td = round(seconds * 1000)
    ms = td % 1000
    s = (td // 1000) % 60
    m = (td // (1000 * 60)) % 60
    h = td // (1000 * 60 * 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def save_srt(segments, output_path="subtitles.srt"):
    """Salva um arquivo .srt com os segmentos do Whisper"""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, s in enumerate(segments, 1):
            start = format_timestamp(s["start"])
            end = format_timestamp(s["end"])
            text = s["text"].strip().replace("-->", "→")
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
