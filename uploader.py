import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Escopos exigidos para upload
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CLIENT_SECRET_FILE = "client_secret.json"
CREDENTIALS_FILE = "youtube_token.pkl"

def get_authenticated_service():
    """Autentica e retorna serviço da YouTube API"""
    creds = None

    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "rb") as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=8080)
        with open(CREDENTIALS_FILE, "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def upload_short(video_path, title, description="#shorts", privacy_status="public"):
    """Faz upload do vídeo como um Short no YouTube"""

    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["shorts"],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"⬆️ Upload em andamento: {int(status.progress() * 100)}%")

    video_id = response["id"]
    print(f"✅ Upload completo! Vídeo: https://youtu.be/{video_id}")
    return f"https://youtu.be/{video_id}"
