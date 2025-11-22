import pymysql
from pymysql.cursors import DictCursor
from app.config import DB_USER, DB_PASS, DB_HOST, DB_NAME
from app.repositories.auth_repo import _hash_password


def _get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        cursorclass=DictCursor,
        autocommit=True,
    )


class UsuarioRepository:

    @staticmethod
    def crear_usuario(db, nombre: str, email: str, contrasena: str, telefono: str):
        pw_hash = _hash_password(contrasena)
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_create_user_with_cliente(%s,%s,%s,%s, %s)", (nombre, email, pw_hash, telefono, 1))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def obtener_todos(db):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_get_all_users()")
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(db, usuario_id: int):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_get_user_by_id(%s)", (usuario_id,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def actualizar_usuario(db, usuario_id: int, **datos):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL sp_update_user(%s, %s, %s, %s, %s, %s)",
                    (
                        usuario_id,
                        datos.get("Nombre"),
                        datos.get("Email"),
                        _hash_password(datos["Contrasena"]) if datos.get("Contrasena") else None,
                        datos.get("Telefono"),
                        datos.get("RolID"),
                    ),
                )
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def eliminar_usuario(db, usuario_id: int):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_delete_user(%s)", (usuario_id,))
                res = cur.fetchone()
                return res and res.get("affected", 0) > 0
        finally:
            conn.close()
