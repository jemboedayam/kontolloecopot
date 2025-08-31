import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import random

# Gunakan hanya satu scope untuk list + upload
SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_creds():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def main():
    creds = get_creds()
    try:
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
            .list(pageSize=100, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])
        if not items:
            print("No files found.")
            return
        print("Files:")
        for item in items:
            with open('./folder_id.txt','a') as f:
                f.write(item['id'] + '\n')
            print(f"{item['name']} ({item['id']})")
    except HttpError as error:
        print(f"An error occurred: {error}")

def upload_basic(pdf_path):
    with open('./folder_id.txt') as f:
        ids = [line.strip() for line in f if line.strip()]
    folder_id = random.choice(ids)

    creds = get_creds()
    try:
        service = build("drive", "v3", credentials=creds)
        file_metadata = {"name": os.path.basename(pdf_path)}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaFileUpload(pdf_path, mimetype="application/pdf")
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f'✅ File uploaded successfully. File ID: {file.get("id")}')
        return file.get("id")
    except HttpError as error:
        print(f"❌ An error occurred: {error}")
        return None
