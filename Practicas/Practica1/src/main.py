# main.py
from getpass import getpass
import os
import auth
import encryption
import storage
import containers
import json
import encryption
from cryptography.fernet import Fernet
from encryption import encrypt_data, decrypt_data
from encryption import load_key

DATA_FILE = 'vault.json'
KEY_FILE = 'vault.key'

def initialize_system():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    if not os.path.exists(DATA_FILE):
        # Asegúrate de que esta sección cifre correctamente los datos iniciales
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
        encrypted_data = encrypt_data('{}', key)
        with open(DATA_FILE, 'wb') as data_file:
            data_file.write(encrypted_data)

def load_or_create_vault(key):
    # Verificar si el archivo del vault existe
    if not os.path.exists(DATA_FILE):
        # Si no existe, crear un nuevo vault vacío y guardarlo
        vault = {}
        encrypted_vault = encrypt_data(json.dumps(vault), key)
        with open(DATA_FILE, 'wb') as file:
            file.write(encrypted_vault)
        return vault
    else:
        # Cargar el vault existente
        with open(DATA_FILE, 'rb') as file:
            encrypted_vault = file.read()
        decrypted_vault = json.loads(decrypt_data(encrypted_vault, key))
        return decrypted_vault


def main():
    initialize_system()
    
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()

    print("Bienvenido a SecureBox")
    password = getpass("Por favor, introduce tu contraseña para acceder: ")
    if not auth.verify_password(password):
        print("Contraseña incorrecta.")
        return

    vault = None  # Inicializa vault aquí
    try:
        vault = load_or_create_vault(key)
        if vault is None:
            print("No se pudo cargar el vault.")
            return
    except Exception as e:
        print(f"Error al manejar el vault: {e}")
        return  # Asegúrate de salir si no se puede cargar el vault


    # Continuar solo si `vault` fue cargado correctamente
    if vault is not None:
        while True:
            print("\nOperaciones disponibles:")
            print("1. Crear contenedor")
            print("2. Editar contenedor")
            print("3. Borrar contenedor")
            print("4. Visualizar contenedor")
            print("5. Salir")
            choice = input("Selecciona una opción: ")

            if choice == "1":
                containers.create_container(vault, key)
            elif choice == "2":
                containers.edit_container(vault, key)
            elif choice == "3":
                containers.delete_container(vault, key)
            elif choice == "4":
                containers.view_container(vault)
            elif choice == "5":
                print("Saliendo...")
                break
            else:
                print("Opción no válida. Por favor, intenta de nuevo.")


if __name__ == "__main__":
    main()
