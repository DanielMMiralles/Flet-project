class Client:
    def __init__(
        self,
        id: int = None,
        user_id: int = None,
        name: str = "",
        email: str = "",
        phone: str = ""
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para fácil serialización"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un Cliente desde un diccionario"""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", "")
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un Cliente desde una fila de base de datos"""
        return cls(
            id=row["id"],
            user_id=row["id_usuario"],
            name=row["nombre"],
            email=row["email"] if "email" in row.keys() else "",
            phone=row["telefono"] if "telefono" in row.keys() else ""
        )