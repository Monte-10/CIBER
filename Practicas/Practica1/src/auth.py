from cryptography.fernet import Fernet
import os

# Nombre del archivo donde se guarda la clave de cifrado de la contraseña
PASSWORD_KEY_FILE = 'password.key'
# Nombre del archivo donde se guarda la contraseña cifrada
PASSWORD_FILE = 'password.enc'

def generate_key():
    """Genera una nueva clave de cifrado y la guarda en un archivo."""
    key = Fernet.generate_key()
    with open(PASSWORD_KEY_FILE, 'wb') as file:
        file.write(key)
    return key

def load_key():
    """Carga la clave de cifrado desde un archivo."""
    try:
        with open(PASSWORD_KEY_FILE, 'rb') as file:
            key = file.read()
        return key
    except FileNotFoundError:
        return generate_key()

def encrypt_password(password, key):
    """Cifra la contraseña con la clave dada."""
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    """Descifra la contraseña con la clave dada."""
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def set_password(new_password):
    """Establece una nueva contraseña, cifrándola y guardándola."""
    key = load_key()
    encrypted_password = encrypt_password(new_password, key)
    with open(PASSWORD_FILE, 'wb') as file:
        file.write(encrypted_password)

def verify_password(input_password):
    """Verifica si la contraseña ingresada coincide con la almacenada."""
    key = load_key()
    try:
        with open(PASSWORD_FILE, 'rb') as file:
            encrypted_password = file.read()
        decrypted_password = decrypt_password(encrypted_password, key)
        return input_password == decrypted_password
    except FileNotFoundError:
        # Si no se encuentra el archivo de contraseña, establece la ingresada como nueva contraseña
        set_password(input_password)
        return True

