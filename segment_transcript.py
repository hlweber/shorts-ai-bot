def segment_transcript(segments, max_duration=600):
    """
    Divide os segmentos transcritos (com timestamps) em blocos de até max_duration segundos
    respeitando quebras naturais de fala.
    """
    blocks = []
    current_block = []
    current_duration = 0

    for i, seg in enumerate(segments):
        start = seg["start"]
        end = seg["end"]
        duration = end - start

        current_block.append(seg)
        current_duration += duration

        # Verifica se chegou no tempo-limite ou há uma pausa longa (> 2s)
        next_start = segments[i + 1]["start"] if i + 1 < len(segments) else None
        long_pause = next_start and (next_start - end) >= 2.0

        if current_duration >= max_duration or long_pause:
            blocks.append(current_block)
            current_block = []
            current_duration = 0

    if current_block:
        blocks.append(current_block)

    return blocks

def block_to_text(block):
    """Converte um bloco de segmentos em texto corrido"""
    return " ".join([seg["text"].strip() for seg in block])

def block_start_end(block):
    """Retorna timestamp de início e fim do bloco"""
    return block[0]["start"], block[-1]["end"]
