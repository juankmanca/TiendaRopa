# from app.services.usuario_service import UsuarioService
# from app.services.productos_service import ProductoService
# from app.services.carrito_service import CarritoService
# from app.utils.menu import mostrar_menu_principal

# def main():
#     usuario_service = UsuarioService()
#     producto_service = ProductoService()
#     carrito_service = CarritoService()

#     while True:
#         opcion = mostrar_menu_principal()

#         if opcion == "1":
#             producto_service.crear_producto()
#         elif opcion == "2":
#             producto_service.listar_productos()
#         elif opcion == "3":
#             producto_service.actualizar_producto()
#         elif opcion == "4":
#             producto_service.eliminar_producto()
#         elif opcion == "5":
#             usuario_service.crear_usuario()
#         elif opcion == "6":
#             usuario_service.listar_usuarios()
#         elif opcion == "7":
#             usuario_service.actualizar_usuario()
#         elif opcion == "8":
#             usuario_service.eliminar_usuario()
#         elif opcion == "9":
#             carrito_service.comprar_producto()
#         elif opcion == "0":
#             print("Saliendo del sistema...")
#             break
#         else:
#             print("Opción inválida. Intente nuevamente.")

#         input("\nSeleccione cualquier tecla para regresar: ")


# main()

from flask import Flask, jsonify
from app.routes.productos_routes import productos_bp
from app.routes.usuarios_routes import usuarios_bp
from app.routes.carrito_routes import carrito_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(carrito_bp, url_prefix="/carrito")

    @app.route("/ping", methods=["GET"])
    def ping():
        return jsonify({"message": "pong"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
