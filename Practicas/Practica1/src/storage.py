import json
from encryption import *

def save_data(vault, key):
    """Guarda el archivo JSON con los datos de los contenedores cifrados."""
    try:
        data_str = json.dumps(vault)  # Convierte el vault a una cadena JSON
        encrypted_data_str = encrypt_data(data_str, key)  # Cifra la cadena JSON
        with open("vault.json", 'w') as file:  # Cambia a 'w' para escribir la cadena cifrada
            file.write(encrypted_data_str)  # Escribe los datos cifrados como cadena Base64
    except Exception as e:
        print(f"Error al guardar los datos: {e}")