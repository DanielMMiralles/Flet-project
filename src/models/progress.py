class Progress:
    def __init__(
        self,
        id: int = None,
        product_id: int = None,
        engineer_id: int = None,
        date: str = "",
        description: str = "",
        percentage: int = 0
    ):
        self.id = id
        self.product_id = product_id
        self.engineer_id = engineer_id
        self.date = date
        self.description = description
        self.percentage = percentage
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para fácil serialización"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "engineer_id": self.engineer_id,
            "date": self.date,
            "description": self.description,
            "percentage": self.percentage
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un Avance desde un diccionario"""
        return cls(
            id=data.get("id"),
            product_id=data.get("product_id"),
            engineer_id=data.get("engineer_id"),
            date=data.get("date", ""),
            description=data.get("description", ""),
            percentage=data.get("percentage", 0)
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un Avance desde una fila de base de datos"""
        return cls(
            id=row["id"],
            product_id=row["id_producto"],
            engineer_id=row["id_ingeniero"],
            date=row["fecha"],
            description=row["descripcion"],
            percentage=row["porcentaje"]
        )