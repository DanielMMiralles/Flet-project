class Assignment:
    def __init__(
        self,
        id: int = None,
        engineer_id: int = None,
        product_id: int = None,
        start_date: str = "",
        end_date: str = None
    ):
        self.id = id
        self.engineer_id = engineer_id
        self.product_id = product_id
        self.start_date = start_date
        self.end_date = end_date
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para fácil serialización"""
        return {
            "id": self.id,
            "engineer_id": self.engineer_id,
            "product_id": self.product_id,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea una Asignación desde un diccionario"""
        return cls(
            id=data.get("id"),
            engineer_id=data.get("engineer_id"),
            product_id=data.get("product_id"),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date")
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea una Asignación desde una fila de base de datos"""
        return cls(
            id=row["id"],
            engineer_id=row["id_ingeniero"],
            product_id=row["id_producto"],
            start_date=row["fecha_inicio"],
            end_date=row["fecha_fin"] if "fecha_fin" in row.keys() and row["fecha_fin"] else None
        )