import os
import sys

# Añadir el directorio src al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import list_all_users

if __name__ == "__main__":
    print("Verificando usuarios en la base de datos...")
    list_all_users()