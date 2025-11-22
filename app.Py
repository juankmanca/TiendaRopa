from flask import Flask, jsonify
from app.routes.productos_routes import productos_bp
from app.routes.usuarios_routes import usuarios_bp
from app.routes.carrito_routes import carrito_bp
from app.routes.auth_routes import auth_bp
from app.routes.pedidos_routes import pedidos_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(carrito_bp, url_prefix="/carrito")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(pedidos_bp, url_prefix="/pedidos")

    @app.route("/ping", methods=["GET"])
    def ping():
        return jsonify({"message": "pong"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
