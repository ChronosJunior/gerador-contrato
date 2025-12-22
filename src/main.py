import os.path
import os
from dotenv import load_dotenv 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from drive import get_file_id, create_folder, move_file_to_folder

SCOPES = ["https://www.googleapis.com/auth/drive"]

def load_credentials():
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
  creds = load_credentials()
  load_dotenv()
  dir_name, file_name = os.getenv("DIR_NAME"), os.getenv("FILE_NAME")
  if dir_name == None or file_name == None:
      print("Environment variables not found.\nCreate a .env file and set the FILE_NAME and DIR_NAME vars.")
      return 1
  try:
      file_id = get_file_id(creds, file_name)
      if file_id == None:
        raise Exception("File not found.")
      dir_id = get_file_id(creds, dir_name, "application/vnd.google-apps.folder")
      if dir_id == None:
        print(f"Directory not found.\nCreating a new one with the name: \'{dir_name}\'")
        dir_id = create_folder(creds, dir_name)
      move_file_to_folder(creds, file_id, dir_id)
      print("The file has been successfully moved to the destination directory!")
  except (Exception, HttpError) as error:
      print(f"An error occurred: {error}")
      return 2

if __name__ == "__main__":
  main()