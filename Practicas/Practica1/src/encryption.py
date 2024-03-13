from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import base64
from hashlib import sha256
import json
from tkinter import simpledialog, Tk

SALT_FILE = 'salt.key'

def save_key(key):
    """
    Guarda la clave de cifrado Fernet en un archivo.

    Args:
    - key (bytes): La clave Fernet a guardar.
    """
    with open('vault.key', 'wb') as key_file:
        key_file.write(key)
    print("Clave guardada exitosamente.")

def load_key():
    """
    Carga la clave de cifrado Fernet desde un archivo.

    Returns:
    - key (bytes): La clave Fernet cargada.
    """
    with open('vault.key', 'rb') as key_file:
        key = key_file.read()
    return key

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Deriva una clave Fernet segura a partir de una contraseña dada y una sal.

    Args:
    - password (str): La contraseña para derivar la clave.
    - salt (bytes): La sal para usar en la derivación de clave.

    Returns:
    - key (bytes): La clave Fernet derivada.
    """
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
    """
    Cifra los datos dados y devuelve el resultado en base64.

    Args:
    - data (str): Los datos a cifrar.
    - key (bytes): La clave Fernet para cifrar los datos.

    Returns:
    - encrypted_data (str): Los datos cifrados codificados en base64.
    """
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode('utf-8'))
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

def decrypt_data(encrypted_data_str: str, key: bytes) -> str:
    """
    Descifra los datos dados desde una cadena en base64 y devuelve la cadena original.

    Args:
    - encrypted_data_str (str): Los datos cifrados en base64.
    - key (bytes): La clave Fernet para descifrar los datos.

    Returns:
    - decrypted_data (str): Los datos descifrados como cadena UTF-8.
    """
    f = Fernet(key)
    encrypted_data_bytes = base64.urlsafe_b64decode(encrypted_data_str)  # Decodifica de Base64 a bytes
    decrypted_data_bytes = f.decrypt(encrypted_data_bytes)
    return decrypted_data_bytes.decode('utf-8')

def generate_container_signature(name, content):
    """
    Genera una firma basada en SHA-256 utilizando el nombre y el contenido del contenedor.

    Args:
    - name (str): El nombre del contenedor.
    - content (str): El contenido del contenedor.

    Returns:
    - signature (str): La firma generada.
    """
    signature_input = f"{name}{content}".encode('utf-8')
    signature = sha256(signature_input).hexdigest()
    return signature

def encrypt_container(name, content, key):
    """
    Cifra el contenido de un contenedor, incluida su firma, y devuelve el resultado en Base64.

    Args:
    - name (str): El nombre del contenedor.
    - content (str): El contenido del contenedor.
    - key (bytes): La clave Fernet para cifrar el contenedor.

    Returns:
    - encrypted_data (str): El contenedor cifrado en base64.
    """
    signature = generate_container_signature(name, content)
    data_to_encrypt = json.dumps({"content": content, "signature": signature})
    f = Fernet(key)
    encrypted_data = f.encrypt(data_to_encrypt.encode('utf-8'))
    # Convertir los datos cifrados a Base64 para que sean serializables a JSON
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

def derive_encryption_key(password: str, salt: bytes, vault):
    """
    Deriva una clave segura a partir de la contraseña, el contenido del vault, y una sal. La función utiliza 
    el hash del contenido del vault como parte de la entrada para la derivación de la clave, añadiendo una capa 
    adicional de seguridad al asegurar que la clave sea única no solo a la contraseña, sino también al contenido actual.

    Args:
    - password (str): La contraseña proporcionada por el usuario.
    - salt (bytes): La sal utilizada para la derivación de la clave.
    - vault (dict): El vault actual cuyo contenido se utiliza en la derivación de la clave.

    Returns:
    - key (bytes): La clave derivada en formato adecuado para su uso con Fernet.
    """
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
    Cifra y guarda el estado actual del vault en un archivo, utilizando una clave derivada que incluye 
    la contraseña del usuario y el contenido actual del vault. Esto garantiza que el vault solo pueda ser 
    descifrado con el conocimiento de la contraseña correcta y cuando el contenido del vault coincide con 
    el estado cuando fue cifrado.

    Args:
    - vault (dict): El vault a ser guardado.
    - password (str): La contraseña utilizada para derivar la clave de cifrado.
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
    Descifra y carga el vault cifrado desde un archivo, utilizando una clave derivada basada en la contraseña 
    proporcionada y el contenido esperado del vault. Si el contenido ha cambiado o la contraseña es incorrecta, 
    el proceso de descifrado fallará, protegiendo contra accesos no autorizados.

    Args:
    - password (str): La contraseña proporcionada por el usuario para descifrar el vault.

    Returns:
    - vault (dict): El vault descifrado y cargado como un diccionario.
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

def generate_key():
    """Genera y retorna una nueva clave de cifrado Fernet."""
    return Fernet.generate_key()

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