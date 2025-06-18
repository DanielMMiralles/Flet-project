class Admin:
    def __init__(
        self,
        id: int = None,
        user_id: int = None,
        name: str = "",
        email: str = ""
    ):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.email = email
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para fácil serialización"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un Administrador desde un diccionario"""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            name=data.get("name", ""),
            email=data.get("email", "")
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un Administrador desde una fila de base de datos"""
        return cls(
            id=row["id"],
            user_id=row["id_usuario"] if "id_usuario" in row.keys() else None,
            name=row["nombre"] if "nombre" in row.keys() else "",
            email=row["email"] if "email" in row.keys() else ""
        )