import os.path
import os
from dotenv import load_dotenv 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def main():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  load_dotenv()
  file_name, mime_type = os.getenv("FILE_NAME"), os.getenv("MIME_TYPE")
  if file_name == None or mime_type == None:
    print("Variáveis de ambiente não encontradas.\nCrie um arquivo .env e configure as variáveis FILE_NAME e MIME_TYPE.")
    return 1
  
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
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
  id = get_file_id(file_name, mime_type)
  print(id)

def get_file_id(name, mime_type):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    try:
        service = build("drive", "v3", credentials=creds)
        query=f"name contains '{name}' and mimeType = '{mime_type}'"
        results = (
            service.files()
            .list(q=query, pageSize=1, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("File not found.")
            return
        return items[0]['id']
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()