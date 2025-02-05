from database import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cuit_cuil = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_finalizacion = db.Column(db.DateTime)
    tipo_servicio = db.Column(db.String(100), nullable=False)
    prioridad = db.Column(db.String(50), nullable=False)
    repuestos = db.Column(db.Text)

class Tecnico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especializacion = db.Column(db.String(100))
    disponibilidad = db.Column(db.Boolean, default=True)

class Activo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(50))
    marca = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    fue_arreglado = db.Column(db.Boolean, default=False)
