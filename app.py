#from flask_jwt_extended import JWTManager
#from flask_jwt_extended.exceptions import JWTExtendedException
from dotenv import load_dotenv
from flask import Flask #, jsonify
from config import Config
from apps.database import db
from flask_migrate import Migrate
from apps.routes import cliente_bp, auth_bp # Importar el Blueprint

load_dotenv()

# Inicializar Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
#app.config.from_object(Config)
app.config.from_object('config.Config')
# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Inicializar la base de datos
db.init_app(app)

# Inicializar JWT
#jwt = JWTManager(app)

#app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY

# Registrar el Blueprint
app.register_blueprint(cliente_bp, url_prefix='/')  # Para rutas generales
app.register_blueprint(auth_bp, url_prefix='/auth')  # Para autenticación


@app.route('/')
def home():
    return {"message": "API de Servicio Técnico funcionando"}

if __name__ == '__main__':
   # print(app.url_map)
    app.run(debug=True)     # ---------------------esto despues borrar------------------

print(app.url_map)
