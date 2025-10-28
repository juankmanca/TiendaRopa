from flask import Blueprint, request, jsonify
from app.services.carrito_service import CarritoService

carrito_bp = Blueprint("carrito", __name__)
service = CarritoService()

@carrito_bp.route("/comprar", methods=["POST"])
def comprar():
    data = request.get_json()
    resultado = service.comprar_producto(data)
    return jsonify({"mensaje": "Compra realizada", "resultado": resultado})
