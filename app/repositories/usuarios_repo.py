from sqlalchemy.orm import Session
from app.models.usuarios import Usuario

class UsuarioRepository:

    @staticmethod
    def crear_usuario(db: Session, nombre: str, email: str, contrasena: str, telefono: str, rol_id: int) -> Usuario:
        """
        Crea un nuevo usuario en la base de datos.
        """
        nuevo_usuario = Usuario(
            Nombre=nombre,
            Email=email,
            Contrasena=contrasena,
            Telefono=telefono,
            RolID=rol_id
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)  # actualiza el objeto con su ID generado
        return nuevo_usuario

    @staticmethod
    def obtener_usuario_por_id(db: Session, usuario_id: int) -> Usuario | None:
        """
        Retorna un usuario por su ID.
        """
        return db.query(Usuario).filter(Usuario.UsuarioID == usuario_id).first()

    @staticmethod
    def obtener_usuario_por_email(db: Session, email: str) -> Usuario | None:
        """
        Retorna un usuario por su email.
        """
        return db.query(Usuario).filter(Usuario.Email == email).first()

    @staticmethod
    def listar_usuarios(db: Session) -> list[Usuario]:
        """
        Devuelve todos los usuarios registrados.
        """
        return db.query(Usuario).all()

    @staticmethod
    def eliminar_usuario(db: Session, usuario_id: int) -> bool:
        """
        Elimina un usuario por ID. Retorna True si se eliminó, False si no existe.
        """
        usuario = db.query(Usuario).filter(Usuario.UsuarioID == usuario_id).first()
        if usuario:
            db.delete(usuario)
            db.commit()
            return True
        return False
