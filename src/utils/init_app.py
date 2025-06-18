from utils.setup_db import setup_database

def initialize_application():
    """Inicializa la aplicación configurando la base de datos y otros recursos necesarios"""
    print("Inicializando aplicación...")
    setup_database()
    print("Aplicación inicializada correctamente.")