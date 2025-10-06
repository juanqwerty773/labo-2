import pandas as pd
import requests
from google.colab import auth
import gspread
from google.auth import default
import base64

# AUTENTICACIÓN GOOGLE
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# ====== CONFIGURACIÓN ======
SHEET_ID = '1qG4SlZfVzdsCQB-4MVyl1ynYYuH8vZ1ntPSch90F6m0'         # <- Pega aquí tu ID de Google Sheet
GITHUB_TOKEN =        # <- Pega aquí tu token personal de GitHub
GITHUB_REPO = 'juanqwerty773/labo-2'          # <- Ejemplo: juanqwerty773/mi-repo
SUBFOLDER = 'clase5/sheets/'                 # <- Subcarpeta Opcional en GitHub (puedes poner '')

# ====== FUNCIONES ======

def get_file_sha(repo, filename, github_token):
    """Obtiene el SHA del archivo si existe en Github (necesario para sobrescribir)"""
    url = f"https://api.github.com/repos/{repo}/contents/{filename}"
    headers = {"Authorization": f"token {github_token}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()["sha"]
    return None

def upload_csv_to_github(repo, filename, csv_content, github_token):
    """Sube (o sobreescribe) el archivo CSV en GitHub"""
    url = f"https://api.github.com/repos/{repo}/contents/{filename}"
    headers = {"Authorization": f"token {github_token}"}
    csv_bytes = base64.b64encode(csv_content.encode()).decode()
    sha = get_file_sha(repo, filename, github_token)
    payload = {
        "message": f"Subir {filename} desde Google Sheets",
        "content": csv_bytes
    }
    if sha:
        payload["sha"] = sha  # Si existe, lo sobreescribe
    r = requests.put(url, headers=headers, json=payload)
    if r.status_code in [200,201]:
        print(f"{filename} subido correctamente.")
    else:
        print(f"Error subiendo {filename}: {r.json()}")


# ====== EJECUCIÓN PRINCIPAL ======

spreadsheet = gc.open_by_key(SHEET_ID)
worksheets = spreadsheet.worksheets()

for ws in worksheets:
    df = pd.DataFrame(ws.get_all_records())
    csv_content = df.to_csv(index=False)
    # Construye la ruta final del archivo en GitHub
    filename = f"{SUBFOLDER}{ws.title}.csv"
    upload_csv_to_github(GITHUB_REPO, filename, csv_content, GITHUB_TOKEN)
