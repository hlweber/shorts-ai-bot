import os
import ffmpeg
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_API_SIZE_MB = 25
BITRATE = "64k"

def extract_audio(video_path, audio_path="audio.mp3"):
    """Extrai áudio em baixa taxa para reduzir tamanho e evitar erro 413."""
    print(f"🎧 Extraindo áudio com bitrate {BITRATE}...")
    ffmpeg.input(video_path).output(audio_path, audio_bitrate=BITRATE).run(overwrite_output=True, quiet=True)
    size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"📦 Áudio salvo: {audio_path} ({size_mb:.2f} MB)")
    return audio_path

def transcribe_audio(video_path):
    """Transcreve usando API da OpenAI e salva arquivos. Rejeita se > 25MB."""
    audio_path = extract_audio(video_path)
    size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    
    if size_mb > MAX_API_SIZE_MB:
        raise ValueError(f"❌ Áudio tem {size_mb:.2f} MB — excede o limite de 25MB da API.")

    print("📤 Enviando áudio para a API Whisper...")
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json"
        )

    return transcript.text, transcript.segments

def format_timestamp(seconds):
    """Converte segundos em timestamp padrão SRT."""
    ms = int((seconds - int(seconds)) * 1000)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def save_srt(segments, output_path):
    """Salva arquivo .srt com os segmentos da transcrição."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, s in enumerate(segments, 1):
            start = format_timestamp(s["start"])
            end = format_timestamp(s["end"])
            text = s["text"].strip().replace("-->", "→")
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
