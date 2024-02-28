from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import os
import base64
from cryptography.fernet import Fernet

def generate_key():
    """Genera y retorna una nueva clave de cifrado Fernet."""
    return Fernet.generate_key()

def save_key(key):
    with open('vault.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    """Carga la clave de cifrado desde 'vault.key'."""
    with open('vault.key', 'rb') as key_file:
        return key_file.read()

def encrypt_data(data: str, key: bytes) -> str:
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())  # Convierte str a bytes y luego cifra
    return base64.urlsafe_b64encode(encrypted_data).decode()  # Convierte bytes cifrados a str base64

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    f = Fernet(key)
    bytes_data = base64.urlsafe_b64decode(encrypted_data)  # Convierte str base64 a bytes
    decrypted_data = f.decrypt(bytes_data)
    return decrypted_data.decode()  # Convierte bytes descifrados a str

# Ejemplo de uso
if __name__ == "__main__":
    password = "mi_super_secreto"  # Esta debería ser la contraseña proporcionada por el usuario
    key, salt = generate_key(password)
    print(f"Key: {key}\nSalt: {salt}")

    data = "Este es un texto secreto"
    encrypted_data = encrypt_data(data, key)
    print(f"Encrypted: {encrypted_data}")

    decrypted_data = decrypt_data(encrypted_data, key)
    print(f"Decrypted: {decrypted_data}")
