from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.models.clientes import Cliente

class UsuarioRepository:

    @staticmethod
    def crear_usuario(db: Session, nombre: str, email: str, contrasena: str, telefono: str) -> Usuario:
        usuario = Usuario(
            Nombre=nombre,
            Email=email,
            Contrasena=contrasena,
            Telefono=telefono,
            RolID=1  # Por ahora, siempre será 1: rol Admin
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        # Crear registro asociado en Clientes
        cliente = Cliente(UsuarioID=usuario.UsuarioID)
        db.add(cliente)
        db.commit()

        return usuario

    @staticmethod
    def obtener_todos(db: Session):
        return db.query(Usuario).all()

    @staticmethod
    def obtener_por_id(db: Session, usuario_id: int):
        return db.query(Usuario).filter(Usuario.UsuarioID == usuario_id).first()

    @staticmethod
    def actualizar_usuario(db: Session, usuario_id: int, **datos):
        usuario = db.query(Usuario).filter(Usuario.UsuarioID == usuario_id).first()
        if not usuario:
            return None

        for campo, valor in datos.items():
            if hasattr(usuario, campo) and valor is not None:
                setattr(usuario, campo, valor)

        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def eliminar_usuario(db: Session, usuario_id: int):
        usuario = db.query(Usuario).filter(Usuario.UsuarioID == usuario_id).first()
        if not usuario:
            return False

        # Eliminar cliente asociado
        cliente = db.query(Cliente).filter(Cliente.UsuarioID == usuario_id).first()
        if cliente:
            db.delete(cliente)

        db.delete(usuario)
        db.commit()
        return True
