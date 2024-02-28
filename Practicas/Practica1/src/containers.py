import storage
from encryption import encrypt_data, decrypt_data
import json

def create_container(vault, key):
    name = input("Nombre del contenedor: ")
    content = input("Contenido del contenedor: ")
    encrypted_content = encrypt_data(content, key)
    vault[name] = encrypted_content
    storage.save_data(vault)  # Ajustado para pasar solo el vault

def edit_container(vault, key):
    name = input("Nombre del contenedor a editar: ")
    if name in vault:
        content = input("Nuevo contenido del contenedor: ")
        encrypted_content = encrypt_data(content, key)
        vault[name] = encrypted_content
        storage.save_data(vault)
    else:
        print("Contenedor no encontrado.")

def delete_container(vault, name):
    if name in vault:
        del vault[name]
        storage.save_data(vault)
    else:
        print("Contenedor no encontrado.")

def view_container(vault, key, name):
    if name in vault:
        encrypted_content = vault[name]
        content = decrypt_data(encrypted_content, key)
        print(f"Contenido: {content}")
    else:
        print("Contenedor no encontrado.")