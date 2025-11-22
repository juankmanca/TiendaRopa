from app.db import SessionLocal
from app.repositories.pedidos_repo import PedidosRepository
from app.repositories.carrito_repo import CarritoRepository


class PedidosService:
    def __init__(self):
        self.db = SessionLocal()

    def realizar_pedido(self, cliente_id: int, metodo_pago_id: int = 1):
        """Crea un pedido a partir del carrito activo del cliente."""
        carrito = CarritoRepository.obtener_carrito_activo(self.db, cliente_id)
        if not carrito:
            return {"ok": False, "message": "No existe carrito activo para el cliente"}

        carrito_id = carrito.get("CarritoID") if isinstance(carrito, dict) else None
        if not carrito_id:
            return {"ok": False, "message": "Carrito inválido"}

        res = PedidosRepository.crear_pedido_desde_carrito(self.db, carrito_id, metodo_pago_id)
        if not res:
            return {"ok": False, "message": "Error al crear el pedido"}

        if isinstance(res, dict) and res.get("status") == 0:
            return {"ok": True, "PedidoID": res.get("PedidoID"), "message": res.get("message")}
        return {"ok": False, "info": res}

    def ver_pedido(self, pedido_id: int):
        filas = PedidosRepository.obtener_pedido_por_id(self.db, pedido_id)
        if not filas:
            return None

        header = filas[0]
        pedido = {
            "PedidoID": header.get("PedidoID"),
            "ClienteID": header.get("ClienteID"),
            "FechaPedido": str(header.get("FechaPedido")) if header.get("FechaPedido") is not None else None,
            "EstadoPedido": header.get("EstadoPedido"),
            "MetodoPagoID": header.get("MetodoPagoID"),
            "Detalle": [],
            "Total": 0.0,
        }

        total = 0.0
        for f in filas:
            if f.get("PedidoDetalleID") is not None:
                cantidad = int(f.get("Cantidad")) if f.get("Cantidad") is not None else 0
                precio = float(f.get("PrecioUnitario")) if f.get("PrecioUnitario") is not None else 0.0
                subtotal = cantidad * precio
                total += subtotal
                pedido["Detalle"].append(
                    {
                        "PedidoDetalleID": f.get("PedidoDetalleID"),
                        "ProductoID": f.get("ProductoID"),
                        "ProductoNombre": f.get("ProductoNombre"),
                        "Cantidad": cantidad,
                        "PrecioUnitario": precio,
                        "SubTotal": subtotal,
                    }
                )

        pedido["Total"] = round(total, 2)
        return pedido

    def eliminar_pedido(self, pedido_id: int):
        """Elimina un pedido y restaura stock usando el repo."""
        res = PedidosRepository.eliminar_pedido_por_id(self.db, pedido_id)
        if not res:
            return {"ok": False, "message": "Error al eliminar el pedido"}
        # res expected {'deleted': N}
        deleted = res.get("deleted") if isinstance(res, dict) else None
        return {"ok": True, "deleted": deleted}

    def pagar_pedido(self, pedido_id: int, monto: float, estado_pago: str = "Pagado"):
        """Registra un pago y actualiza estado del pedido."""
        res = PedidosRepository.pagar_pedido(self.db, pedido_id, monto, estado_pago)
        if not res:
            return {"ok": False, "message": "Error al registrar el pago"}
        if isinstance(res, dict) and res.get("status") == 0:
            return {"ok": True, "PagoID": res.get("PagoID"), "message": res.get("message")}
        return {"ok": False, "info": res}
