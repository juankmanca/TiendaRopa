from app.services.usuario_service import UsuarioService
from app.services.productos_service import ProductoService
from app.services.carrito_service import CarritoService
from app.utils.menu import mostrar_menu_principal

def main():
    usuario_service = UsuarioService()
    producto_service = ProductoService()
    carrito_service = CarritoService()

    while True:
        opcion = mostrar_menu_principal()

        if opcion == "1":
            producto_service.crear_producto()
        elif opcion == "2":
            producto_service.listar_productos()
        elif opcion == "3":
            producto_service.actualizar_producto()
        elif opcion == "4":
            producto_service.eliminar_producto()
        elif opcion == "5":
            usuario_service.crear_usuario()
        elif opcion == "6":
            usuario_service.listar_usuarios()
        elif opcion == "7":
            usuario_service.actualizar_usuario()
        elif opcion == "8":
            usuario_service.eliminar_usuario()
        elif opcion == "9":
            carrito_service.comprar_producto()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

        input("\nSeleccione cualquier tecla para regresar: ")


main()