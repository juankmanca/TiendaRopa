<<<<<<< HEAD
from app.db import SessionLocal
from app.repositories.usuarios_repo import usuarioRepository
=======
# app/services/usuario_service.py
from app.db import SessionLocal
from app.repositories.usuario_repo import UsuarioRepository
>>>>>>> backup

class UsuarioService:
    def __init__(self):
        self.db = SessionLocal()

    def crear_usuario(self):
<<<<<<< HEAD
        print("\n=== Crear usuario ===")
        nombre = input("Nombre: ")
        descripcion = input("Descripción: ")
        telefono = float(input("telefono: "))
        contraseña = int(input("contraseña: "))
        rolid = int(input("rolID: "))
        

        prod = UsuarioService(
            self.db, nombre, descripcion, telefono, contraseña, rolid
        )
        print(f"usuario creado  {UsuarioService.crear_usuario}")

   
=======
        print("\n=== Crear nuevo usuario ===")
        nombre = input("Nombre: ")
        email = input("Email: ")
        contrasena = input("Contraseña: ")
        telefono = input("Teléfono: ")

        usuario = UsuarioRepository.crear_usuario(self.db, nombre, email, contrasena, telefono)
        print(f"Usuario '{usuario.Nombre}' creado correctamente con ID {usuario.UsuarioID}")

    def listar_usuarios(self):
        print("\n=== Lista de usuarios ===")
        usuarios = UsuarioRepository.obtener_todos(self.db)
        if not usuarios:
            print("No hay usuarios registrados.")
            return

        for u in usuarios:
            print(f"[{u.UsuarioID}] {u.Nombre} - {u.Email} - Tel: {u.Telefono}")

    def actualizar_usuario(self):
        print("\n=== Actualizar usuario ===")
        usuario_id = int(input("ID del usuario: "))
        nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
        email = input("Nuevo email (dejar vacío para no cambiar): ")
        telefono = input("Nuevo teléfono (dejar vacío para no cambiar): ")

        datos = {
            "Nombre": nombre or None,
            "Email": email or None,
            "Telefono": telefono or None
        }

        usuario = UsuarioRepository.actualizar_usuario(self.db, usuario_id, **datos)
        if usuario:
            print("Usuario actualizado correctamente.")
        else:
            print("Usuario no encontrado.")

    def eliminar_usuario(self):
        print("\n=== Eliminar usuario ===")
        usuario_id = int(input("ID del usuario a eliminar: "))
        if UsuarioRepository.eliminar_usuario(self.db, usuario_id):
            print("Usuario y cliente eliminado correctamente.")
        else:
            print("Usuario no encontrado.")
>>>>>>> backup
