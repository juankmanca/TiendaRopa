from app.db import SessionLocal
from app.repositories.productos_repo import ProductoRepository

class ProductoService:
    def __init__(self):
        self.db = SessionLocal()

    def crear_producto(self, data):
        prod = ProductoRepository.crear_producto(
            self.db,
            data["nombre"],
            data["descripcion"],
            data["precio"],
            data["stock"],
            data["categoria_id"],
            data["marca_id"],
        )
        return {
            "ProductoID": prod.ProductoID,
            "Nombre": prod.Nombre,
            "Descripcion": prod.Descripcion,
            "Precio": prod.Precio,
            "Stock": prod.Stock,
        }

    def listar_productos(self):
        productos = ProductoRepository.listar_productos(self.db)
        return [
            {
                "ProductoID": p.ProductoID,
                "Nombre": p.Nombre,
                "Descripcion": p.Descripcion,
                "Precio": p.Precio,
                "Stock": p.Stock,
            }
            for p in productos
        ]

    def actualizar_producto(self, producto_id, data):
        producto = ProductoRepository.obtener_producto_por_id(self.db, producto_id)
        if not producto:
            return None

        actualizado = ProductoRepository.actualizar_producto(
            self.db,
            producto_id,
            Nombre=data.get("nombre", producto.Nombre),
            Precio=float(data.get("precio", producto.Precio)),
            Stock=int(data.get("stock", producto.Stock)),
            Descripcion=data.get("descripcion", producto.Descripcion),
        )
        return {
            "ProductoID": actualizado.ProductoID,
            "Nombre": actualizado.Nombre,
            "Descripcion": actualizado.Descripcion,
            "Precio": actualizado.Precio,
            "Stock": actualizado.Stock,
        }

    def eliminar_producto(self, producto_id):
        return ProductoRepository.eliminar_producto(self.db, producto_id)
