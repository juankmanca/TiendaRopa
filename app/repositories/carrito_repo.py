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


class CarritoRepository:

    @staticmethod
    def obtener_carrito_activo(db, cliente_id: int):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_get_active_cart(%s)", (cliente_id,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def crear_carrito(db, cliente_id: int):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_create_cart(%s)", (cliente_id,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def agregar_producto(db, carrito_id: int, producto_id: int, cantidad: int):
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_add_to_cart(%s, %s, %s)", (carrito_id, producto_id, cantidad))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def obtener_carritos_con_detalle_por_cliente(db, cliente_id: int):
        """Devuelve lista de filas con carrito + detalle para un cliente."""
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_get_cart_with_details_by_cliente(%s)", (cliente_id,))
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def vaciar_carrito_por_id(db, carrito_id: int):
        """Llama a sp_empty_cart_by_id para restaurar stock, eliminar detalles y marcar carrito inactivo.

        Retorna un diccionario como {'deleted_details': N} o None en error.
        """
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_empty_cart_by_id(%s)", (carrito_id,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def crear_pedido_desde_carrito(db, carrito_id: int, metodo_pago_id: int = 1):
        """Crea un pedido a partir del carrito: inserta Pedidos y PedidoDetalle, borra detalles y marca carrito inactivo."""
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_create_order_from_cart(%s, %s)", (carrito_id, metodo_pago_id))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def obtener_pedido_por_id(db, pedido_id: int):
        """Devuelve filas del pedido y sus detalles llamando a sp_get_order_by_id."""
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_get_order_by_id(%s)", (pedido_id,))
                return cur.fetchall()
        finally:
            conn.close()
