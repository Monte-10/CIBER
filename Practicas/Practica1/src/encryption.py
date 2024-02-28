from cryptography.fernet import Fernet
import os
import base64

def generate_key():
    """Genera y retorna una nueva clave de cifrado Fernet."""
    return Fernet.generate_key()

def save_key(key):
    """Guarda la clave de cifrado en 'vault.key'."""
    with open('vault.key', 'wb') as key_file:
        key_file.write(key)
    print("Clave guardada exitosamente.")

def load_key():
    """Carga la clave de cifrado desde 'vault.key'."""
    with open('vault.key', 'rb') as key_file:
        key = key_file.read()
    return key

def encrypt_data(data: str, key: bytes) -> str:
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    encrypted_str = base64.urlsafe_b64encode(encrypted_data).decode()
    print(f"Datos cifrados (base64): {encrypted_str}")
    return encrypted_str

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    bytes_data = base64.urlsafe_b64decode(encrypted_data)
    f = Fernet(key)
    decrypted_data = f.decrypt(bytes_data).decode()
    print(f"Datos descifrados: {decrypted_data}")
    return decrypted_data

# Sección de prueba
if __name__ == "__main__":
    key = generate_key()
    save_key(key)
    loaded_key = load_key()
    test_data = "Este es un texto secreto"
    print(f"Datos originales: {test_data}")
    encrypted_test_data = encrypt_data(test_data, loaded_key)
    decrypted_test_data = decrypt_data(encrypted_test_data, loaded_key)
    assert test_data == decrypted_test_data, "El proceso de cifrado y descifrado no coinciden."
    print("La prueba de cifrado/descifrado fue exitosa.")
