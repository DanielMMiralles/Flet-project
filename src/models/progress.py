class Progress:
    """Modelo para representar el progreso de un proyecto"""
    
    def __init__(self, id=None, project_id=None, engineer_id=None, percentage=0, description="", date=None):
        self.id = id
        self.project_id = project_id
        self.engineer_id = engineer_id
        self.percentage = percentage
        self.description = description
        self.date = date
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Progress a partir de una fila de la base de datos"""
        return cls(
            id=row["id"],
            project_id=row["id_proyecto"] if "id_proyecto" in row.keys() else row["id_producto"],
            engineer_id=row["id_ingeniero"],
            percentage=row["porcentaje"],
            description=row["descripcion"] if "descripcion" in row.keys() else "",
            date=row["fecha"]
        )
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "engineer_id": self.engineer_id,
            "percentage": self.percentage,
            "description": self.description,
            "date": self.date
        }