import storage

def create_container():
    name = input("Nombre del contenedor: ")
    content = input("Contenido del contenedor: ")
    # Aquí deberías cifrar el contenido antes de guardarlo
    data = storage.load_data()
    data[name] = content  # Asegúrate de cifrar este contenido
    storage.save_data(data)
    print("Contenedor creado.")

def edit_container():
    name = input("Nombre del contenedor a editar: ")
    data = storage.load_data()
    if name in data:
        content = input("Nuevo contenido del contenedor: ")
        # Aquí deberías cifrar el contenido antes de guardarlo
        data[name] = content  # Asegúrate de cifrar este contenido
        storage.save_data(data)
        print("Contenedor actualizado.")
    else:
        print("Contenedor no encontrado.")

def delete_container():
    name = input("Nombre del contenedor a borrar: ")
    data = storage.load_data()
    if name in data:
        del data[name]
        storage.save_data(data)
        print("Contenedor borrado.")
    else:
        print("Contenedor no encontrado.")

def view_container():
    name = input("Nombre del contenedor a visualizar: ")
    data = storage.load_data()
    if name in data:
        # Aquí deberías descifrar el contenido antes de mostrarlo
        print(f"Contenido: {data[name]}")  # Asegúrate de descifrar este contenido
    else:
        print("Contenedor no encontrado.")
