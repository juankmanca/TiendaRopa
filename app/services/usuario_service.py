from app.db import SessionLocal
from app.repositories.usuario_repo import UsuarioRepository

class UsuarioService:
    def __init__(self):
        self.db = SessionLocal()

    def crear_usuario(self, data):
        res = UsuarioRepository.crear_usuario(
            self.db,
            data["nombre"],
            data["email"],
            data["contrasena"],
            data.get("telefono"),
        )
        # res puede incluir {'UsuarioID': id, 'ClienteID': id}
        usuario_id = None
        if isinstance(res, dict):
            usuario_id = res.get("UsuarioID") or res.get("UsuarioId")
        return {"UsuarioID": usuario_id}

    def listar_usuarios(self):
        print("Listando service...")
        usuarios = UsuarioRepository.obtener_todos(self.db)
        print("Usuarios obtenidos:", usuarios)
        return [
            {
                "UsuarioID": u.get("UsuarioID"),
                "ClienteID": u.get("ClienteID"),
                "Nombre": u.get("Nombre"),
                "Email": u.get("Email"),
                "Telefono": u.get("Telefono"),
            }
            for u in usuarios
        ]

    def actualizar_usuario(self, usuario_id, data):
        usuario = UsuarioRepository.actualizar_usuario(
            self.db,
            usuario_id,
            Nombre=data.get("nombre"),
            Email=data.get("email"),
            Telefono=data.get("telefono"),
        )
        if not usuario:
            return None
        return {
            "UsuarioID": usuario.get("UsuarioID"),
            "Nombre": usuario.get("Nombre"),
            "Email": usuario.get("Email"),
            "Telefono": usuario.get("Telefono"),
        }

    def eliminar_usuario(self, usuario_id):
        return UsuarioRepository.eliminar_usuario(self.db, usuario_id)
