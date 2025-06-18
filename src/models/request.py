class Request:
    def __init__(
        self,
        id: int = None,
        client_id: int = None,
        product_id: int = None,
        request_date: str = "",
        details: str = "",
        status: str = "pendiente"
    ):
        self.id = id
        self.client_id = client_id
        self.product_id = product_id
        self.request_date = request_date
        self.details = details
        self.status = status
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para fácil serialización"""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "product_id": self.product_id,
            "request_date": self.request_date,
            "details": self.details,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea una Solicitud desde un diccionario"""
        return cls(
            id=data.get("id"),
            client_id=data.get("client_id"),
            product_id=data.get("product_id"),
            request_date=data.get("request_date", ""),
            details=data.get("details", ""),
            status=data.get("status", "pendiente")
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea una Solicitud desde una fila de base de datos"""
        return cls(
            id=row["id"],
            client_id=row["id_cliente"],
            product_id=row["id_producto"],
            request_date=row["fecha_solicitud"],
            details=row["detalles"] if "detalles" in row.keys() else "",
            status=row["estado"]
        )