import os
import json
from getpass import getpass
import encryption
from encryption import *
import containers
from cryptography.fernet import Fernet
import google_drive_integration
from google_drive_integration import *

DATA_FILE = 'vault.json'
KEY_FILE = 'vault.key'
PASSWORD_FILE = 'password.key'
SALT_FILE = 'salt.key'
TEST_VALUE_FILE = 'test_value.key'

SALT_FILE = 'salt.key'
TEST_VALUE_FILE = 'test_value.key'
TEST_VALUE = b"SecureBoxTest"  # Valor de prueba para cifrar y luego verificar

def initialize_system():
    if not os.path.exists(SALT_FILE) or not os.path.exists(TEST_VALUE_FILE):
        # Configuración inicial
        password = getpass("Establece una contraseña para SecureBox: ")
        password_confirm = getpass("Confirma tu contraseña: ")
        if password != password_confirm:
            print("Las contraseñas no coinciden. Intenta nuevamente.")
            exit()

        salt = os.urandom(16)
        with open(SALT_FILE, 'wb') as salt_file:
            salt_file.write(salt)
        
        key = derive_key(password, salt)
        f = Fernet(key)
        encrypted_test_value = f.encrypt(TEST_VALUE)
        with open(TEST_VALUE_FILE, 'wb') as test_file:
            test_file.write(encrypted_test_value)

        print("Configuración inicial completada.")
    else:
        # Verificación durante los inicios de sesión posteriores
        salt = open(SALT_FILE, 'rb').read()
        password = getpass("Introduce tu contraseña para acceder a SecureBox: ")
        key = derive_key(password, salt)
        if not verify_access(key):
            print("Acceso denegado. La contraseña es incorrecta.")
            exit()
    
    return key

def verify_access(key):
    try:
        with open(TEST_VALUE_FILE, 'rb') as test_file:
            encrypted_test_value = test_file.read()
        f = Fernet(key)
        decrypted_test_value = f.decrypt(encrypted_test_value)
        return decrypted_test_value == TEST_VALUE
    except Exception as e:
        print(f"Acceso denegado. No se pudo verificar la contraseña. {e}")
        return False

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
    
    if verify_access(key):
        print("¡Bienvenido a SecureBox!")
        # Continuar con la lógica del programa
    else:
        print("Acceso denegado. La contraseña es incorrecta.")
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
        print("5. Listar todos los contenedores")
        print("6. Guardar cambios y salir")
        print("7. Subir copia de seguridad a Google Drive")
        print("8. Recuperar copia de seguridad de Google Drive")
        choice = input("Selecciona una opción: ")

        if choice == "1":
            containers.create_container(vault, key)
        elif choice == "2":
            containers.edit_container(vault, key)
        elif choice == "3":
            container_name = input("Introduce el nombre del contenedor que deseas borrar: ")
            containers.delete_container(vault, key, container_name)
        elif choice == "4":
            container_name = input("Introduce el nombre del contenedor que deseas visualizar: ")
            containers.view_container(vault, key, container_name)
        elif choice == "5":
            containers.list_containers(vault)
        elif choice == "6":
            save_vault_changes(vault, key)
            print("Saliendo...")
            exit()
        elif choice == "7":
            try:
                # Autenticar al usuario y obtener el servicio de Google Drive
                service = authenticate_google_drive()
                # Definir el nombre del archivo y el tipo MIME
                file_path = "vault.json"
                mime_type = "application/json"
                # Subir el archivo
                upload_file(service, file_path, mime_type)
            except Exception as e:
                print(f"Error al subir la copia de seguridad: {e}")

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