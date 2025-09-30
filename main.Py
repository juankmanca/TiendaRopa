from app.utils.menu import mostrar_menu_principal
from app.services.tienda_service import TiendaService

def main():
    tienda = TiendaService()
    while True:
        opcion = mostrar_menu_principal()
        if opcion == "1":
            tienda.registrar_usuario()
        elif opcion == "2":
            tienda.listar_productos()
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
