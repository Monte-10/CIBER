from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import io
import json

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """
    Autentica al usuario con Google Drive y devuelve un objeto de servicio.
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)

    # Esto abrirá un navegador y pedirá al usuario que inicie sesión y autorice la aplicación.
    creds = flow.run_local_server(port=0)

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file(service, file_name, mime_type, folder_id=None):
    """
    Sube un archivo a Google Drive en una carpeta específica.
    """
    file_metadata = {'name': file_name}
    if folder_id:  # Si se proporciona un folder_id, lo usa para definir la carpeta de destino
        file_metadata['parents'] = [folder_id]
    
    media = MediaFileUpload(file_name, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Archivo {file_name} subido exitosamente con el ID: {file.get('id')}")

def find_backup_file(service, file_name='vault.json'):
    """Busca el archivo de copia de seguridad en Google Drive."""
    response = service.files().list(q=f"name='{file_name}'", spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])
    if files:
        return files[0]  # Retorna el primer archivo encontrado
    return None

def download_file(service, file_id, file_path):
    """Descarga el archivo de Google Drive."""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Descarga {int(status.progress() * 100)}%.")
    with open(file_path, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())
    print(f"Archivo descargado en {file_path}.")

def recover_vault(service, file_id, file_path='vault.json'):
    """Recupera el archivo de copia de seguridad y lo guarda en el sistema de archivos local."""
    try:
        # Encontrar el archivo de copia de seguridad por ID y descargarlo
        print(f"Intentando descargar el archivo con ID: {file_id}")
        download_file(service, file_id, file_path)
        print(f"Archivo {file_path} descargado exitosamente.")

        # Ahora, intentar cargar los datos del archivo descargado
        with open(file_path, 'r') as file:
            vault_data = json.load(file)
            print("Datos de vault recuperados exitosamente.")
            return vault_data
    except Exception as e:
        print(f"Error durante la recuperación de la copia de seguridad: {e}")
        return None
