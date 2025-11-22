from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
service = AuthService()


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "email y password requeridos"}), 400

    res = service.login(email, password)
    if not res:
        return jsonify({"error": "Credenciales inválidas"}), 401

    # res contiene {'access_token': '...'}
    return jsonify(res), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    nombre = data.get("nombre")
    email = data.get("email")
    password = data.get("password")
    telefono = data.get("telefono")
    if not nombre or not email or not password:
        return jsonify({"error": "nombre, email y password requeridos"}), 400

    res = service.crear_usuario(nombre, email, password, telefono)
    if not res:
        return jsonify({"error": "No se pudo crear el usuario"}), 500

    return jsonify(res), 201
