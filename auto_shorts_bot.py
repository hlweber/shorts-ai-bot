import os
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from youtube_crawler import get_new_videos_from_channels
from agent_pipeline import process_video

PROCESSED_DB = "processed_videos.json"

def load_processed():
    """Carrega lista de vídeos já processados"""
    if os.path.exists(PROCESSED_DB):
        with open(PROCESSED_DB, "r") as f:
            return set(json.load(f))
    return set()

def save_processed(video_ids):
    """Salva lista atualizada de vídeos processados"""
    with open(PROCESSED_DB, "w") as f:
        json.dump(list(video_ids), f)

def daily_job():
    print("🔁 Iniciando rotina diária de geração de Shorts...")
    already_done = load_processed()
    new_videos = get_new_videos_from_channels()

    to_process = [v for v in new_videos if v["video_id"] not in already_done]

    print(f"🎯 {len(to_process)} vídeos novos encontrados.")

    for video in to_process:
        print(f"▶️ Processando: {video['title']}")
        try:
            process_video(video["video_id"])
            already_done.add(video["video_id"])
        except Exception as e:
            print(f"❌ Erro ao processar {video['video_id']}: {e}")

    save_processed(already_done)
    print("✅ Fim do ciclo.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(daily_job, trigger="cron", hour=3)  # Roda todo dia às 03:00
    print("⏰ Scheduler ativo. Ctrl+C para parar.")
    scheduler.start()
