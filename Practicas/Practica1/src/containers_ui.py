from tkinter import simpledialog, messagebox
import json
from encryption import encrypt_container, decrypt_data
import storage

def create_container_ui(vault, key, name, content):
    """
    Crea un nuevo contenedor dentro del vault cifrado a través de la interfaz gráfica.
    
    Args:
    - vault (dict): El vault en el que se almacenará el contenedor.
    - key (bytes): La clave de cifrado utilizada para cifrar el contenido del contenedor.
    - name (str): El nombre del nuevo contenedor.
    - content (str): El contenido del nuevo contenedor.
    
    La función cifra el contenido utilizando la clave proporcionada y actualiza el vault
    con el nuevo contenedor cifrado. Posteriormente, guarda los cambios realizados en el almacenamiento.
    """
    encrypted_content = encrypt_container(name, content, key)
    vault[name] = encrypted_content
    storage.save_data(vault, key)

def edit_container_ui(vault, key, name, content):
    """
    Edita el contenido de un contenedor existente en el vault a través de la interfaz gráfica.
    
    Args:
    - vault (dict): El vault que contiene el contenedor a editar.
    - key (bytes): La clave de cifrado utilizada para cifrar el contenido modificado del contenedor.
    - name (str): El nombre del contenedor a editar.
    - content (str): El nuevo contenido del contenedor.
    
    Si el contenedor existe, actualiza su contenido con el nuevo contenido cifrado y guarda los cambios.
    Si no se encuentra el contenedor, muestra un mensaje de error.
    """
    if name in vault:
        encrypted_content = encrypt_container(name, content, key)
        vault[name] = encrypted_content
        storage.save_data(vault, key)
    else:
        messagebox.showerror("Error", "Contenedor no encontrado.")

def delete_container_ui(vault, key, name):
    """
    Elimina un contenedor específico del vault a través de la interfaz gráfica.
    
    Args:
    - vault (dict): El vault del cual se eliminará el contenedor.
    - key (bytes): La clave de cifrado (necesaria para guardar los cambios en el almacenamiento).
    - name (str): El nombre del contenedor a eliminar.
    
    Si el contenedor existe, se elimina del vault y se guardan los cambios.
    Si no se encuentra el contenedor, muestra un mensaje de error.
    """
    if name in vault:
        del vault[name]
        storage.save_data(vault, key)
    else:
        messagebox.showerror("Error", "Contenedor no encontrado.")

def view_container_ui(vault, key, name):
    """
    Muestra el contenido de un contenedor específico del vault a través de la interfaz gráfica.
    
    Args:
    - vault (dict): El vault que contiene el contenedor a visualizar.
    - key (bytes): La clave de cifrado utilizada para descifrar el contenido del contenedor.
    - name (str): El nombre del contenedor cuyo contenido se desea visualizar.
    
    Si el contenedor existe, muestra su contenido descifrado en una ventana de mensaje.
    Si no se encuentra el contenedor, muestra un mensaje de error.
    """
    if name in vault:
        encrypted_data = vault[name]
        decrypted_data = decrypt_data(encrypted_data, key)
        container_data = json.loads(decrypted_data)
        content = container_data["content"]
        messagebox.showinfo("Contenedor", f"Contenido del contenedor '{name}':\n{content}")
    else:
        messagebox.showerror("Error", "Contenedor no encontrado.")

def list_containers_ui(vault):
    """
    Lista todos los nombres de los contenedores existentes en el vault a través de la interfaz gráfica.
    
    Args:
    - vault (dict): El vault del cual se listarán los contenedores.
    
    Muestra los nombres de todos los contenedores disponibles en una ventana de mensaje.
    Si no hay contenedores disponibles, muestra un mensaje informativo.
    """
    if vault:
        containers_list = "\n".join(vault.keys())
        messagebox.showinfo("Contenedores disponibles", containers_list)
    else:
        messagebox.showinfo("Información", "No hay contenedores disponibles.")
