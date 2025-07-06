import librosa
import numpy as np
from tracking_utils import log_event, timed_step

@timed_step(output_dir=None, step_name="detect_audio_events")
def detect_audio_events(audio_path, output_dir, db_offset=10.0, min_gap_sec=3):
    """
    Detecta eventos de som alto (ex: risos, aplausos) com threshold dinâmico.
    O limiar é a mediana do volume RMS + db_offset.
    """
    y, sr = librosa.load(audio_path)
    rms = librosa.feature.rms(y=y)[0]
    db_series = librosa.amplitude_to_db(rms)
    median_db = np.median(db_series)
    threshold_db = median_db + db_offset

    times = librosa.times_like(rms, sr=sr)
    events = []
    last_event = -min_gap_sec

    for t, db in zip(times, db_series):
        if db > threshold_db and (t - last_event) >= min_gap_sec:
            timestamp = f"{int(t)//60:02}:{int(t)%60:02}"
            events.append({"time": timestamp, "db": db})
            last_event = t

    log_event(output_dir, {
        "type": "audio_events_detected",
        "threshold_db": round(threshold_db, 1),
        "count": len(events),
        "example": events[:5]
    })

    return events
