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


class PedidosRepository:
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

    @staticmethod
    def eliminar_pedido_por_id(db, pedido_id: int):
        """Elimina un pedido y restaura stock llamando a sp_delete_order_by_id."""
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_delete_order_by_id(%s)", (pedido_id,))
                return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def pagar_pedido(db, pedido_id: int, monto: float, estado_pago: str = "Pagado"):
        """Registra un pago y actualiza el estado del pedido llamando a sp_pay_order."""
        conn = _get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("CALL sp_pay_order(%s, %s, %s)", (pedido_id, monto, estado_pago))
                return cur.fetchone()
        finally:
            conn.close()
