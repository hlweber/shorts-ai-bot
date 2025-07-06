import os
import json
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from tracking_utils import log_event

def authenticate_youtube():
    """
    Autentica com as credenciais locais da Google (OAuth2).
    Requer token.json e client_secret.json previamente configurados.
    """
    import google_auth_oauthlib.flow
    import googleapiclient.discovery

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes
    )
    creds = flow.run_console()

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
    return youtube

def upload_short(youtube, video_path, metadata, output_dir):
    """
    Sobe um vídeo curto para o YouTube como Shorts, usando metadados dinâmicos.
    """
    try:
        title = metadata.get("title", "Shorts gerado por IA")
        description = metadata.get("description", "Conteúdo gerado automaticamente.")
        tags = metadata.get("tags", [])
        category_id = metadata.get("category_id", "22")

        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": "public",
                "madeForKids": False
            }
        }

        media_file = MediaFileUpload(video_path, chunksize=-1, resumable=True)

        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        )

        response = request.execute()

        log_event(output_dir, {
            "type": "upload_success",
            "video_path": video_path,
            "video_id": response["id"],
            "youtube_url": f"https://youtu.be/{response['id']}"
        })

    except Exception as e:
        log_event(output_dir, {
            "type": "upload_failed",
            "video_path": video_path,
            "error": str(e)
        })
        raise
