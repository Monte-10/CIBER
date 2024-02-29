import json
from encryption import *

# Constantes para el nombre del archivo y la contraseña (en un caso real, la contraseña no debería estar hardcodeada)
FILE_NAME = "secure_data.json"

def load_data(key):
    """Carga y descifra el archivo JSON con los datos de los contenedores utilizando la clave proporcionada."""
    try:
        with open(FILE_NAME, 'r') as encrypted_file:  # Cambia a 'r' porque los datos cifrados están en base64
            encrypted_data_str = encrypted_file.read()  # Lee los datos cifrados como una cadena base64
        decrypted_data = decrypt_data(encrypted_data_str, key)  # Descifra los datos
        return json.loads(decrypted_data)  # Convierte la cadena descifrada de nuevo a un objeto JSON
    except FileNotFoundError:
        return {}

def save_data(vault, key):
    """Guarda el archivo JSON con los datos de los contenedores cifrados."""
    try:
        data_str = json.dumps(vault)  # Convierte el vault a una cadena JSON
        encrypted_data_str = encrypt_data(data_str, key)  # Cifra la cadena JSON
        with open(FILE_NAME, 'w') as file:  # Cambia a 'w' para escribir la cadena cifrada
            file.write(encrypted_data_str)  # Escribe los datos cifrados como cadena Base64
    except Exception as e:
        print(f"Error al guardar los datos: {e}")