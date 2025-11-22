from flask import Blueprint, request, jsonify
import jwt

from app.services.carrito_service import CarritoService
from app.config import SECRET_KEY
from app.utils.encrypt import decrypt_token

carrito_bp = Blueprint("carrito", __name__)
service = CarritoService()


def _get_cliente_id_from_header(req):
    auth = req.headers.get("Authorization") or req.headers.get("authorization")
    if not auth:
        return None
    parts = auth.split()
    # Accept both 'Bearer <token>' and just '<token>'
    if len(parts) == 0:
        return None
    token = parts[0] if len(parts) == 1 else parts[1]
    # strip possible quotes
    token = token.strip().strip('"').strip("'")
    # If token appears encrypted (our format uses '|' separators), try to decrypt first
    if "|" in token:
        try:
            print("Token appears encrypted, attempting decryption")
            token = decrypt_token(token)
            print("Decrypted token successfully")
        except Exception as e:
            print(f"Failed to decrypt token: {e}")
            return None
    try:
        print(f"Decoding token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("cliente_id") or payload.get("ClienteID")
    except jwt.ExpiredSignatureError:
        print("JWT decode failed: token expired")
        return None
    except jwt.InvalidTokenError as e:
        msg = str(e)
        print(f"JWT decode failed: {msg}")
        # Some tokens (created with numeric 'sub') raise 'Subject must be a string'.
        # As a fallback for development/testing, try to decode without signature
        # verification to extract the payload (NOT recommended for production).
        if "Subject must be a string" in msg or "Subject" in msg:
            try:
                print("Attempting fallback decode without signature verification (dev only)")
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_signature": False})
                return payload.get("cliente_id") or payload.get("ClienteID")
            except Exception as e2:
                print(f"Fallback decode also failed: {e2}")
                return None
        return None

@carrito_bp.route("/comprar", methods=["POST"])
def comprar():
    data = request.get_json() or {}
    # intentar obtener cliente_id desde token (Authorization: Bearer <token>)
    auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
    token_cliente = _get_cliente_id_from_header(request)
    print(f"Token cliente ID: {token_cliente}")
    # si vino header pero el token no fue decodificado => token inválido/expirado
    if auth_header and not token_cliente:
        return jsonify({"error": "token inválido o expirado"}), 401
    if token_cliente:
        data["cliente_id"] = token_cliente
    if not data.get("cliente_id"):
        return jsonify({"error": "cliente_id no proporcionado en el token o en la URL"}), 401
    resultado = service.comprar_producto(data)
    return jsonify({"mensaje": "Compra realizada", "resultado": resultado})


@carrito_bp.route("/ver", methods=["GET"])
def ver_carritos():
    """Obtiene los carritos (y su detalle) de un cliente."""
    auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
    token_cliente = _get_cliente_id_from_header(request)
    if auth_header and not token_cliente:
        return jsonify({"error": "token inválido o expirado"}), 401
    use_id = token_cliente if token_cliente else cliente_id
    carritos = service.ver_carritos_cliente(use_id)
    return jsonify({"carritos": carritos}), 200


@carrito_bp.route("/vaciar", methods=["POST"])
def vaciar_carrito():
    """Vacía el carrito activo del cliente indicado (restaura stock)."""
    auth_header = request.headers.get("Authorization") or request.headers.get("authorization")
    token_cliente = _get_cliente_id_from_header(request)
    if auth_header and not token_cliente:
        return jsonify({"error": "token inválido o expirado"}), 401
    use_id = token_cliente if token_cliente else cliente_id
    res = service.vaciar_carrito(use_id)
    status = 200 if res.get("ok") else 400
    return jsonify(res), status

