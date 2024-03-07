import storage
from encryption import *
import json
from getpass import getpass
from cryptography.fernet import Fernet
from tkinter import simpledialog, messagebox

def create_container(vault, key):
    name = input("Nombre del contenedor: ")
    content = input("Contenido del contenedor: ")
    encrypted_content = encrypt_container(name, content, key)
    vault[name] = encrypted_content
    storage.save_data(vault, key)

def edit_container(vault, key):
    name = input("Nombre del contenedor a editar: ")
    if name in vault:
        content = input("Nuevo contenido del contenedor: ")
        encrypted_content = encrypt_container(name, content, key)
        vault[name] = encrypted_content
        storage.save_data(vault, key)
    else:
        print("Contenedor no encontrado.")

def delete_container(vault, name):
    if name in vault:
        del vault[name]
        print(f"Contenedor '{name}' borrado exitosamente.")
    else:
        print("Contenedor no encontrado.")

def view_container(vault, key, name):
    # Verifica si el nombre del contenedor existe en el vault
    if name in vault:
        encrypted_data_base64 = vault[name]
        # Decodifica los datos cifrados de Base64 a bytes
        encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data_base64)
        # Crea una instancia de Fernet con la clave proporcionada
        f = Fernet(key)
        # Descifra los datos
        decrypted_data_bytes = f.decrypt(encrypted_data_bytes)
        # Convierte los datos descifrados a una cadena UTF-8
        decrypted_data = decrypted_data_bytes.decode('utf-8')
        
        # Asume que los datos descifrados son una cadena JSON que contiene "content" y "signature"
        container_data = json.loads(decrypted_data)
        content = container_data["content"]
        
        print(f"Contenido del contenedor '{name}': {content}")
    else:
        print("El contenedor especificado no existe.")
        
def list_containers(vault):
    """Lista todos los nombres de los contenedores existentes."""
    if vault:
        print("Contenedores disponibles:")
        for name in vault.keys():
            print(f"- {name}")
    else:
        print("No hay contenedores disponibles.")
