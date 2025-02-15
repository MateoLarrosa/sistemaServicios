""" from flask_bcrypt import generate_password_hash, check_password_hash
from apps.database import db
from sqlalchemy import ForeignKeyConstraint

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    contrasena_hash = db.Column(db.String(255, collation='Latin1_General_CI_AS'), nullable=False)
    tipoUsuario = db.Column(db.String(50, collation='Latin1_General_CI_AS'), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)
    intentosLogin = db.Column(db.Integer, default=0)
    bloqueado = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.contrasena_hash, password)

class Cliente(db.Model):
    __tablename__ = 'Clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    cuit = db.Column(db.String(20, collation='Latin1_General_CI_AS'), nullable=False, unique=True)
    mail = db.Column(db.String(100, collation='Latin1_General_CI_AS'), unique=True, nullable=False)
    telefono = db.Column(db.String(20, collation='Latin1_General_CI_AS'), nullable=False)
    calle = db.Column(db.String(255, collation='Latin1_General_CI_AS'), nullable=False)
    numero = db.Column(db.String(10, collation='Latin1_General_CI_AS'), nullable=False)
    localidad = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    provincia = db.Column(db.String(100, collation='Latin1_General_CI_AS'))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    nroActivo = db.Column(db.Integer)
    idUsuario = db.Column(db.Integer)

    __table_args__ = (
        ForeignKeyConstraint(['idUsuario'], ['Usuario.id'], ondelete='SET NULL'),
    )

class Local(db.Model):
    __tablename__ = 'Local'
    id = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.String(20, collation='Latin1_General_CI_AS'))
    nombre = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    direccion = db.Column(db.String(255, collation='Latin1_General_CI_AS'), nullable=False)
    localidad = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    provincia = db.Column(db.String(100, collation='Latin1_General_CI_AS'))
    contacto = db.Column(db.String(100, collation='Latin1_General_CI_AS'))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    id_cliente = db.Column(db.Integer)

    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['Cliente.id'], ondelete='SET NULL'),
    )

class Activo(db.Model):
    __tablename__ = 'activos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    idLocal = db.Column(db.Integer)
    modelo = db.Column(db.String(50, collation='Latin1_General_CI_AS'))
    marca = db.Column(db.String(50, collation='Latin1_General_CI_AS'))
    logo = db.Column(db.String(255, collation='Latin1_General_CI_AS'))
    descripcion = db.Column(db.Text(collation='Latin1_General_CI_AS'))
    nroSerie = db.Column(db.String(100, collation='Latin1_General_CI_AS'), unique=True)
    nroActivo = db.Column(db.Integer)
    estado = db.Column(db.String(50, collation='Latin1_General_CI_AS'))
    voltaje = db.Column(db.Float)
    poseeTierra = db.Column(db.Boolean, default=False)

    __table_args__ = (
        ForeignKeyConstraint(['idLocal'], ['local.id'], ondelete='SET NULL'),
    )

class Tecnico(db.Model):
    __tablename__ = 'tecnicos'
    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer)
    nombre = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    especializacion = db.Column(db.String(100, collation='Latin1_General_CI_AS'))
    disponibilidad = db.Column(db.Boolean, default=True)

    __table_args__ = (
        ForeignKeyConstraint(['idUsuario'], ['Usuario.id'], ondelete='SET NULL'),
    )

class OrdenDeTrabajo(db.Model):
    __tablename__ = 'ordenes_de_trabajo'
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50, collation='Latin1_General_CI_AS'), nullable=False)
    fecha_creada = db.Column(db.DateTime, nullable=False)
    fecha_finalizada = db.Column(db.DateTime)
    tipo_servicio = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    fechaInicio = db.Column(db.DateTime)
    duracion = db.Column(db.Integer)
    horaInicio = db.Column(db.Time)
    horaFin = db.Column(db.Time)
    prioridad = db.Column(db.String(50, collation='Latin1_General_CI_AS'), nullable=False)
    id_cliente = db.Column(db.Integer)
    id_tecnico = db.Column(db.Integer)
    id_local = db.Column(db.Integer)
    id_activo = db.Column(db.Integer)
    comentario = db.Column(db.Text(collation='Latin1_General_CI_AS'))
    fue_arreglado = db.Column(db.Boolean, default=False)

    __table_args__ = (
        ForeignKeyConstraint(['id_cliente'], ['clientes.id'], ondelete='SET NULL'),
        ForeignKeyConstraint(['id_tecnico'], ['tecnicos.id'], ondelete='SET NULL'),
        ForeignKeyConstraint(['id_local'], ['local.id'], ondelete='SET NULL'),
        ForeignKeyConstraint(['id_activo'], ['activos.id'], ondelete='SET NULL'),
    )

class Repuesto(db.Model):
    __tablename__ = 'repuestos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255, collation='Latin1_General_CI_AS'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    idActivo = db.Column(db.Integer)

    __table_args__ = (
        ForeignKeyConstraint(['idActivo'], ['activos.id'], ondelete='SET NULL'),
    )

class ServicioRepuesto(db.Model):
    __tablename__ = 'servicio_repuestos'
    id = db.Column(db.Integer, primary_key=True)
    id_orden_de_trabajo = db.Column(db.Integer)
    idRepuesto = db.Column(db.Integer)
    costo = db.Column(db.Float, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['id_orden_de_trabajo'], ['ordenes_de_trabajo.id'], ondelete='SET NULL'),
        ForeignKeyConstraint(['idRepuesto'], ['repuestos.id'], ondelete='SET NULL'),
    )

class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    idOrdenDeTrabajo = db.Column(db.Integer)
    tipo_tarea = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    descripcion = db.Column(db.Text(collation='Latin1_General_CI_AS'))

    __table_args__ = (
        ForeignKeyConstraint(['idOrdenDeTrabajo'], ['ordenes_de_trabajo.id'], ondelete='SET NULL'),
    )

class HorarioTecnico(db.Model):
    __tablename__ = 'horarios_tecnicos'
    id = db.Column(db.Integer, primary_key=True)
    tecnicoId = db.Column(db.Integer)
    diaSemana = db.Column(db.DateTime, nullable=False)
    horaInicio = db.Column(db.Time, nullable=False)
    horaFin = db.Column(db.Time, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['tecnicoId'], ['tecnicos.id'], ondelete='SET NULL'),
    )



 """

