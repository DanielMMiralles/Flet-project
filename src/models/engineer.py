class Engineer:
    """Modelo para representar un ingeniero"""
    
    def __init__(self, id=None, name="", specialty="", experience=0, available=True):
        self.id = id
        self.name = name
        self.specialty = specialty
        self.experience = experience
        self.available = available
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Engineer a partir de una fila de la base de datos"""
        return cls(
            id=row["id"],
            name=row["nombre"],
            specialty=row["especialidad"],
            experience=row["experiencia"],
            available=row["disponible"] == 1
        )
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty,
            "experience": self.experience,
            "available": self.available
        }