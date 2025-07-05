# 📹 Shorts AI Bot

Agente autônomo que:

- Baixa vídeos de canais do YouTube
- Analisa conteúdo multimodal (áudio, texto e imagem)
- Identifica momentos com potencial viral
- Gera cortes com trilha sonora, overlay e legendas
- Publica automaticamente no YouTube Shorts

---

## 🚀 Funcionalidades

- 🎯 Segmentação inteligente por assunto e tempo
- 🧠 Análise com GPT-4o (OpenAI)
- 🎵 Adição automática de trilha sonora sugerida pela IA
- 😂 Detecção de risadas, sons altos e momentos virais
- 🔤 Geração de legendas automáticas com Whisper
- 📤 Upload automatizado para o YouTube Shorts
- 🧾 Logs, metadados e transcrições salvos para análise futura

---

## 🗂️ Estrutura do Projeto

```
shorts-ai-bot/
├── agent_pipeline.py          # Pipeline principal
├── auto_shorts_bot.py         # Executa o pipeline diariamente
├── youtube_crawler.py         # Encontra novos vídeos por canal
├── transcript_utils.py        # Transcrição com Whisper
├── audio_events.py            # Análise de som
├── video_utils.py             # Corte, resize, trilha, overlay
├── segment_transcript.py      # Quebra lógica de conteúdo por tempo
├── video_metadata.py          # Metadados via YouTube API
├── prompt_utils.py            # Prompt + parser GPT
├── tracking_utils.py          # Logs, metadados, outputs
├── uploader.py                # Upload pro YouTube Shorts
│
├── sounds/                    # Trilhas sonoras locais (ex: meme.mp3)
├── overlays/                  # Stickers PNG (ex: 😂.png, 💥.png)
├── outputs/                   # Um diretório por vídeo analisado
├── channels.json              # Canais que serão monitorados
├── processed_videos.json      # Vídeos já processados
├── requirements.txt           # Dependências Python
├── .env.example               # Configurações de ambiente
└── README.md                  # Este arquivo
```

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/shorts-ai-bot.git
cd shorts-ai-bot
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure variáveis de ambiente

Crie um arquivo `.env` com base no `.env.example`:

```env
OPENAI_API_KEY=sk-...
YOUTUBE_API_KEY=AIza...
```

---

## ▶️ Executando manualmente

```bash
python agent_pipeline.py
```

Para agendar execuções automáticas, use `auto_shorts_bot.py` com `cron` ou `apscheduler`.

---

## 🧪 Exemplo de saída (`outputs/{video_id}/`)

```
outputs/KM2yZt92t9Q/
├── highlight_1.mp4
├── highlight_2.mp4
├── transcript.txt
├── audio_events.txt
├── subtitles.srt
├── metadata.json
├── execution.log
└── original.mp4
```

---

## 🧠 Requisitos

- Conta na [OpenAI](https://platform.openai.com/)
- Chave de API do [YouTube Data API v3](https://console.cloud.google.com/)
- Python 3.9+ com `ffmpeg` instalado no sistema

---

## 🐳 Docker (opcional)

```bash
docker build -t shorts-ai-bot .
docker run --env-file .env shorts-ai-bot
```

---

## 📌 Roadmap

- [ ] Publicação no Instagram (pausado por enquanto)
- [x] Salvamento de metadados
- [x] Análise de áudio (risos, aplausos)
- [x] Escolha de música e stickers por IA
- [x] Logging completo por vídeo
- [ ] Painel de estatísticas (futuro)

---

## 👨‍💻 Autor

Henrique — Data Analyst & Automation Enthusiast  
Feito com ❤️ e GPT-4o

---

### ⚠️ Aviso

Este projeto está em fase experimental e depende de APIs pagas. Use com responsabilidade.
