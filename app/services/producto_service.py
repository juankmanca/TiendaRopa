from app.db import SessionLocal
from app.repositories.productos_repo import ProductoRepository


class ProductoService:
    def __init__(self):
        self.db = SessionLocal()

    def crear_producto(self, data):
        # crear devuelve {'ProductoID': id}
        created = ProductoRepository.crear_producto(
            self.db,
            data["nombre"],
            data["descripcion"],
            data["precio"],
            data["stock"],
            data["categoria_id"],
            data["marca_id"],
        )
        producto_id = created.get("ProductoID") if created else None
        if not producto_id:
            return None
        prod = ProductoRepository.obtener_producto_por_id(self.db, producto_id)
        if not prod:
            return None
        return {
            "ProductoID": prod.get("ProductoID"),
            "Nombre": prod.get("Nombre"),
            "Descripcion": prod.get("Descripcion"),
            "Precio": float(prod.get("Precio")) if prod.get("Precio") is not None else None,
            "Stock": int(prod.get("Stock")) if prod.get("Stock") is not None else None,
        }

    def listar_productos(self):
        productos = ProductoRepository.listar_productos(self.db)
        return [
            {
                "ProductoID": p.get("ProductoID"),
                "Nombre": p.get("Nombre"),
                "Descripcion": p.get("Descripcion"),
                "Precio": float(p.get("Precio")) if p.get("Precio") is not None else None,
                "Stock": int(p.get("Stock")) if p.get("Stock") is not None else None,
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
            Nombre=data.get("nombre", producto.get("Nombre")),
            Precio=data.get("precio", producto.get("Precio")),
            Stock=data.get("stock", producto.get("Stock")),
            Descripcion=data.get("descripcion", producto.get("Descripcion")),
        )
        if not actualizado:
            return None
        return {
            "ProductoID": actualizado.get("ProductoID"),
            "Nombre": actualizado.get("Nombre"),
            "Descripcion": actualizado.get("Descripcion"),
            "Precio": float(actualizado.get("Precio")) if actualizado.get("Precio") is not None else None,
            "Stock": int(actualizado.get("Stock")) if actualizado.get("Stock") is not None else None,
        }

    def eliminar_producto(self, producto_id):
        return ProductoRepository.eliminar_producto(self.db, producto_id)
