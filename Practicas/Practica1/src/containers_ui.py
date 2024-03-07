from tkinter import simpledialog, messagebox
import json
from encryption import encrypt_container, decrypt_data
import storage

def create_container_ui(vault, key, name, content):
    """
    Crea un nuevo contenedor con el nombre y contenido proporcionados.
    """
    encrypted_content = encrypt_container(name, content, key)
    vault[name] = encrypted_content
    storage.save_data(vault, key)

def edit_container_ui(vault, key, name, content):
    """
    Edita el contenedor existente con el nuevo contenido proporcionado.
    """
    if name in vault:
        encrypted_content = encrypt_container(name, content, key)
        vault[name] = encrypted_content
        storage.save_data(vault, key)
    else:
        messagebox.showerror("Error", "Contenedor no encontrado.")

def delete_container_ui(vault, key, name):
    """
    Elimina el contenedor especificado.
    """
    if name in vault:
        del vault[name]
        storage.save_data(vault, key)
    else:
        messagebox.showerror("Error", "Contenedor no encontrado.")

def view_container_ui(vault, key, name):
    """
    Muestra el contenido del contenedor especificado.
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
    Lista todos los contenedores existentes.
    """
    if vault:
        containers_list = "\n".join(vault.keys())
        messagebox.showinfo("Contenedores disponibles", containers_list)
    else:
        messagebox.showinfo("Información", "No hay contenedores disponibles.")
