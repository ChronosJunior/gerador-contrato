from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_file_id(creds, name, mime_type=""):
    try:
        service = build("drive", "v3", credentials=creds)
        if mime_type=="":
          query=f"name= '{name}'"
        else:
          query=f"name = '{name}' and mimeType = '{mime_type}'"
        results = (
            service.files()
            .list(q=query, pageSize=1, fields="nextPageToken, files(id, name, mimeType)")
            .execute()
        )
        items = results.get("files", [])
        if not items:
            return
        return items[0]['id']
    except HttpError as error:
      raise error

def create_folder(creds, name):
  try:
    service = build("drive", "v3", credentials=creds)
    file_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }

    file = service.files().create(body=file_metadata, fields="id").execute()
    return file.get("id")

  except HttpError as error:
    raise error

def move_file_to_folder(creds, file_id, folder_id):
  try:
    service = build("drive", "v3", credentials=creds)

    file = service.files().get(fileId=file_id, fields="parents").execute()
    if file.get("parents") != None:
      previous_parents = ",".join(file.get("parents"))
    else:
      previous_parents = ""
    file = (
        service.files()
        .update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields="id, parents",
        )
        .execute()
    )
    return file.get("parents")

  except HttpError as error:
    raise error