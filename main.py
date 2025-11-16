import os.path
import os
from dotenv import load_dotenv 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from drive import get_file_id

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def load_credentials():
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
    # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def main():
    creds = load_credentials()
    load_dotenv()
    file_name, mime_type = os.getenv("FILE_NAME"), os.getenv("MIME_TYPE")
    if file_name == None or mime_type == None:
        print("Variáveis de ambiente não encontradas.\nCrie um arquivo .env e configure as variáveis FILE_NAME e MIME_TYPE.")
        return 1

    id = get_file_id(creds, file_name, mime_type)
    if id == None:
        print("Arquivo não encontrado.")
        return 2
    print(id)


if __name__ == "__main__":
    main()