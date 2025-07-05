import base64
import io
from PIL import Image

def encode_frame_to_base64(frame_rgb):
    """Converte frame RGB em imagem JPEG base64"""
    image = Image.fromarray(frame_rgb)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def analyze_video_with_gpt4o(client, transcript, frames, duration_sec, audio_events=None):
    """Usa GPT-4o para sugerir cortes virais com base em texto + imagem + som"""

    image_payloads = []
    for frame in frames[:10]:  # Envia até 10 frames
        b64 = encode_frame_to_base64(frame)
        image_payloads.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
        })

    audio_clues = "\n".join(audio_events) if audio_events else "Nenhum evento sonoro relevante encontrado."

    messages = [
        {"role": "system", "content": "Você é um editor de vídeos virais especializado em Shorts e Reels."},
        {"role": "user", "content": [
            {"type": "text", "text": f"""Duração do vídeo: {int(duration_sec // 60)} minutos

Transcrição:
{transcript}

Eventos sonoros detectados:
{audio_clues}

Sua tarefa:
- Sugira até 1 corte por minuto de vídeo, com duração de 15 a 60 segundos
- Para cada corte, informe:
  - Início (MM:SS)
  - Fim (MM:SS)
  - Título chamativo
  - Estilo de trilha sonora (ex: meme, épica, suspense)
  - Emoji ou sticker visual (ex: 😂, 💥, 🔥)
"""}
        ] + image_payloads}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=2000
    )

    return extract_highlights_from_response(response.choices[0].message.content)

def extract_highlights_from_response(text):
    """Extrai cortes com trilha sonora e visual sugerido"""
    highlights = []
    blocks = text.strip().split("\n\n")
    for block in blocks:
        item = {"start": None, "end": None, "title": "", "soundtrack": "", "overlay": ""}
        for line in block.strip().split("\n"):
            if "Início:" in line:
                item["start"] = line.split(":", 1)[1].strip()
            elif "Fim:" in line:
                item["end"] = line.split(":", 1)[1].strip()
            elif "Título:" in line:
                item["title"] = line.split(":", 1)[1].strip().strip('"')
            elif "Música:" in line or "Trilha sonora:" in line:
                item["soundtrack"] = line.split(":", 1)[1].strip()
            elif "Sticker:" in line or "Emoji:" in line:
                item["overlay"] = line.split(":", 1)[1].strip()
        if item["start"] and item["end"]:
            highlights.append(item)
    return highlights
