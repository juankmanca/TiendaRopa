from flask import Blueprint, request, jsonify
from app.services.producto_service import ProductoService

productos_bp = Blueprint("productos", __name__)
service = ProductoService()

@productos_bp.route("/", methods=["GET"])
def listar():
    productos = service.listar_productos()
    return jsonify(productos)

@productos_bp.route("/", methods=["POST"])
def crear():
    data = request.get_json()
    producto = service.crear_producto(data)
    return jsonify({"mensaje": "Producto creado", "producto": producto}), 201

@productos_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.get_json()
    actualizado = service.actualizar_producto(id, data)
    return jsonify({"mensaje": "Producto actualizado", "producto": actualizado})

@productos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    eliminado = service.eliminar_producto(id)
    return jsonify({"mensaje": f"Producto {id} eliminado", "resultado": eliminado})
