# main.py
from getpass import getpass
import os
import auth
import encryption
import storage
import containers
import json

DATA_FILE = 'vault.json'
KEY_FILE = 'vault.key'

def initialize_system():
    """Inicializa el sistema comprobando si existe una clave de cifrado y la base de datos. Si no, los crea."""
    if not os.path.exists(KEY_FILE):
        key = encryption.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        # Aquí deberíamos asegurarnos de que el archivo esté cifrado correctamente desde el inicio
        storage.save_data(encryption.encrypt_data(key, '{}'))  # Guarda un JSON vacío cifrado como inicio.

def load_or_create_vault(key):
    """Carga o crea el vault de contenedores."""
    encrypted_data = storage.load_data()
    if encrypted_data is None:
        return {}
    try:
        decrypted_data = encryption.decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)
    except Exception as e:
        print(f"Error al descifrar el vault: {e}")
        return None

def main():
    initialize_system()
    
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read()

    print("Bienvenido a SecureBox")
    password = getpass("Por favor, introduce tu contraseña para acceder: ")
    if not auth.verify_password(password):
        print("Contraseña incorrecta.")
        return

    vault = load_or_create_vault(key)
    if vault is None:
        print("No se pudo cargar el vault.")
        return

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
