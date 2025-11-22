from flask import Blueprint, request, jsonify
from app.services.carrito_service import CarritoService

carrito_bp = Blueprint("carrito", __name__)
service = CarritoService()

@carrito_bp.route("/comprar", methods=["POST"])
def comprar():
    data = request.get_json()
    resultado = service.comprar_producto(data)
    return jsonify({"mensaje": "Compra realizada", "resultado": resultado})


@carrito_bp.route("/<int:cliente_id>", methods=["GET"])
def ver_carritos(cliente_id):
    """Obtiene los carritos (y su detalle) de un cliente."""
    carritos = service.ver_carritos_cliente(cliente_id)
    return jsonify({"carritos": carritos}), 200


@carrito_bp.route("/<int:cliente_id>/vaciar", methods=["POST"])
def vaciar_carrito(cliente_id):
    """Vacía el carrito activo del cliente indicado (restaura stock)."""
    res = service.vaciar_carrito(cliente_id)
    status = 200 if res.get("ok") else 400
    return jsonify(res), status

