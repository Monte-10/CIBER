from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import os
import base64

def generate_key(password_provided):
    """Genera una clave de cifrado a partir de una contraseña."""
    password = password_provided.encode()  # Convert to type bytes
    salt = os.urandom(16)  # Cambiar por un salt fijo si necesitas desencriptar sin tener el mismo entorno de ejecución
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
    return key, salt

def encrypt_data(data, key):
    """Cifra los datos proporcionados con la clave proporcionada."""
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    """Descifra los datos proporcionados con la clave proporcionada."""
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()

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
