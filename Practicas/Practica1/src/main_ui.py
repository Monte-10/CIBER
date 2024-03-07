import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import encryption
import containers
import google_drive_integration as gdrive
import system_init as sysinit
import containers_ui

class SecureBoxUI:
    def __init__(self, master):
        self.master = master
        master.title("SecureBox")
        
        # Inicializa la clave de cifrado
        self.key = sysinit.initialize_system_gui(master)
        if self.key is None:
            master.quit()  # Salir si la inicialización falla
            return

        self.vault = sysinit.load_or_create_vault_gui(self.key, master)
        if self.vault is None:
            master.quit()  # Salir si la carga/creación del vault falla
            return
        
        self.label = tk.Label(master, text="¡Bienvenido a SecureBox!")
        self.label.pack()

        self.create_container_button = tk.Button(master, text="Crear contenedor", command=self.create_container)
        self.create_container_button.pack()

        self.edit_container_button = tk.Button(master, text="Editar contenedor", command=self.edit_container)
        self.edit_container_button.pack()

        self.delete_container_button = tk.Button(master, text="Borrar contenedor", command=self.delete_container)
        self.delete_container_button.pack()

        self.view_container_button = tk.Button(master, text="Visualizar contenedor", command=self.view_container)
        self.view_container_button.pack()

        self.list_containers_button = tk.Button(master, text="Listar todos los contenedores", command=self.list_containers)
        self.list_containers_button.pack()

        self.upload_backup_button = tk.Button(master, text="Subir copia de seguridad a Google Drive", command=self.upload_backup)
        self.upload_backup_button.pack()

        self.quit_button = tk.Button(master, text="Salir", command=master.quit)
        self.quit_button.pack()

    def create_container(self):
        name = simpledialog.askstring("Input", "Nombre del contenedor:", parent=self.master)
        content = simpledialog.askstring("Input", "Contenido del contenedor:", parent=self.master)
        if name and content:
            containers_ui.create_container_ui(self.vault, self.key, name, content)
            messagebox.showinfo("Información", "Contenedor creado con éxito.")
            self.save_vault()
        else:
            messagebox.showerror("Error", "Debe proporcionar tanto el nombre como el contenido para el contenedor.")

    def edit_container(self):
        name = simpledialog.askstring("Input", "Nombre del contenedor a editar:", parent=self.master)
        if name in self.vault:
            content = simpledialog.askstring("Input", "Nuevo contenido del contenedor:", parent=self.master)
            if content:  # Asegurarse de que se haya ingresado contenido
                containers_ui.edit_container_ui(self.vault, self.key, name, content)
                messagebox.showinfo("Información", f"Contenedor '{name}' editado con éxito.")
                self.save_vault()
            else:
                messagebox.showerror("Error", "Debe proporcionar el contenido para el contenedor.")

    def delete_container(self):
        name = simpledialog.askstring("Input", "Nombre del contenedor a borrar:", parent=self.master)
        if name in self.vault:
            containers_ui.delete_container_ui(self.vault, self.key, name)
            messagebox.showinfo("Información", f"Contenedor '{name}' borrado con éxito.")
            self.save_vault()
        else:
            messagebox.showerror("Error", "Contenedor no encontrado.")

    def view_container(self):
        name = simpledialog.askstring("Input", "Nombre del contenedor a visualizar:", parent=self.master)
        if name and name in self.vault:
            containers_ui.view_container_ui(self.vault, self.key, name)
        else:
            messagebox.showerror("Error", "Contenedor no encontrado.")

    def list_containers(self):
        containers_ui.list_containers_ui(self.vault)

    def upload_backup(self):
        try:
            service = gdrive.authenticate_google_drive()
            file_path = "vault.json"
            mime_type = "application/json"
            gdrive.upload_file(service, file_path, mime_type)
            messagebox.showinfo("Backup", "Copia de seguridad subida con éxito a Google Drive.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo subir la copia de seguridad: {e}")

    def save_vault(self):
        # Guarda el vault actualizado utilizando la clave
        try:
            encryption.save_vault_changes(self.vault, self.key)
            messagebox.showinfo("Información", "Cambios guardados exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar los cambios en el vault: {e}")

root = tk.Tk()
my_gui = SecureBoxUI(root)
root.mainloop()
