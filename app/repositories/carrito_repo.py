from sqlalchemy.orm import Session
from app.models.carrito import Carrito
from app.models.carrito_detalle import CarritoDetalle
from app.models.productos import Producto
from datetime import datetime

class CarritoRepository:

    @staticmethod
    def obtener_carrito_activo(db: Session, cliente_id: int) -> Carrito | None:
        return db.query(Carrito).filter(
            Carrito.ClienteID == cliente_id,
            Carrito.Activo == True
        ).first()

    @staticmethod
    def crear_carrito(db: Session, cliente_id: int) -> Carrito:
        nuevo = Carrito(
            ClienteID=cliente_id,
            FechaCreacion=datetime.now(),
            Activo=True
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    @staticmethod
    def agregar_producto(db: Session, carrito_id: int, producto_id: int, cantidad: int) -> CarritoDetalle | None:
        producto = db.query(Producto).filter(Producto.ProductoID == producto_id).first()
        if not producto:
            print("Producto no encontrado.")
            return None

        if producto.Stock < cantidad:
            print(f"Stock insuficiente. Disponible: {producto.Stock}")
            return None

        detalle = CarritoDetalle(
            CarritoID=carrito_id,
            ProductoID=producto_id,
            Cantidad=cantidad,
            PrecioUnitario=producto.Precio
        )

        # Descontar stock
        producto.Stock -= cantidad

        db.add(detalle)
        db.commit()
        db.refresh(detalle)
        print(f"Producto agregado al carrito. Subtotal: ${float(producto.Precio) * cantidad:.2f}")
        return detalle
