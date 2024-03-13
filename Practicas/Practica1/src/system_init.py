import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
import base64
from cryptography.fernet import Fernet
from encryption import derive_key, encrypt_data, decrypt_data

SALT_FILE = 'salt.key'
ENCRYPTED_VAULT_FILE = 'encrypted_vault.dat'
DATA_FILE = 'vault.json'
TEST_VALUE_FILE = 'test_value.key'
TEST_VALUE = b"SecureBoxTest"

def initialize_system_gui(parent):
    """
    Inicializa el sistema de seguridad mediante una interfaz gráfica de usuario (GUI), solicitando una contraseña.

    Args:
    - parent: El widget de tkinter que actúa como contenedor padre para los diálogos de entrada y mensajes.

    Returns:
    - La clave derivada a partir de la contraseña introducida, o None si el proceso no se completa satisfactoriamente.
    """
    from tkinter import simpledialog, messagebox
    import os
    from encryption import derive_key, encrypt_data, decrypt_data, Fernet
    
    # Verifica si es la configuración inicial o una verificación posterior
    is_initial_setup = not os.path.exists(SALT_FILE) or not os.path.exists(TEST_VALUE_FILE)

    # Solicita la contraseña
    password = simpledialog.askstring("Contraseña", "Introduce tu contraseña para SecureBox:", parent=parent, show='*')

    # Solicita la confirmación de la contraseña solo si es la configuración inicial
    if is_initial_setup:
        password_confirm = simpledialog.askstring("Confirmar Contraseña", "Confirma tu contraseña:", parent=parent, show='*')
        if password != password_confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden. Intenta nuevamente.", parent=parent)
            return None
    else:
        password_confirm = password  # No es necesario confirmar si no es la configuración inicial
    
    if is_initial_setup:
        # Proceso de configuración inicial
        salt = os.urandom(16)
        with open(SALT_FILE, 'wb') as salt_file:
            salt_file.write(salt)
        
        key = derive_key(password, salt)
        f = Fernet(key)
        encrypted_test_value = f.encrypt(TEST_VALUE)
        with open(TEST_VALUE_FILE, 'wb') as test_file:
            test_file.write(encrypted_test_value)
        
        messagebox.showinfo("Configuración", "Configuración inicial completada.", parent=parent)
    else:
        # Verificación durante los inicios de sesión posteriores
        salt = open(SALT_FILE, 'rb').read()
        key = derive_key(password, salt)
        try:
            with open(TEST_VALUE_FILE, 'rb') as test_file:
                encrypted_test_value = test_file.read()
            f = Fernet(key)
            decrypted_test_value = f.decrypt(encrypted_test_value)
            if decrypted_test_value != TEST_VALUE:
                messagebox.showerror("Error", "Acceso denegado. La contraseña es incorrecta.", parent=parent)
                return None
        except Exception as e:
            messagebox.showerror("Error", "Acceso denegado. No se pudo verificar la contraseña. " + str(e), parent=parent)
            return None
    
    return key


def load_or_create_vault_gui(key, parent):
    """
    Carga el vault cifrado desde un archivo, o crea uno nuevo si no existe o está vacío.

    Args:
    - key: La clave utilizada para cifrar/descifrar el vault.
    - parent: El widget de tkinter que actúa como contenedor padre para los mensajes de error.

    Returns:
    - Un diccionario representando el vault cargado o un nuevo vault vacío, o None si ocurre un error.
    """
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        vault = {}
    else:
        try:
            with open(DATA_FILE, 'rb') as file:
                encrypted_vault = file.read()
            decrypted_vault = decrypt_data(encrypted_vault, key)
            vault = json.loads(decrypted_vault)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", "No se pudo cargar el vault debido a un error: " + str(e), parent=parent)
            return None
    
    return vault

def save_vault_changes(vault, key):
    """
    Cifra y guarda el vault actualizado en un archivo utilizando la clave proporcionada.

    Args:
    - vault: El diccionario que representa el vault a guardar.
    - key: La clave utilizada para cifrar el vault.

    Raises:
    - Muestra un mensaje de error a través de la GUI si ocurre un error durante el guardado.
    """
    try:
        encrypted_vault = encrypt_data(json.dumps(vault), key)
        with open(ENCRYPTED_VAULT_FILE, 'wb') as file:
            file.write(encrypted_vault)
    except Exception as e:
        messagebox.showerror("Error", "Error al guardar cambios en el vault: " + str(e))
