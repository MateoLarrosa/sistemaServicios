from dotenv import load_dotenv
from flask import Flask
from config import Config
from database import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from routes import cliente_bp  # Importar el Blueprint

load_dotenv()

# Inicializar Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Inicializar la base de datos
db.init_app(app)

# Inicializar JWT
jwt = JWTManager(app)

# Registrar el Blueprint
app.register_blueprint(cliente_bp)

@app.route('/')
def home():
    return {"message": "API de Servicio Técnico funcionando"}

if __name__ == '__main__':
    app.run(debug=True)
