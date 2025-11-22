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


@carrito_bp.route("/<int:cliente_id>/realizar_pedido", methods=["POST"])
def realizar_pedido(cliente_id):
    """Crea un pedido a partir del carrito activo del cliente.

    Body JSON opcional: { "metodo_pago_id": 1 }
    """
    data = request.get_json() or {}
    metodo_pago_id = data.get("metodo_pago_id", 1)
    res = service.realizar_pedido(cliente_id, metodo_pago_id)
    status = 200 if res.get("ok") else 400
    return jsonify(res), status


@carrito_bp.route("/pedido/<int:pedido_id>", methods=["GET"])
def ver_pedido(pedido_id):
    """Obtiene la información completa de un pedido (header + detalle)."""
    pedido = service.ver_pedido(pedido_id)
    if not pedido:
        return jsonify({"error": "Pedido no encontrado"}), 404
    return jsonify({"pedido": pedido}), 200
