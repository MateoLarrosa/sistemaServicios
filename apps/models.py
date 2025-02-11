from flask_bcrypt import generate_password_hash, check_password_hash
from apps.database import db 

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cuit_cuil = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    calle = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    provincia = db.Column(db.String(100))

from flask_bcrypt import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)  # Almacenamos el hash
    tipo_usuario = db.Column(db.String(50), nullable=False)  # Admin, Técnico, Cliente
    estado = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)

    def set_password(self, password):
        """Encripta la contraseña antes de almacenarla."""
        self.contrasena_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verifica si la contraseña es correcta."""
        return check_password_hash(self.contrasena_hash, password)


class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50), nullable=False)  # Pendiente, En Proceso, Finalizado
    fecha_creada = db.Column(db.DateTime, nullable=False)
    fecha_finalizada = db.Column(db.DateTime)
    tipo_servicio = db.Column(db.String(100), nullable=False)
    horario_inicio = db.Column(db.DateTime)
    prioridad = db.Column(db.String(50), nullable=False)  # Alta, Media, Baja
    repuestos = db.Column(db.Text)  # Lista de repuestos utilizados en la reparación

class Local(db.Model):
    __tablename__ = 'locales'
    id = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.String(20))
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)

class Tecnico(db.Model):
    __tablename__ = 'tecnicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especializacion = db.Column(db.String(100))
    disponibilidad = db.Column(db.Boolean, default=True)

class Activo(db.Model):
    __tablename__ = 'activos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_local = db.Column(db.Integer, db.ForeignKey('locales.id'))
    modelo = db.Column(db.String(50))
    marca = db.Column(db.String(50))
    logo = db.Column(db.String(255))  # Ruta o URL de la imagen del equipo
    descripcion = db.Column(db.Text)
    fue_arreglado = db.Column(db.Boolean, default=False)
    numero_serie = db.Column(db.String(100), unique=True)  # Número de serie del equipo

class FirmaServicio(db.Model):
    __tablename__ = 'firma_servicio'
    id = db.Column(db.Integer, primary_key=True)
    id_servicio = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    firma_cliente = db.Column(db.String(255))  # Ruta o archivo de la firma
    firma_tecnico = db.Column(db.String(255))
    fecha_firma = db.Column(db.DateTime, nullable=False)
    confirmacion = db.Column(db.Boolean, default=False)


