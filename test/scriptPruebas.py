#from app import db, app
#from sqlalchemy.sql import text

#from flask_jwt_extended import create_access_token
#from datetime import timedelta
#from app import app
#from config import Config
#app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
#with app.app_context():
    #try:
        # Realiza una consulta básica con el objeto text
        #db.session.execute(text('SELECT 1'))
        #print("Conexión exitosa a la base de datos.")
   # except Exception as e:
     #   print(f"Error al conectar a la base de datos: {e}")


import sys
import os

# Agregar el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Ahora importa utils
from utils import cargar_casos_auditoria
from app import app

with app.app_context():
  cargar_casos_auditoria()
