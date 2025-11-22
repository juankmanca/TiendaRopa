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


class ProductoRepository:

    @staticmethod
    def crear_producto(db, nombre: str, descripcion: str, precio: float, stock: int, categoria_id: int, marca_id: int):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL sp_create_product(%s, %s, %s, %s, %s, %s)",
                    (nombre, descripcion, precio, stock, categoria_id, marca_id),
                )
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def obtener_producto_por_id(db, producto_id: int):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_get_product_by_id(%s)", (producto_id,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def listar_productos(db):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_list_products()")
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def actualizar_producto(db, producto_id: int, **kwargs):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL sp_update_product(%s, %s, %s, %s, %s, %s, %s)",
                    (
                        producto_id,
                        kwargs.get("Nombre"),
                        kwargs.get("Descripcion"),
                        kwargs.get("Precio"),
                        kwargs.get("Stock"),
                        kwargs.get("CategoriaID"),
                        kwargs.get("MarcaID"),
                    ),
                )
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def eliminar_producto(db, producto_id: int) -> bool:
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_delete_product(%s)", (producto_id,))
                res = cur.fetchone()
                return res and res.get("affected", 0) > 0
        finally:
            conn.close()
