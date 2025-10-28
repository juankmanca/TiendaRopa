from app.db import SessionLocal
from app.repositories.carrito_repo import CarritoRepository

class CarritoService:
    def __init__(self):
        self.db = SessionLocal()

    def comprar_producto(self, data):
        cliente_id = data["cliente_id"]
        producto_id = data["producto_id"]
        cantidad = data["cantidad"]

        carrito = CarritoRepository.obtener_carrito_activo(self.db, cliente_id)
        if not carrito:
            carrito = CarritoRepository.crear_carrito(self.db, cliente_id)

        detalle = CarritoRepository.agregar_producto(
            self.db,
            carrito.CarritoID,
            producto_id,
            cantidad
        )

        return {
            "CarritoID": carrito.CarritoID,
            "Detalle": {
                "ProductoID": producto_id,
                "Cantidad": cantidad,
                "Resultado": bool(detalle)
            }
        }
