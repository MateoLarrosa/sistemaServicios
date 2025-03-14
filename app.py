from flask_jwt_extended.exceptions import JWTExtendedException
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask import Flask #, jsonify
from flask_migrate import Migrate
from config import Config
from apps.database import db
from apps.routes import cliente_bp, auth_bp # Importar el Blueprint
from apps.monitoring import monitoreo_bp
from flask_cors import CORS

load_dotenv()

# Inicializar Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, supports_credentials=True)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.JWT_REFRESH_TOKEN_EXPIRES

#Configuracion de cookies
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False  # True si usas HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Desactívalo por ahora

# Inicializar JWT
jwt = JWTManager(app)

#app.config.from_object(Config)
app.config.from_object('config.Config')

# Inicializar la base de datos
db.init_app(app)



# Registrar el Blueprint
app.register_blueprint(cliente_bp, url_prefix='/')  # Para rutas generales
app.register_blueprint(auth_bp, url_prefix='/auth')  # Para autenticación
app.register_blueprint(monitoreo_bp, url_prefix='/')


@app.route('/')
def home():
    return {"message": "API de Servicio Técnico funcionando"}

if __name__ == '__main__':
   # print(app.url_map)
    app.run(debug=True)     # ---------------------esto despues borrar------------------

print(app.url_map)
