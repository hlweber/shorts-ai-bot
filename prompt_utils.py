import json
import base64
import io
from PIL import Image
from tracking_utils import log_event, timed_step

def image_to_base64(image):
    img = Image.fromarray(image)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()

@timed_step(output_dir=None, step_name="gpt_analysis")
def analyze_video_with_gpt(client, transcript, frames, duration_sec, audio_events, output_dir, model="gpt-4o"):
    """
    Monta o prompt e envia para o modelo GPT, incluindo transcrição, eventos e imagens.
    Loga o envio, a resposta e qualquer falha.
    """
    images_to_send = frames[:3]  # segurança: só 3 imagens
    base64_imgs = [image_to_base64(img) for img in images_to_send]

    messages = [
        {"role": "system", "content": "Você é um editor de vídeos curtos que seleciona os melhores trechos virais de vídeos longos."},
        {"role": "user", "content": f"Transcrição:\n{transcript[:3000]}\n\nEventos de áudio detectados: {audio_events}"}
    ]

    for img in base64_imgs:
        messages.append({
            "role": "user",
            "content": {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img}"}
            }
        })

    log_event(output_dir, {
        "type": "gpt_prompt_sent",
        "model": model,
        "input_tokens_est": len(transcript.split()) + len(audio_events) * 10,
        "frames_sent": len(images_to_send),
        "duration_sec": duration_sec
    })

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        text_response = response.choices[0].message.content
        highlights = json.loads(text_response)
    except Exception as e:
        log_event(output_dir, {
            "type": "gpt_response_failure",
            "error": str(e)
        })
        return []

    log_event(output_dir, {
        "type": "gpt_response_success",
        "highlights_count": len(highlights),
        "preview": str(highlights)[:300]
    })

    return highlights
