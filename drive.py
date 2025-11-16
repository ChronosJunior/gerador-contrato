from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_file_id(creds, name, mime_type):
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
            return
        return items[0]['id']
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")