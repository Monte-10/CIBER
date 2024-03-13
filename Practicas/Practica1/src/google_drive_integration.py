from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import io
import json

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """
    Esta función autentica al usuario con Google Drive utilizando OAuth 2.0. Usa las credenciales almacenadas en 
    'credentials.json' para solicitar el acceso. Abre una nueva ventana del navegador para que el usuario inicie sesión 
    en su cuenta de Google y autorice a la aplicación a acceder a su Google Drive.

    Returns:
        service (Resource): Un objeto de servicio de la API de Google Drive que se utiliza para hacer solicitudes a la API.
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)

    # Esto abrirá un navegador y pedirá al usuario que inicie sesión y autorice la aplicación.
    creds = flow.run_local_server(port=0)

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file(service, file_name, mime_type, folder_id=None):
    """
    Sube un archivo local a Google Drive. Opcionalmente, permite especificar una carpeta de destino mediante su ID.

    Args:
        service (Resource): El objeto de servicio obtenido de authenticate_google_drive().
        file_name (str): El nombre del archivo local a subir.
        mime_type (str): El tipo MIME del archivo, que indica el formato de archivo.
        folder_id (str, optional): El ID de la carpeta de Google Drive donde se subirá el archivo. None por defecto.

    Prints:
        Un mensaje confirmando la subida exitosa del archivo y su ID en Google Drive.
    """
    file_metadata = {'name': file_name}
    if folder_id:  # Si se proporciona un folder_id, lo usa para definir la carpeta de destino
        file_metadata['parents'] = [folder_id]
    
    media = MediaFileUpload(file_name, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Archivo {file_name} subido exitosamente con el ID: {file.get('id')}")

# Estas funciones corresponden a la lógica de recuperar el vault de Drive, pero dio errores y al final no terminamos de implementarlo, además para que
# fuera cómodo necesitamos manejar tokens lo que hacía la aplicación mucho mas insegura.
def find_backup_file(service, file_name='vault.json'):
    """
    Busca en Google Drive un archivo específico por nombre y devuelve su información si existe.

    Args:
        service (Resource): El objeto de servicio obtenido de authenticate_google_drive().
        file_name (str): El nombre del archivo a buscar en Google Drive.

    Returns:
        dict: Información del primer archivo encontrado que coincide con el nombre dado.
        None: Si no se encuentra ningún archivo.
    """
    response = service.files().list(q=f"name='{file_name}'", spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])
    if files:
        return files[0]  # Retorna el primer archivo encontrado
    return None

def download_file(service, file_id, file_path):
    """
    Descarga un archivo específico de Google Drive y lo guarda en el sistema de archivos local.

    Args:
        service (Resource): El objeto de servicio obtenido de authenticate_google_drive().
        file_id (str): El ID del archivo de Google Drive a descargar.
        file_path (str): La ruta local donde se guardará el archivo descargado.

    Prints:
        El progreso de la descarga y un mensaje confirmando la descarga exitosa del archivo.
    """
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
    """
    Recupera el archivo de copia de seguridad desde Google Drive usando su ID y lo carga en el sistema.

    Args:
        service (Resource): El objeto de servicio obtenido de authenticate_google_drive().
        file_id (str): El ID del archivo de copia de seguridad en Google Drive.
        file_path (str): La ruta local donde se guardará el archivo de copia de seguridad descargado.

    Returns:
        dict: Los datos del vault recuperados si la recuperación fue exitosa.
        None: Si ocurre un error durante el proceso de recuperación.
    """
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
