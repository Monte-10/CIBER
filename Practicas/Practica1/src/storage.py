import json
from encryption import encrypt_data, decrypt_data, generate_key

# Constantes para el nombre del archivo y la contraseña (en un caso real, la contraseña no debería estar hardcodeada)
FILE_NAME = "secure_data.json"
PASSWORD = "mi_super_secreto"

def load_data():
    """Carga y descifra el archivo JSON con los datos de los contenedores."""
    try:
        key, _ = generate_key(PASSWORD)  # Asumimos que el salt no es necesario para este ejemplo
        with open(FILE_NAME, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
            decrypted_data = decrypt_data(encrypted_data, key)
            return json.loads(decrypted_data)
    except FileNotFoundError:
        return {}  # Si el archivo no existe, retorna un diccionario vacío

def save_data(data):
    """Cifra y guarda el archivo JSON con los datos de los contenedores."""
    key, _ = generate_key(PASSWORD)
    encrypted_data = encrypt_data(json.dumps(data), key)
    with open(FILE_NAME, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

# Ejemplo de uso
if __name__ == "__main__":
    # Cargamos los datos existentes (si los hay)
    data = load_data()
    print(f"Datos cargados: {data}")

    # Modificamos los datos (esto es solo un ejemplo)
    data["nuevo_contenedor"] = {"contenido": "información secreta"}

    # Guardamos los datos modificados
    save_data(data)

    # Verificamos que se hayan guardado correctamente
    data = load_data()
    print(f"Datos después de guardar: {data}")
