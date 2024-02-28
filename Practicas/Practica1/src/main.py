import os
import json
from getpass import getpass
import encryption
from encryption import encrypt_data, decrypt_data, load_key, save_key
import containers
from cryptography.fernet import Fernet

DATA_FILE = 'vault.json'
KEY_FILE = 'vault.key'
PASSWORD_FILE = 'password.key'


def initialize_system():
    # Verifica si existe la clave de cifrado, si no, la genera y guarda
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()

    # Si es la primera ejecución, solicita al usuario que establezca una contraseña
    if not os.path.exists(PASSWORD_FILE):
        while True:
            password = getpass("Establece una contraseña para SecureBox: ")
            password_confirm = getpass("Confirma tu contraseña: ")
            if password == password_confirm:
                break
            else:
                print("Las contraseñas no coinciden. Intenta nuevamente.")
        
        # Cifra y guarda la contraseña establecida
        encrypted_password = encrypt_data(password, key)
        with open(PASSWORD_FILE, 'w') as file:  # Guarda como texto la contraseña cifrada
            file.write(encrypted_password)
    
    return key

def verify_password(input_password, key):
    """Verifica que la contraseña ingresada sea correcta."""
    with open(PASSWORD_FILE, 'r') as file:
        encrypted_password = file.read()
    decrypted_password = decrypt_data(encrypted_password, key)
    return input_password == decrypted_password

def save_password(password, key):
    """Cifra y guarda la contraseña."""
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    with open(PASSWORD_FILE, 'wb') as file:
        file.write(encrypted_password)

def load_or_create_vault(key):
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        print("El archivo del vault no existe o está vacío, creando un nuevo vault.")
        return {}
    else:
        try:
            with open(DATA_FILE, 'r') as file:
                encrypted_vault = file.read()
            decrypted_vault = json.loads(decrypt_data(encrypted_vault, key))
            return decrypted_vault
        except Exception as e:
            print(f"No se pudo cargar el vault debido a un error: {e}")
            return None


def main():
    key = initialize_system()
    
    # Intenta verificar la contraseña hasta un máximo de intentos permitidos
    attempts = 3
    for _ in range(attempts):
        password_attempt = getpass("Por favor, introduce tu contraseña para acceder: ")
        if verify_password(password_attempt, key):
            print("Bienvenido a SecureBox")
            break
        else:
            print("Contraseña incorrecta.")
    else:
        print("Número máximo de intentos alcanzado. Acceso denegado.")
        return

    # Carga o crea el vault
    try:
        vault = load_or_create_vault(key)
        if vault is None:
            print("No se pudo cargar el vault correctamente.")
            return
    except Exception as e:
        print(f"Error al manejar el vault: {e}")
        return

    # Interfaz de usuario para la gestión de contenedores dentro del vault
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

        # Guarda cualquier cambio realizado en el vault
        try:
            encrypted_vault = encryption.encrypt_data(json.dumps(vault), key)
            with open(DATA_FILE, 'w') as data_file:
                data_file.write(encrypted_vault)
        except Exception as e:
            print(f"Error al guardar el vault: {e}")

if __name__ == "__main__":
    main()