from sqlalchemy.orm import Session
from app.models.productos import Producto

class ProductoRepository:

    @staticmethod
    def crear_producto(db: Session, nombre: str, descripcion: str, precio: float, stock: int, categoria_id: int, marca_id: int) -> Producto:
        nuevo = Producto(
            Nombre=nombre,
            Descripcion=descripcion,
            Precio=precio,
            Stock=stock,
            CategoriaID=categoria_id,
            MarcaID=marca_id
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    @staticmethod
    def obtener_producto_por_id(db: Session, producto_id: int) -> Producto | None:
        return db.query(Producto).filter(Producto.ProductoID == producto_id).first()

    @staticmethod
    def listar_productos(db: Session) -> list[Producto]:
        return db.query(Producto).all()

    @staticmethod
    def actualizar_producto(db: Session, producto_id: int, **kwargs) -> Producto | None:
        producto = db.query(Producto).filter(Producto.ProductoID == producto_id).first()
        if not producto:
            return None
        for attr, value in kwargs.items():
            if hasattr(producto, attr) and value is not None:
                setattr(producto, attr, value)
        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def eliminar_producto(db: Session, producto_id: int) -> bool:
        producto = db.query(Producto).filter(Producto.ProductoID == producto_id).first()
        if producto:
            db.delete(producto)
            db.commit()
            return True
        return False
