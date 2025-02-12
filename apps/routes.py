#from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import Blueprint, request, jsonify, render_template
from apps.database import db
from apps.models import Cliente, Usuario
from apps.schemas import cliente_schema, clientes_schema

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/auth')

def login_page():
    return render_template('home.html')

@cliente_bp.route('/clientes', methods=['GET'])
#@jwt_required()
def obtener_clientes():
    clientes = Cliente.query.all()
    return jsonify(clientes_schema.dump(clientes)), 200

@cliente_bp.route('/clientes', methods=['POST'])
def crear_cliente():
    data = request.get_json()
    errors = cliente_schema.validate(data)

    if errors:
        return jsonify(errors), 400  # Devuelve los errores si los datos no son válidos
    
    nuevo_cliente = Cliente(
        nombre=data.get('nombre'),
        cuit_cuil=data.get('cuit_cuil'),
        email=data.get('email'),
        telefono=data.get('telefono'),
        direccion=data.get('direccion')
    )
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify({"message": "Cliente creado exitosamente"}), 201

@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()
    cliente.nombre = data.get('nombre', cliente.nombre)
    cliente.cuit_cuil = data.get('cuit_cuil', cliente.cuit_cuil)
    cliente.email = data.get('email', cliente.email)
    cliente.telefono = data.get('telefono', cliente.telefono)
    cliente.direccion = data.get('direccion', cliente.direccion)

    db.session.commit()
    return jsonify({"message": "Cliente actualizado exitosamente"}), 200

@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado exitosamente"}), 200


### RUTAS DE INICIO Y LOGIN DE USUARIO --------------------------------------------------------------------

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar un nuevo usuario"""
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        tipo_usuario=data.get('tipo_usuario', 'Cliente')
    )
    nuevo_usuario.set_password(data['password'])

    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify({"message": "Usuario registrado exitosamente"}), 201



@auth_bp.route('/login', methods=['POST'])
def login():
    """Autenticar un usuario sin generar un token"""
    data = request.get_json()
    print(f"Datos recibidos: {data}") # Log para ver los datos en consola ----------

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    usuario = Usuario.query.filter_by(email=data.get('email')).first()
    print(f"Usuario encontrado: {usuario}")  # Verifica si se encontró un usuario ---------
    
    if usuario and usuario.check_password(data.get('password')):
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    
    return jsonify({"error": "Credenciales inválidas"}), 401



### RUTAS PARA REDIRIGIR A PAGINAS/TEMPLATES ----------------------------------------------------------------------------------

@auth_bp.route('/')
def login_page():
    return render_template('home.html')


# RUTAS PARA EL HOME  QUE DERIVAN EN EL INICIO SEGUN EL USUARIO
@auth_bp.route('/inicioAdmin', methods=['GET'])
def inicioAdmin():
    return render_template('inicioAdmin.html')  # Renderiza el archivo inicioAdmin.html

@auth_bp.route('/inicioTecnico', methods=['GET'])
def inicioTecnico():
    return render_template('inicioTecnico.html')  # Renderiza el archivo inicioTecnico.html

@auth_bp.route('/inicioCliente', methods=['GET'])
def inicioCliente():
    return render_template('inicioCliente.html')  # Renderiza el archivo inicioCliente.html



# RUTAS PARA EL INICIO DEL ADMINISTRADOR
@auth_bp.route('/misServicios', methods=['GET'])
def misServicios():
    return render_template('misServicios.html')  # Renderiza el archivo serviciosAdmin.html

@auth_bp.route('/gestionDeClientes', methods=['GET'])
def gestionDeClientes():
    return render_template('gestionDeClientes.html')  # Renderiza el archivo gestionDeClientes.html

@auth_bp.route('/gestionDeTecnicos', methods=['GET'])
def gestionDeTecnicos():
    return render_template('gestionDeTecnicos.html')  # Renderiza el archivo gestionDeTecnicos.html