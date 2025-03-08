import os
from flask_jwt_extended.exceptions import JWTExtendedException
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask import Flask, request, redirect, url_for
from flask_migrate import Migrate
from config import Config
from apps.database import db
from apps.routes import cliente_bp, auth_bp #logos_bp (por ahora sin utilizar) # Importar el Blueprint
from apps.monitoring import monitoreo_bp
from flask_cors import CORS
from werkzeug.utils import secure_filename

load_dotenv()

# Inicializar Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, supports_credentials=True)

UPLOAD_FOLDER = 'uploads/logos/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurar que la carpeta de uploads existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
#app.register_blueprint(logos_bp, url_prefix='/') # Para subir logos --- por ahora sin utilizar


@app.route('/')
def home():
    return {"message": "API de Servicio Técnico funcionando"}

@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    return f"File saved at {filepath}"








if __name__ == '__main__':
   # print(app.url_map)
    app.run(debug=True)     # ---------------------esto despues borrar------------------

print(app.url_map)
