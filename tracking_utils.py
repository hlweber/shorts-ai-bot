import os
import json
import time
from datetime import datetime

def log_event(output_dir, event_data):
    """
    Salva um evento no arquivo execution_log.json dentro da pasta de saída.
    """
    log_path = os.path.join(output_dir, "execution_log.json")
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log = json.load(f)
    else:
        log = []

    event_data["timestamp"] = datetime.utcnow().isoformat()
    log.append(event_data)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def timed_step(output_dir, step_name):
    """
    Decorador que mede o tempo de execução de uma função e loga o resultado.
    Também registra falhas com mensagem de erro.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                duration = round(time.time() - start, 2)
                log_event(output_dir, {
                    "type": "step_success",
                    "step": step_name,
                    "duration_sec": duration
                })
                return result
            except Exception as e:
                duration = round(time.time() - start, 2)
                log_event(output_dir, {
                    "type": "step_failure",
                    "step": step_name,
                    "duration_sec": duration,
                    "error": str(e)
                })
                raise
        return wrapper
    return decorator