from flask_bcrypt import generate_password_hash, check_password_hash
from apps.database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    contrasena_hash = db.Column(db.String(255, collation='Latin1_General_CI_AS'), nullable=False)
    tipoUsuario = db.Column(db.String(50, collation='Latin1_General_CI_AS'), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime)
    intentosLogin = db.Column(db.Integer, default=0)
    bloqueado = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.contrasena_hash, password)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    cuit = db.Column(db.String(20, collation='Latin1_General_CI_AS'), nullable=False, unique=True)
    mail = db.Column(db.String(100, collation='Latin1_General_CI_AS'), unique=True, nullable=False)
    telefono = db.Column(db.String(20, collation='Latin1_General_CI_AS'), nullable=False)
    calle = db.Column(db.String(255, collation='Latin1_General_CI_AS'), nullable=False)
    numero = db.Column(db.String(10, collation='Latin1_General_CI_AS'), nullable=False)
    localidad = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    provincia = db.Column(db.String(100, collation='Latin1_General_CI_AS'))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    razonSocial = db.Column(db.String(255, collation='Latin1_General_CI_AS'), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))

class Local(db.Model):
    __tablename__ = 'locales'
    id = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.String(20, collation='Latin1_General_CI_AS'))
    nombre = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    direccion = db.Column(db.String(255, collation='Latin1_General_CI_AS'), nullable=False)
    localidad = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    provincia = db.Column(db.String(100, collation='Latin1_General_CI_AS'))
    contacto = db.Column(db.String(100, collation='Latin1_General_CI_AS'))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='SET NULL'))

class Tecnico(db.Model):
    __tablename__ = 'tecnicos'
    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
    nombre = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    especializacion = db.Column(db.String(100, collation='Latin1_General_CI_AS'))
    disponibilidad = db.Column(db.Boolean, default=True)

