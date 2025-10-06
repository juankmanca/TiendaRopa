from app.db import SessionLocal
from app.repositories.usuarios_repo import usuarioRepository

class UsuarioService:
    def __init__(self):
        self.db = SessionLocal()

    def crear_usuario(self):
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

   
