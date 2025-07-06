import cv2
import os
from tracking_utils import log_event, timed_step

@timed_step(output_dir=None, step_name="extract_frames")
def extract_frames(video_path, output_dir, interval_sec=3):
    """
    Extrai e salva frames do vídeo a cada X segundos.
    Salva os arquivos em outputs/<video_id>/frames/.
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)

    frame_dir = os.path.join(output_dir, "frames")
    os.makedirs(frame_dir, exist_ok=True)

    i = saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if i % frame_interval == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(rgb)
            path = os.path.join(frame_dir, f"frame_{saved:04}.jpg")
            cv2.imwrite(path, cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
            saved += 1
        i += 1

    cap.release()
    log_event(output_dir, {
        "type": "frames_extracted",
        "count": saved,
        "interval_sec": interval_sec
    })
    return frames
