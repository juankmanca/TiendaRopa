from app.db import SessionLocal
from app.repositories.carrito_repo import CarritoRepository

class CarritoService:
    def __init__(self):
        self.db = SessionLocal()

    def comprar_producto(self):
        print("\n=== Agregar producto al carrito ===")
        cliente_id = int(input("ID del cliente: "))
        producto_id = int(input("ID del producto: "))
        cantidad = int(input("Cantidad: "))

        carrito = CarritoRepository.obtener_carrito_activo(self.db, cliente_id)
        if not carrito:
            print("No existe carrito activo. Creando uno nuevo...")
            carrito = CarritoRepository.crear_carrito(self.db, cliente_id)

        detalle = CarritoRepository.agregar_producto(self.db, carrito.CarritoID, producto_id, cantidad)
        if detalle:
            print(f"Producto agregado correctamente al carrito #{carrito.CarritoID}.")
