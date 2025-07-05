import librosa
import numpy as np

def detect_audio_events(audio_path, threshold_db=-25.0):
    """Detecta picos de som alto (risos, aplausos, etc)"""
    y, sr = librosa.load(audio_path)
    S = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(S, sr=sr)

    events = []
    for t, rms in zip(times, S):
        db = librosa.amplitude_to_db([rms])[0]
        if db > threshold_db:
            min_sec = int(t)
            timestamp = f"{min_sec//60:02}:{min_sec%60:02}"
            events.append(f"Som alto detectado em {timestamp} (nível {db:.1f} dB)")

    return events
