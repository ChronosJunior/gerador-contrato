from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
]

CREDS = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=CREDS)

results = drive_service.files().list(
    pageSize=5,
    fields="files(id, name)"
).execute()

files = results.get("files", [])

print("Arquivos encontrados:")
for f in files:
    print(f"- {f['name']} ({f['id']})")
