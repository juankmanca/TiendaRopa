from app.utils.menu import mostrar_menu_principal
from app.services.productos_service import ProductoService

def main():
    productos_service = ProductoService()

    while True:
        opcion = mostrar_menu_principal()
        if opcion == "1":
            productos_service.crear_producto()
        elif opcion == "2":
            productos_service.listar_productos()
        elif opcion == "3":
            productos_service.actualizar_producto()
        elif opcion == "4":
            productos_service.eliminar_producto()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
