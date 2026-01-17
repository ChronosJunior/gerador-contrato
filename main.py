import os
import io
from datetime import datetime

from googleapiclient.http import MediaIoBaseUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SPREADSHEET_ID = "1gy5BxyFmntyjSHxWfaxx1T6k8RqI8NMFOymGqmNq2TU"
SHEET_NAME = "Dados"

TEMPLATE_DOC_ID = "1CN0blp4tS5rs9kzBCERWA0KFoISQFjWtaFeVR-9on20"
PASTA_VOLUNTARIOS_ID = "1HDZpuk2voO5P2-oCFZSt8K3ylwGZP04j"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents"
]

CONFIG = {
    "CNPJ_CHRONOS": "43.262.002/0001-61",
    "ENDERECO_CHRONOS": "Avenida Araújo Pinho, nº 39, Canela, CEP 40110-150, Salvador, Bahia",

    "NOME_PRESIDENTE": "NOME DA PRESIDENTE",
    "CPF_PRESIDENTE": "000.000.000-00",
    "RG_PRESIDENTE": "0000000",
    "UF_PRESIDENTE": "BA",

    "NOME_DIRETOR": "NOME DO DIRETOR DA DGG",
    "CPF_DIRETOR": "000.000.000-00",
    "RG_DIRETOR": "0000000",
    "UF_DIRETOR": "BA",

    "FORO": "Salvador",
    "CIDADE_ASSINATURA": "Salvador"
}


def autenticar():
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


def ler_planilha(sheets_service):
    range_ = f"{SHEET_NAME}!A2:O"
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_
    ).execute()

    return result.get("values", [])


def processar_voluntario(linha, drive, docs):
    voluntario = {
        "NOME": linha[0],
        "RG": linha[1],
        "CPF": linha[2],
        "UF": linha[3],
        "MES_INGRESSO": linha[4],
        "ANO_INGRESSO": linha[5],
        "RUA": linha[6],
        "NUMERO": linha[7],
        "BAIRRO": linha[8],
        "CIDADE": linha[9],
        "CEP": linha[11],
        "NACIONALIDADE": linha[12],
        "CIVIL": linha[13],
        "OCUPACAO": linha[14],
    }

    data_ingresso = f"{voluntario['MES_INGRESSO']} de {voluntario['ANO_INGRESSO']}"

    copia = drive.files().copy(
        fileId=TEMPLATE_DOC_ID,
        body={"name": f"TEMP_{voluntario['NOME']}"}
    ).execute()

    doc_id = copia["id"]

    requests = []

    for key, value in voluntario.items():
        requests.append({
            "replaceAllText": {
                "containsText": {
                    "text": f"{{{{{key}}}}}",
                    "matchCase": True
                },
                "replaceText": value
            }
        })

    requests.append({
        "replaceAllText": {
            "containsText": {"text": "{{DATA_INGRESSO}}", "matchCase": True},
            "replaceText": data_ingresso
        }
    })

    for key, value in CONFIG.items():
        requests.append({
            "replaceAllText": {
                "containsText": {
                    "text": f"{{{{{key}}}}}",
                    "matchCase": True
                },
                "replaceText": value
            }
        })

    hoje = datetime.now().strftime("%d de %B de %Y")
    requests.append({
        "replaceAllText": {
            "containsText": {"text": "{{DATA_ASSINATURA}}", "matchCase": True},
            "replaceText": hoje
        }
    })

    docs.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": requests}
    ).execute()

    pasta = drive.files().create(
        body={
            "name": voluntario["NOME"],
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [PASTA_VOLUNTARIOS_ID]
        }
    ).execute()

    pasta_id = pasta["id"]

    pdf = drive.files().export(
        fileId=doc_id,
        mimeType="application/pdf"
    ).execute()

    media = MediaIoBaseUpload(
        io.BytesIO(pdf),
        mimetype="application/pdf",
        resumable=False
    )

    drive.files().create(
        body={
            "name": f"Termo de Voluntariado - {voluntario['NOME']}.pdf",
            "parents": [pasta_id]
        },
        media_body=media,
        fields="id"
    ).execute()

    drive.files().delete(fileId=doc_id).execute()


def main():
    creds = autenticar()

    sheets = build("sheets", "v4", credentials=creds)
    drive = build("drive", "v3", credentials=creds)
    docs = build("docs", "v1", credentials=creds)

    linhas = ler_planilha(sheets)

    for linha in linhas:
        if not linha or not linha[0]:
            continue
        processar_voluntario(linha, drive, docs)

    print("PDFs gerados com sucesso.")


if __name__ == "__main__":
    main()