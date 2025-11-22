import hashlib
import pymysql
from pymysql.cursors import DictCursor
from app.config import DB_USER, DB_PASS, DB_HOST, DB_NAME


def _get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        cursorclass=DictCursor,
        autocommit=True,
    )


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def login(email: str, password: str) -> dict | None:
    """Llama al procedimiento almacenado sp_login pasando email y hash de contraseña.

    Retorna un diccionario con los datos del usuario (sin contraseña) o None si no hay coincidencia.
    """
    pw_hash = _hash_password(password)
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL sp_login(%s, %s)", (email, pw_hash))
            row = cur.fetchone()
            return row
    finally:
        conn.close()


def create_user(nombre: str, email: str, password: str, telefono: str | None = None, rol_id: int = 1) -> dict | None:
    """Llama a sp_create_user para insertar un nuevo usuario.

    Retorna un diccionario con UsuarioID (ejemplo: {'UsuarioID': 5}) o None en fallo.
    """
    pw_hash = _hash_password(password)
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL sp_create_user(%s, %s, %s, %s, %s)", (nombre, email, pw_hash, telefono, rol_id))
            res = cur.fetchone()
            return res
    finally:
        conn.close()
