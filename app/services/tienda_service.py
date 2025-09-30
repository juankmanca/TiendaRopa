from app.db import SessionLocal
from app.repositories.usuarios_repo import UsuarioRepository

class TiendaService:
    def __init__(self):
        self.db = SessionLocal()

    def registrar_usuario(self):
        print("\n=== Registro de Usuario ===")
        nombre = input("Nombre: ")
        email = input("Email: ")
        contrasena = input("Contraseña: ")
        telefono = input("Teléfono: ")
        rol_id = 1  # por defecto "cliente"

        usuario = UsuarioRepository.crear_usuario(
            self.db, nombre, email, contrasena, telefono, rol_id
        )
        print(f"✅ Usuario creado con ID {usuario.UsuarioID}")

    def listar_usuarios(self):
        usuarios = UsuarioRepository.listar_usuarios(self.db)
        for u in usuarios:
            print(f"[{u.UsuarioID}] {u.Nombre} - {u.Email}")
