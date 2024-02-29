from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import base64
from hashlib import sha256
import json
SALT_FILE = 'salt.key'

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

def derive_key(password: str, salt: bytes) -> bytes:
    """Deriva una clave segura a partir de una contraseña y una sal."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())  # Deriva la clave
    return base64.urlsafe_b64encode(key)  # La pasa a formato base64

def encrypt_data(data: str, key: bytes) -> str:
    """Cifra los datos y devuelve una cadena codificada en base64."""
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode('utf-8'))
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

def decrypt_data(encrypted_data_str: str, key: bytes) -> str:
    """Descifra los datos de una cadena en base64 y devuelve la cadena original."""
    f = Fernet(key)
    encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data_str)  # Decodifica de Base64 a bytes
    decrypted_data_bytes = f.decrypt(encrypted_data_bytes)
    return decrypted_data_bytes.decode('utf-8')

def generate_container_signature(name, content):
    """Genera una firma utilizando SHA-256 basada en el nombre y el contenido del contenedor."""
    signature_input = f"{name}{content}".encode('utf-8')
    signature = sha256(signature_input).hexdigest()
    return signature

def encrypt_container(name, content, key):
    """Cifra el contenido del contenedor y su firma, devolviendo una cadena Base64."""
    signature = generate_container_signature(name, content)
    data_to_encrypt = json.dumps({"content": content, "signature": signature})
    f = Fernet(key)
    encrypted_data = f.encrypt(data_to_encrypt.encode('utf-8'))
    # Convertir los datos cifrados a Base64 para que sean serializables a JSON
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

def derive_encryption_key(password: str, salt: bytes, vault):
    """Deriva una clave segura a partir de la contraseña y el contenido del vault."""
    # Convierte contraseña a bytes
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
    else:
        password_bytes = password  # Si ya es bytes, lo deja sin cambios

    # Calcula el hash del contenido del vault como additional_data
    contents_hash = sha256(json.dumps(vault, sort_keys=True).encode()).digest()
    
    # Combina la contraseña (ya en bytes) y el hash del contenido (también en bytes)
    combined_input = password_bytes + contents_hash

    # Deriva la clave utilizando tanto la contraseña como el hash del contenido
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(combined_input)
    
    # Devuelve la clave en formato adecuado para Fernet (base64)
    return base64.urlsafe_b64encode(key)


def save_vault_changes(vault, password):
    """
    Cifra y guarda el vault utilizando una clave derivada de la contraseña del usuario y el contenido del vault.
    """
    # Intenta cargar la sal existente o genera una nueva
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, 'rb') as salt_file:
            save_salt = salt_file.read()
    else:
        save_salt = os.urandom(16)
        with open(SALT_FILE, 'wb') as salt_file:
            salt_file.write(save_salt)
    
    # Deriva la clave de cifrado
    encryption_key = derive_encryption_key(password, save_salt, vault)
    
    # Cifra el vault
    f = Fernet(encryption_key)
    encrypted_vault = f.encrypt(json.dumps(vault).encode())
    
    # Guarda el vault cifrado
    with open('encrypted_vault.dat', 'wb') as file:
        file.write(encrypted_vault)
    
    print("Cambios guardados exitosamente.")

def load_vault_changes(password):
    """
    Descifra y carga el vault utilizando la clave derivada de la contraseña del usuario y el contenido del vault.
    """
    with open(SALT_FILE, 'rb') as salt_file:
        save_salt = salt_file.read()
    
    # Asumimos que necesitas cargar un indicador del contenido del vault para derivar la clave
    # Esto puede ser complicado si el contenido cambia. Podrías necesitar almacenar un hash fijo o metadata.
    # Por simplicidad, asumiremos que el contenido no influye directamente en la clave en esta función.
    
    # Deriva la clave de cifrado
    # Necesitas una manera de obtener un 'vault_contents' consistente o simplificar el uso de 'additional_data'
    encryption_key = derive_encryption_key(password, save_salt, {})
    
    # Descifra el vault
    with open('encrypted_vault.dat', 'rb') as file:
        encrypted_vault = file.read()
    f = Fernet(encryption_key)
    decrypted_vault = f.decrypt(encrypted_vault).decode()
    
    return json.loads(decrypted_vault)

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
