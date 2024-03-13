import storage
from encryption import *
import json
from getpass import getpass
from cryptography.fernet import Fernet
from tkinter import simpledialog, messagebox

def create_container(vault, key):
    """
    Crea un nuevo contenedor dentro del vault cifrado.
    
    Args:
    - vault (dict): El vault en el que se almacena el contenedor.
    - key (bytes): La clave de cifrado usada para cifrar el contenedor.
    
    La función solicita al usuario el nombre y contenido del nuevo contenedor,
    cifra esta información usando la clave proporcionada y actualiza el vault
    con el contenedor cifrado. Finalmente, guarda los cambios en el almacenamiento.
    """
    name = input("Nombre del contenedor: ")
    content = input("Contenido del contenedor: ")
    encrypted_content = encrypt_container(name, content, key)
    vault[name] = encrypted_content
    storage.save_data(vault, key)

def edit_container(vault, key):
    """
    Permite editar el contenido de un contenedor existente dentro del vault.
    
    Args:
    - vault (dict): El vault que contiene el contenedor a editar.
    - key (bytes): La clave de cifrado usada para cifrar el contenedor modificado.
    
    Si el contenedor existe, solicita al usuario el nuevo contenido,
    actualiza el contenedor con este contenido cifrado y guarda los cambios.
    De lo contrario, informa que el contenedor no fue encontrado.
    """
    name = input("Nombre del contenedor a editar: ")
    if name in vault:
        content = input("Nuevo contenido del contenedor: ")
        encrypted_content = encrypt_container(name, content, key)
        vault[name] = encrypted_content
        storage.save_data(vault, key)
    else:
        print("Contenedor no encontrado.")

def delete_container(vault, name):
    """
    Elimina un contenedor específico del vault.
    
    Args:
    - vault (dict): El vault del cual se eliminará el contenedor.
    - name (str): El nombre del contenedor a eliminar.
    
    Si el contenedor existe, se elimina del vault y se muestran cambios guardados.
    De lo contrario, se informa que el contenedor no se encontró.
    """
    if name in vault:
        del vault[name]
        print(f"Contenedor '{name}' borrado exitosamente.")
    else:
        print("Contenedor no encontrado.")

def view_container(vault, key, name):
    """
    Muestra el contenido de un contenedor específico dentro del vault.
    
    Args:
    - vault (dict): El vault que contiene el contenedor.
    - key (bytes): La clave de cifrado usada para descifrar el contenedor.
    - name (str): El nombre del contenedor a visualizar.
    
    Si el contenedor existe, descifra y muestra su contenido.
    De lo contrario, informa que el contenedor especificado no existe.
    """
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
    """
    Lista los nombres de todos los contenedores existentes dentro del vault.
    
    Args:
    - vault (dict): El vault del cual listar los contenedores.
    
    Imprime los nombres de todos los contenedores disponibles.
    Si no hay contenedores, informa que no hay contenedores disponibles.
    """
    if vault:
        print("Contenedores disponibles:")
        for name in vault.keys():
            print(f"- {name}")
    else:
        print("No hay contenedores disponibles.")
