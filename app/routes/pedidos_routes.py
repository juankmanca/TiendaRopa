from flask import Blueprint, request, jsonify
from app.services.pedidos_service import PedidosService

pedidos_bp = Blueprint("pedidos", __name__)
service = PedidosService()


@pedidos_bp.route("/cliente/<int:cliente_id>/crear", methods=["POST"])
def realizar_pedido_cliente(cliente_id):
    data = request.get_json() or {}
    metodo_pago_id = data.get("metodo_pago_id", 1)
    res = service.realizar_pedido(cliente_id, metodo_pago_id)
    status = 200 if res.get("ok") else 400
    return jsonify(res), status


@pedidos_bp.route("/<int:pedido_id>", methods=["GET"])
def ver_pedido(pedido_id):
    pedido = service.ver_pedido(pedido_id)
    if not pedido:
        return jsonify({"error": "Pedido no encontrado"}), 404
    return jsonify({"pedido": pedido}), 200


@pedidos_bp.route("/<int:pedido_id>", methods=["DELETE"])
def eliminar_pedido(pedido_id):
    res = service.eliminar_pedido(pedido_id)
    status = 200 if res.get("ok") else 400
    return jsonify(res), status


@pedidos_bp.route("/<int:pedido_id>/pagar", methods=["POST"])
def pagar_pedido(pedido_id):
    data = request.get_json() or {}
    monto = data.get("monto")
    estado_pago = data.get("estado_pago", "Pagado")
    if monto is None:
        return jsonify({"error": "monto es requerido"}), 400
    try:
        monto = float(monto)
    except Exception:
        return jsonify({"error": "monto inválido"}), 400
    res = service.pagar_pedido(pedido_id, monto, estado_pago)
    status = 200 if res.get("ok") else 400
    return jsonify(res), status
