from app.db import SessionLocal
from app.repositories.usuario_repo import UsuarioRepository

class UsuarioService:
    def __init__(self):
        self.db = SessionLocal()

    def crear_usuario(self, data):
        usuario = UsuarioRepository.crear_usuario(
            self.db,
            data["nombre"],
            data["email"],
            data["contrasena"],
            data["telefono"]
        )
        return {
            "UsuarioID": usuario.UsuarioID,
            "Nombre": usuario.Nombre,
            "Email": usuario.Email,
            "Telefono": usuario.Telefono,
        }

    def listar_usuarios(self):
        print("Listando service...")
        usuarios = UsuarioRepository.obtener_todos(self.db)
        print("Usuarios obtenidos:", usuarios)
        return [
            {
                "UsuarioID": u.UsuarioID,
                "Nombre": u.Nombre,
                "Email": u.Email,
                "Telefono": u.Telefono,
            }
            for u in usuarios
        ]

    def actualizar_usuario(self, usuario_id, data):
        usuario = UsuarioRepository.actualizar_usuario(
            self.db,
            usuario_id,
            Nombre=data.get("nombre"),
            Email=data.get("email"),
            Telefono=data.get("telefono")
        )
        if not usuario:
            return None
        return {
            "UsuarioID": usuario.UsuarioID,
            "Nombre": usuario.Nombre,
            "Email": usuario.Email,
            "Telefono": usuario.Telefono,
        }

    def eliminar_usuario(self, usuario_id):
        return UsuarioRepository.eliminar_usuario(self.db, usuario_id)
