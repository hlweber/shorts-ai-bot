import os
from auto_shorts_bot import run_bot
from uploader import authenticate_youtube, upload_short
import json

# ✅ Configurações
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_IDS = ["UC_x5XG1OV2P6uZZ5FSM9Ttw"]  # Substitua pelos canais desejados
OUTPUT_DIR = "outputs"
MAX_VIDEOS = 1
GPT_MODEL = "gpt-4o"
MUSIC_PATH = "assets/default_music.mp3"
OVERLAY_IMG = "assets/emojis/pop.png"

# ✅ Rodar o pipeline completo
run_bot(
    youtube_api_key=YOUTUBE_API_KEY,
    channel_ids=CHANNEL_IDS,
    base_dir=OUTPUT_DIR,
    max_videos=MAX_VIDEOS,
    gpt_model=GPT_MODEL,
    music_path=MUSIC_PATH,
    overlay_img_path=OVERLAY_IMG,
    youtube_api_key=YOUTUBE_API_KEY
)

# ✅ Upload dos shorts gerados
youtube = authenticate_youtube()

for video_id in os.listdir(OUTPUT_DIR):
    output_path = os.path.join(OUTPUT_DIR, video_id)
    processed_path = os.path.join(output_path, "processed")
    metadata_path = os.path.join(output_path, "_log", "video_metadata.json")

    if not os.path.exists(processed_path) or not os.path.exists(metadata_path):
        continue

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    for fname in os.listdir(processed_path):
        if fname.endswith(".mp4"):
            full_path = os.path.join(processed_path, fname)
            upload_short(youtube, full_path, metadata, output_path)
