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


### RUTAS DE INICIO Y LOGIN DE USUARIO

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

    # Verifica si el usuario existe y si la contraseña es correcta
    #if usuario and usuario.check_password(data.get('contrasena')):
        #return jsonify({"message": "Inicio de sesión exitoso", "usuario_id": usuario.id, "tipo_usuario": usuario.tipo_usuario}), 200
    if usuario and usuario.check_password(data.get('password')):
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    
    return jsonify({"error": "Credenciales inválidas"}), 401

@auth_bp.route('/')
def login_page():
    return render_template('home.html')

@auth_bp.route('/inicio', methods=['GET'])
def inicio():
    return render_template('inicioAdmin.html')  # Renderiza el archivo inicio.html










# ----------------------------------------------------------------------------------------------------------------------------------------------

### METODOS SIN UTILIZAR POR EL MOMENTO

#@auth_bp.route('/login', methods=['POST'])
#def login():
 #   """Autenticar un usuario y generar un token JWT"""
  #  data = request.get_json()
   # usuario = Usuario.query.filter_by(email=data.get('email')).first()
#
 #   if usuario and usuario.check_password(data.get('contrasena')):
  #      token = create_access_token(
   #         identity= str(usuario.id),
    #        additional_claims={"tipo": usuario.tipo_usuario})
     #   return jsonify({"access_token": token}), 200

    #return jsonify({"error": "Credenciales inválidas"}), 401

#@cliente_bp.route('/clientes', methods=['GET'])
#@jwt_required()
#def obtener_clientes():
 #   usuario_actual = get_jwt_identity()
  #  usuario_tipo = get_jwt()["tipo"]  # Obtener "tipo" de los additional_claims

#    print(f"Usuario autenticado: ID {usuario_actual}, Tipo: {usuario_tipo}")  # Debug

    # Verificar si el usuario tiene permisos de Admin
 #   if usuario_tipo != "Admin":
  #      return jsonify({"error": "No tienes permisos para acceder a esta ruta"}), 403

   # clientes = Cliente.query.all()
    #return jsonify(clientes_schema.dump(clientes)), 200


#@cliente_bp.route('/clientes', methods=['GET'])
#@jwt_required()
#def obtener_clientes():
   # print("Token recibido:", get_jwt())
    #usuario_actual = get_jwt_identity()
    #if usuario_actual["tipo"] != "Admin":
        #return jsonify({"error": "No tienes permisos para acceder a esta ruta"}), 403
 #   clientes = Cliente.query.all()
  #  return jsonify(clientes_schema.dump(clientes)), 200