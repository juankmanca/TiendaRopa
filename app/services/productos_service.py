from app.db import SessionLocal
from app.repositories.productos_repo import ProductoRepository

class ProductoService:
    def __init__(self):
        self.db = SessionLocal()

    def crear_producto(self):
        print("\n=== Crear Producto ===")
        nombre = input("Nombre: ")
        descripcion = input("Descripción: ")
        precio = float(input("Precio: "))
        stock = int(input("Stock: "))
        categoria_id = int(input("CategoriaID: "))
        marca_id = int(input("MarcaID: "))

        prod = ProductoRepository.crear_producto(
            self.db, nombre, descripcion, precio, stock, categoria_id, marca_id
        )
        print(f"Producto creado con ID {prod.ProductoID}")

    def listar_productos(self):
        productos = ProductoRepository.listar_productos(self.db)
        if not productos:
            print("No hay productos registrados.")
            return
        print("\n=== Lista de productos ===")
        for p in productos:
            print(f"[{p.ProductoID}] {p.Nombre} - {p.Descripcion} - ${p.Precio} (Stock: {p.Stock})")

    def actualizar_producto(self):
        producto_id = int(input("ID del producto a actualizar: "))
        producto = ProductoRepository.obtener_producto_por_id(self.db, producto_id)
        if not producto:
            print("Producto no encontrado.")
            return
        print(f"Editando producto: {producto.Nombre}")
        nuevo_nombre = input(f"Nuevo nombre ({producto.Nombre}): ") or producto.Nombre
        nueva_descripcion = input(f"Nueva descripción ({producto.Descripcion}): ") or producto.Descripcion
        nuevo_precio = input(f"Nuevo precio ({producto.Precio}): ") or producto.Precio
        nuevo_stock = input(f"Nuevo stock ({producto.Stock}): ") or producto.Stock

        actualizado = ProductoRepository.actualizar_producto(
            self.db,
            producto_id,
            Nombre=nuevo_nombre,
            Precio=float(nuevo_precio),
            Stock=int(nuevo_stock),
            Descripcion=nueva_descripcion
        )
        print(f"Producto actualizado: {actualizado.Nombre}")

    def eliminar_producto(self):
        producto_id = int(input("ID del producto a eliminar: "))
        ok = ProductoRepository.eliminar_producto(self.db, producto_id)
        if ok:
            print("Producto eliminado.")
        else:
            print("Producto no encontrado.")
