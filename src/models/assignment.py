class Assignment:
    """Modelo para representar una asignación de ingeniero a proyecto"""
    
    def __init__(self, id=None, project_id=None, engineer_id=None, start_date=None, end_date=None):
        self.id = id
        self.project_id = project_id
        self.engineer_id = engineer_id
        self.start_date = start_date
        self.end_date = end_date
    
    @classmethod
    def from_db_row(cls, row):
        """Crea un objeto Assignment a partir de una fila de la base de datos"""
        return cls(
            id=row["id"],
            project_id=row["id_proyecto"] if "id_proyecto" in row.keys() else row["id_producto"],
            engineer_id=row["id_ingeniero"],
            start_date=row["fecha_inicio"],
            end_date=row["fecha_fin"] if "fecha_fin" in row.keys() else None
        )
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "engineer_id": self.engineer_id,
            "start_date": self.start_date,
            "end_date": self.end_date
        }