class HorarioTecnico(db.Model):
    __tablename__ = 'horarios_tecnicos'
    id = db.Column(db.Integer, primary_key=True)
    tecnicoId = db.Column(db.Integer, db.ForeignKey('tecnicos.id', ondelete='SET NULL'))
    fecha = db.Column(db.Date, nullable=False)  # Cambié de DateTime a Date para diferenciar días exactos
    horaInicio = db.Column(db.Time, nullable=False)
    horaFin = db.Column(db.Time, nullable=False)

class OrdenDeTrabajo(db.Model):
    __tablename__ = 'ordenes_de_trabajo'
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(50, collation='Latin1_General_CI_AS'), nullable=False)
    fecha_creada = db.Column(db.DateTime, nullable=False)
    fecha_finalizada = db.Column(db.DateTime)
    tipo_servicio = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    fechaInicio = db.Column(db.DateTime)
    duracion = db.Column(db.Integer)
    horaInicio = db.Column(db.Time)
    horaFin = db.Column(db.Time)
    prioridad = db.Column(db.String(50, collation='Latin1_General_CI_AS'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='SET NULL'))
    id_tecnico = db.Column(db.Integer, db.ForeignKey('tecnicos.id', ondelete='SET NULL'))
    id_local = db.Column(db.Integer, db.ForeignKey('locales.id', ondelete='SET NULL'))
    id_activo = db.Column(db.Integer, db.ForeignKey('activos.id', ondelete='SET NULL'))
    comentario = db.Column(db.Text(collation='Latin1_General_CI_AS'))
    fue_arreglado = db.Column(db.Boolean, default=False)

class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    idOrdenDeTrabajo = db.Column(db.Integer, db.ForeignKey('ordenes_de_trabajo.id', ondelete='SET NULL'))
    tipo_tarea = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    descripcion = db.Column(db.Text(collation='Latin1_General_CI_AS'))

class Activo(db.Model):
    __tablename__ = 'activos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100, collation='Latin1_General_CI_AS'), nullable=False)
    idLocal = db.Column(db.Integer, db.ForeignKey('locales.id', ondelete='SET NULL'))
    modelo = db.Column(db.String(50, collation='Latin1_General_CI_AS'))
    marca = db.Column(db.String(50, collation='Latin1_General_CI_AS'))
    logo = db.Column(db.String(255, collation='Latin1_General_CI_AS'))
    descripcion = db.Column(db.Text(collation='Latin1_General_CI_AS'))
    nroSerie = db.Column(db.String(100, collation='Latin1_General_CI_AS'), unique=True)
    nroActivo = db.Column(db.Integer)
    estado = db.Column(db.String(50, collation='Latin1_General_CI_AS'))
    voltaje = db.Column(db.Float)
    poseeTierra = db.Column(db.Boolean, default=False)

class Repuesto(db.Model):
    __tablename__ = 'repuestos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255, collation='Latin1_General_CI_AS'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    idActivo = db.Column(db.Integer, db.ForeignKey('activos.id', ondelete='SET NULL'))

class ServicioRepuesto(db.Model):
    __tablename__ = 'servicio_repuestos'
    id = db.Column(db.Integer, primary_key=True)
    id_orden_de_trabajo = db.Column(db.Integer, db.ForeignKey('ordenes_de_trabajo.id', ondelete='SET NULL'))
    idRepuesto = db.Column(db.Integer, db.ForeignKey('repuestos.id', ondelete='SET NULL'))
    costo = db.Column(db.Float, nullable=False)

class FirmaOrdenDeTrabajo(db.Model):
    __tablename__ = 'firmaOrdenDeTrabajo'
    
    id = db.Column(db.Integer, primary_key=True)
    idOrdenDeTrabajo = db.Column(db.Integer, db.ForeignKey('ordenes_de_trabajo.id', ondelete='SET NULL'))
    firmaCliente = db.Column(db.LargeBinary, nullable=False)  # Almacena firma como binario
    firmaTecnico = db.Column(db.LargeBinary, nullable=False)
    fechaFirma = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    confirmacion = db.Column(db.Boolean, nullable=False, default=False)
    comentario = db.Column(db.Text(collation='Latin1_General_CI_AS'), nullable=True)