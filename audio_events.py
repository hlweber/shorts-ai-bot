import librosa
import numpy as np

def detect_audio_events(audio_path, db_offset=10.0, min_gap_sec=3):
    """
    Detecta eventos de som alto (potencialmente risadas/aplausos),
    usando threshold adaptativo baseado na mediana.
    """
    y, sr = librosa.load(audio_path)
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(rms, sr=sr)

    # Converte todo o RMS para dB
    db_series = librosa.amplitude_to_db(rms)

    # Define threshold como mediana + offset
    median_db = np.median(db_series)
    threshold_db = median_db + db_offset
    print(f"🔊 Threshold dinâmico definido em {threshold_db:.1f} dB (mediana {median_db:.1f} dB)")

    events = []
    last_event_time = -min_gap_sec

    for t, db in zip(times, db_series):
        if db > threshold_db and (t - last_event_time) >= min_gap_sec:
            min_sec = int(t)
            timestamp = f"{min_sec//60:02}:{min_sec%60:02}"
            events.append({
                "time": timestamp,
                "db": db,
                "description": f"🌟 Som alto detectado em {timestamp} (~{db:.1f} dB)"
            })
            last_event_time = t

    return events
