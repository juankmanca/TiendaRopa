from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService

usuarios_bp = Blueprint("usuarios", __name__)
service = UsuarioService()

@usuarios_bp.route("/", methods=["GET"])
def listar():
    print("Listando usuarios...")
    usuarios = service.listar_usuarios()
    return jsonify(usuarios), 200

@usuarios_bp.route("/", methods=["POST"])
def crear():
    data = request.get_json()
    nuevo = service.crear_usuario(data)
    return jsonify({"mensaje": "Usuario creado", "usuario": nuevo}), 201

@usuarios_bp.route("/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.get_json()
    actualizado = service.actualizar_usuario(id, data)
    return jsonify({"mensaje": "Usuario actualizado", "usuario": actualizado})

@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def eliminar(id):
    eliminado = service.eliminar_usuario(id)
    return jsonify({"mensaje": f"Usuario {id} eliminado", "resultado": eliminado})
