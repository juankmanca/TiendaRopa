from app.db import SessionLocal
from app.repositories.carrito_repo import CarritoRepository

class CarritoService:
    def __init__(self):
        self.db = SessionLocal()

    def comprar_producto(self, data):
        cliente_id = data["cliente_id"]
        producto_id = data["producto_id"]
        cantidad = data["cantidad"]
        carrito = CarritoRepository.obtener_carrito_activo(self.db, cliente_id)
        if not carrito:
            carrito = CarritoRepository.crear_carrito(self.db, cliente_id)

        # carrito puede ser dict con CarritoID
        carrito_id = carrito.get("CarritoID") if isinstance(carrito, dict) else None
        detalle = CarritoRepository.agregar_producto(
            self.db,
            carrito_id,
            producto_id,
            cantidad,
        )

        # detalle puede devolver status/message o CarritoDetalleID
        resultado = {
            "ProductoID": producto_id,
            "Cantidad": cantidad,
            "DetalleRaw": detalle,
        }
        # Normalizar resultado simple
        if isinstance(detalle, dict):
            if detalle.get("status") == 0:
                resultado["Resultado"] = True
                resultado["CarritoDetalleID"] = detalle.get("CarritoDetalleID")
            else:
                resultado["Resultado"] = False
                resultado["Error"] = detalle.get("message")
                if detalle.get("available") is not None:
                    resultado["Available"] = detalle.get("available")
        else:
            resultado["Resultado"] = bool(detalle)

        return {"CarritoID": carrito_id, "Detalle": resultado}

    def ver_carritos_cliente(self, cliente_id: int):
        """Construye una estructura de carritos con su detalle a partir de las filas devueltas por el repo."""
        filas = CarritoRepository.obtener_carritos_con_detalle_por_cliente(self.db, cliente_id)
        if not filas:
            return []

        # Agrupar por CarritoID
        carritos = {}
        for f in filas:
            cid = f.get("CarritoID")
            if cid not in carritos:
                carritos[cid] = {
                    "CarritoID": cid,
                    "ClienteID": f.get("ClienteID"),
                    "FechaCreacion": str(f.get("FechaCreacion")) if f.get("FechaCreacion") is not None else None,
                    "Activo": bool(f.get("Activo")),
                    "Detalle": [],
                }
            # Si hay detalle
            if f.get("CarritoDetalleID") is not None:
                carritos[cid]["Detalle"].append(
                    {
                        "CarritoDetalleID": f.get("CarritoDetalleID"),
                        "ProductoID": f.get("ProductoID"),
                        "ProductoNombre": f.get("ProductoNombre"),
                        "Cantidad": int(f.get("Cantidad")) if f.get("Cantidad") is not None else None,
                        "PrecioUnitario": float(f.get("PrecioUnitario")) if f.get("PrecioUnitario") is not None else None,
                    }
                )

        # Devolver lista ordenada por CarritoID
        return [carritos[k] for k in sorted(carritos.keys())]

    def vaciar_carrito(self, cliente_id: int):
        """Vacía el carrito activo de un cliente: restaura stock y marca el carrito inactivo.

        Retorna dict con resultado y detalles del proceso.
        """
        carrito = CarritoRepository.obtener_carrito_activo(self.db, cliente_id)
        if not carrito:
            return {"ok": False, "message": "No existe carrito activo para el cliente"}

        carrito_id = carrito.get("CarritoID") if isinstance(carrito, dict) else None
        if not carrito_id:
            return {"ok": False, "message": "Carrito inválido"}

        res = CarritoRepository.vaciar_carrito_por_id(self.db, carrito_id)
        # res expected {'deleted_details': N}
        deleted = None
        if isinstance(res, dict):
            deleted = res.get("deleted_details")
        return {"ok": True, "CarritoID": carrito_id, "deleted_details": deleted}
    
