class User:
    def __init__(
        self,
        id: int = None,
        username: str = "",
        password: str = "",
        role: str = ""
    ):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para fácil serialización"""
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crea un Usuario desde un diccionario"""
        return cls(
            id=data.get("id"),
            username=data.get("username", ""),
            password=data.get("password", ""),
            role=data.get("role", "")
        )
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un Usuario desde una fila de base de datos"""
        return cls(
            id=row["id"],
            username=row["usuario"],
            password=row["password"],
            role=row["rol"]
        )