class Product:
    def __init__(
        self,
        id: int = None,
        name: str = "",
        description: str = "",
        days: int = 0,
        engineers: int = 0,
        image: str = "",
        status: str = "propuesta",
        client_id: int = None,
        requirements: str = ""
    ):
        self.id = id
        self.name = name
        self.description = description
        self.days = days
        self.engineers = engineers
        self.image = image
        self.status = status
        self.client_id = client_id
        self.requirements = requirements

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para fácil serialización"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "days": self.days,
            "engineers": self.engineers,
            "image": self.image,
            "status": self.status,
            "client_id": self.client_id,
            "requirements": self.requirements
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crea un Producto desde un diccionario"""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            description=data.get("description", ""),
            days=data.get("days", 0),
            engineers=data.get("engineers", 0),
            image=data.get("image", ""),
            status=data.get("status", "propuesta"),
            client_id=data.get("client_id"),
            requirements=data.get("requirements", "")
        )
    
    @classmethod
    def from_db_row(cls, row: tuple):
        """Crea un Producto desde una fila de base de datos"""
        return cls(
            id=row[0],                # id -> id
            name=row[1],              # nombre -> name
            description=row[5],       # descripcion -> description
            days=row[2],              # dias -> days
            engineers=row[3],         # cantidad_ing -> engineers
            image=row[4],             # imagen -> image
            status="activo",          # valor por defecto
            client_id=None,           # valor por defecto
            requirements=""           # valor por defecto
        )
    