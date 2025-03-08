import re
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, create_refresh_token
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, make_response, current_app
from apps.database import db
from apps.models import Cliente, Usuario, Tecnico, Local, Activo, OrdenDeTrabajo, solicitudServicio
from apps.schemas import cliente_schema, clientes_schema
from utils import admin_required, registrar_evento_auditoria, validar_cuit, validar_mail
from datetime import datetime, timedelta
from apps.monitoring import usuarios_activos, time, monitoreo_bp


cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/auth')
def login_page():

    ### LA LOGICA PARA ELIMINAR LA COOKIEE TODAVIA NO FUNCIONA. SIGUE SIN MATAR LA SESION.


    # Verificar si la cookie ya fue eliminada
    if request.cookies.get('access_token_cookie'):
        # Eliminar la cookie solo si existe
        response = make_response(render_template('home.html'))
        #response.set_cookie('access_token_cookie', '', expires=0, httponly=True, samesite='Strict')
        response.delete_cookie('access_token')
    else:
        # Si la cookie ya fue eliminada, simplemente renderiza la página
        response = make_response(render_template('home.html'))

    # Configurar encabezados para evitar el almacenamiento en caché
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response
    #return render_template('home.html')


@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
@jwt_required()
@admin_required
def obtener_cliente(id):
    """Obtener información de un cliente, restringiendo acceso según el rol"""

    claims = get_jwt() # OBTENGO UN DICCIONARIO CON TIPO USUARIO
    usuario_id  = get_jwt_identity() # OBTENGO EL ID COMO STRING

    print(f"Claims del token: {claims}")  # 🔍 Depuración
    print(f"ID del usuario autenticado: {usuario_id}")

    if claims.get("tipoUsuario") != "admin" and int(usuario_id) != id:
        return jsonify({"error": "Acceso no autorizado"}), 403  # 403 Forbidden

    cliente = Cliente.query.get(id)
    
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    return jsonify(cliente_schema.dump(cliente)), 200



@cliente_bp.route('/clientes', methods=['POST'])
@jwt_required()
@admin_required 
def crear_cliente():
    data = request.get_json()
    #errors = cliente_schema.validate(data)

    campos_requeridos = ["nombre", "cuit", "mail", "telefono", "calle", "numero", "localidad"]
    for campo in campos_requeridos:
        if campo not in data or not data[campo].strip():
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    """ if errors:
        return jsonify(errors), 400  # Devuelve los errores si los datos no son válidos """
    
    # Validar formato del email
    if not validar_mail(data["mail"]):
        return jsonify({"error": "Formato de email inválido"}), 400

    # Validar CUIT
    if not validar_cuit(data["cuit"]):
        return jsonify({"error": "Formato de CUIT inválido (debe contener solo 11 números)"}), 400

    # Validar que el CUIT y el email no existan ya en la BD
    if Cliente.query.filter_by(cuit=data["cuit"]).first():
        return jsonify({"error": "El CUIT ya está registrado"}), 409
    if Cliente.query.filter_by(mail=data["mail"]).first():
        return jsonify({"error": "El email ya está registrado"}), 409

    nuevo_cliente = Cliente(
        nombre=data.get('nombre'),
        cuit=data.get('cuit'),
        mail=data.get('mail'),  # Antes era email
        telefono=data.get('telefono'),
        calle=data.get('calle'),
        numero=data.get('numero'),
        localidad=data.get('localidad'),
        provincia=data.get('provincia'),
        latitud=data.get('latitud'),
        longitud=data.get('longitud'),
        razonSocial=data.get('razonSocial'),
        idUsuario=data.get('idUsuario')  # Relación con la tabla Usuario
    )
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify({"message": "Cliente creado exitosamente", "id": nuevo_cliente.id}), 201

@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    """Actualizar un cliente existente"""
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()

    # Validar formato del email si se proporciona
    if "mail" in data and data["mail"] and not validar_mail(data["mail"]):
        return jsonify({"error": "Formato de email inválido"}), 400

    # Validar CUIT si se proporciona
    if "cuit" in data and data["cuit"]:
        if not validar_cuit(data["cuit"]):
            return jsonify({"error": "Formato de CUIT inválido (debe contener solo 11 números)"}), 400

        # **Asegurar que el CUIT no esté en uso por otro cliente**
        cliente_existente = Cliente.query.filter(Cliente.cuit == data["cuit"], Cliente.id != id).first()
        if cliente_existente:
            return jsonify({"error": "El CUIT ya está en uso por otro cliente"}), 409

    # Validar que el nuevo email no pertenezcan a otro cliente
    if "mail" in data and data["mail"] != cliente.mail:
        if Cliente.query.filter_by(mail=data["mail"]).first():
            return jsonify({"error": "El email ya está en uso por otro cliente"}), 409

    cliente.nombre = data.get('nombre', cliente.nombre)
    cliente.cuit = data.get('cuit', cliente.cuit)
    cliente.mail = data.get('mail', cliente.mail)  # Antes era email
    cliente.telefono = data.get('telefono', cliente.telefono)
    cliente.calle = data.get('calle', cliente.calle)
    cliente.numero = data.get('numero', cliente.numero)
    cliente.localidad = data.get('localidad', cliente.localidad)
    cliente.provincia = data.get('provincia', cliente.provincia)
    cliente.latitud = data.get('latitud', cliente.latitud)
    cliente.longitud = data.get('longitud', cliente.longitud)
    cliente.razonSocial = data.get('razonSocial', cliente.razonSocial)
    cliente.idUsuario = data.get('idUsuario', cliente.idUsuario)

    db.session.commit()
    return jsonify({"message": "Cliente actualizado exitosamente"}), 200

@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    """Eliminar un cliente"""
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado exitosamente"}), 200


### RUTAS DE INICIO Y LOGIN DE USUARIO + FUNCIONES PARA VERIFICAR DATOS --------------------------------------------------------------------

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar un nuevo usuario"""
    data = request.get_json()

    # Validar que los datos obligatorios estén presentes
    if not data.get('nombreUsuario') or not data.get('password'):
        return jsonify({"error": "Nombre de usuario y contraseña son requeridos"}), 400

    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(nombreUsuario=data['nombreUsuario']).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    # Crear nuevo usuario con los datos proporcionados
    nuevoUsuario = Usuario(
        nombreUsuario=data['nombreUsuario'],
        tipoUsuario=data.get('tipoUsuario', 'Cliente')  # Default: 'Cliente'
    )
    nuevoUsuario.set_password(data['password'])  # Hashear la contraseña

    # Guardar en la base de datos
    db.session.add(nuevoUsuario)
    db.session.commit()
    
    return jsonify({"message": "Usuario registrado exitosamente"}), 201




## REFRESH TOKEN
ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Expira en 15 minutos
REFRESH_TOKEN_EXPIRES = timedelta(days=7)

## VARIABLES PARA EL CONTROL DE LOGIN FORZADO
MAX_INTENTOS_LOGIN = 5
TIEMPO_BLOQUEO_MINUTOS = 10

@auth_bp.route('/login', methods=['POST'])
def login():
    """Autenticar un usuario con protección contra fuerza bruta y refresh token"""
    print("Hasta aca llegue ok")

    username = request.form['nombreUsuario']
    password = request.form['password']

    id_cliente = None
    id_tecnico = None

    if not username or not password:
        return respuesta_con_auditoria(
            401, 
            "Error al iniciar sesión, faltó completar un campo", 
            id_caso=2
        )

    usuario = Usuario.query.filter_by(nombreUsuario=username).first()
    print(f"Usuario encontrado: {usuario}")  # Verifica si se encontró un usuario
    
    if not usuario:
        return respuesta_con_auditoria(
            401, 
            f"No existe nombre de usuario ingresado = '{username}'", 
            id_caso=2
        )

    # Identificar si es Cliente o Técnico (el Admin queda NULL)
    if usuario.tipoUsuario == "Cliente":
        cliente = Cliente.query.filter_by(idUsuario=usuario.id).first()
        if cliente:
            id_cliente = cliente.id

    elif usuario.tipoUsuario == "Tecnico":
        tecnico = Tecnico.query.filter_by(idUsuario=usuario.id).first()
        if tecnico:
            id_tecnico = tecnico.id

    # Verificar si la cuenta está bloqueada
    if usuario.bloqueado:
        tiempo_desbloqueo = usuario.ultimo_acceso + timedelta(minutes=TIEMPO_BLOQUEO_MINUTOS)
        if datetime.utcnow() < tiempo_desbloqueo:
            return respuesta_con_auditoria(
                403, 
                f"Usuario {usuario.id} intentó iniciar sesión pero está bloqueado", 
                id_caso=2, 
                usuario=usuario, 
                id_cliente=id_cliente, 
                id_tecnico=id_tecnico
            )
        else:
            usuario.bloqueado = False  # Desbloquear si ya pasó el tiempo
            usuario.intentosLogin = 0  # Reiniciar intentos fallidos

    # Verificar la contraseña
    if usuario.check_password(password):
        usuario.intentosLogin = 0  # Reiniciar intentos fallidos
        usuario.ultimo_acceso = datetime.utcnow()

        # Generar access token y refresh token
        accessToken = create_access_token(
            identity=str(usuario.id),
            additional_claims={"tipoUsuario": usuario.tipoUsuario, "nombreUsuario": usuario.nombreUsuario},
            expires_delta=ACCESS_TOKEN_EXPIRES
        )

        print(f"Access Token: {accessToken}")  # Log para ver el access token

        # Registrar al usuario como activo en el monitoreo
        usuarios_activos[str(usuario.id)] = time.time()

        refreshToken = create_refresh_token(
            identity=str(usuario.id),
            additional_claims={"tipoUsuario": usuario.tipoUsuario},
            expires_delta=REFRESH_TOKEN_EXPIRES
        )

        print(f"Refresh Token: {refreshToken}")  # Log para ver el access token

        db.session.commit()

        # 🔹 **Registrar en auditoría**
        registrar_evento_auditoria(
            id_caso=1, 
            id_usuario=usuario.id, 
            id_cliente=id_cliente,
            id_tecnico=id_tecnico,
            detalle=f"Inicio de sesión exitoso para {usuario.nombreUsuario}"
        )

        if usuario.tipoUsuario == "Admin":

            response = make_response(redirect(url_for('auth.inicioAdmin')))
            response.set_cookie('access_token_cookie', accessToken, httponly=True, secure=False)  # Cambia `secure=True` si usas HTTPS
            return response
        
        elif usuario.tipoUsuario == "Cliente":

            response = make_response(redirect(url_for('auth.inicioCliente')))
            response.set_cookie('access_token_cookie', accessToken, httponly=True, secure=False)  # Cambia `secure=True` si usas HTTPS
            return response
        
        elif usuario.tipoUsuario == "Tecnico":

            response = make_response(redirect(url_for('auth.inicioTecnico')))
            response.set_cookie('access_token_cookie', accessToken, httponly=True, secure=False)  # Cambia `secure=True` si usas HTTPS
            return response

    # Incrementar intentos fallidos y bloquear si es necesario
    usuario.intentosLogin += 1
    if usuario.intentosLogin >= MAX_INTENTOS_LOGIN:
        usuario.bloqueado = True
        usuario.ultimo_acceso = datetime.utcnow()  # Guardamos el momento del bloqueo
        db.session.commit()
        return respuesta_con_auditoria(
            403, 
            f"Usuario {usuario.id} fue bloqueado por {TIEMPO_BLOQUEO_MINUTOS} minutos", 
            id_caso=2, 
            usuario=usuario, 
            id_cliente=id_cliente, 
            id_tecnico=id_tecnico
        )

    db.session.commit()

    return respuesta_con_auditoria(
        401, 
        "Credenciales inválidas", 
        id_caso=2, 
        usuario=usuario, 
        id_cliente=id_cliente, 
        id_tecnico=id_tecnico
    )


def respuesta_con_auditoria(codigo_http, mensaje, id_caso, usuario=None, id_cliente=None, id_tecnico=None):
    """Función para registrar en auditoría antes de devolver la respuesta"""
    registrar_evento_auditoria(
        id_caso=id_caso,
        id_usuario=getattr(usuario, 'id', None),
        id_cliente=id_cliente,
        id_tecnico=id_tecnico,
        detalle=mensaje
    )
    return jsonify({"error": mensaje}), codigo_http


### RUTAS PARA REDIRIGIR A PAGINAS/TEMPLATES ----------------------------------------------------------------------------------

@auth_bp.route('/pruebaPostman')
def pruebaPostman():
    return render_template('pruebaPostman.html')

# RUTAS PARA EL HOME  QUE DERIVAN EN EL INICIO SEGUN EL USUARIO
@auth_bp.route('/inicioAdmin', methods=['GET','POST'])

@jwt_required(locations=["cookies"])
@admin_required
def inicioAdmin():

     current_user = get_jwt()
     return render_template('inicio.html', userType=current_user['tipoUsuario'], userName = current_user['nombreUsuario'])

@auth_bp.route('/inicioCliente', methods=['GET','POST'])

@jwt_required(locations=["cookies"])
def inicioCliente():

    current_user = get_jwt()
    return render_template('inicio.html', userType=current_user['tipoUsuario'], userName = current_user['nombreUsuario'])

@auth_bp.route('/inicioTecnico', methods=['GET','POST'])

@jwt_required(locations=["cookies"])
def inicioTecnico():

    current_user = get_jwt()
    return render_template('inicio.html', userType=current_user['tipoUsuario'], userName = current_user['nombreUsuario'])




######### SOLICITUD SERVICIO TECNICO -----------------------------------------------------------------------


@auth_bp.route('/solicitudServicio', methods=['GET'])
@jwt_required(locations=["cookies"])
def solicitudServicio():
    return render_template('solicitudServicio.html')  # Renderiza el archivo solicitudServicio.html


@auth_bp.route('/registrarSolicitudServicio', methods=['POST'])
@jwt_required(locations=["cookies"])
def registrarSolicitudServicio():

    data = request.form

    """ cliente = Cliente(
        nro_Cliente = request.form['nroCliente'],
        razon_social = request.form['razonSocial'],
    ) """

    cliente = Cliente.query.filter_by(idUsuario=get_jwt_identity()).first()

    nroClienteBD = cliente.nroCliente
    razonSocialBD = cliente.razonSocial

    if nroClienteBD == request.form['nroCliente'] and razonSocialBD == request.form['razonSocial']:

        local = Local(
            horarioAtencion = request.form['horarioAtencion'],
            direccion = request.form['calle'],
            entreCalle = request.form['entreCalle'],
            localidad = request.form['localidad'],
            provincia = request.form['provincia'],
            latitud = 0,  ## ver como llenar, por el momento 0
            longitud = 0, ## ver como llear, por el momento 0
            contacto = request.form['contactoPdv'],
            telefono = request.form['telefono'],
            nombre = request.form['nombrePdv'],
        )

        Activo(
            nroActivo = request.form['nroActivo'],
            marca = request.form['marca'],
            modelo = request.form['modelo'],
            nroSerie = request.form['nroSerie'],
            logo = request.form['logo'],
            falla = request.form['falla'],
        )
    else:
        return jsonify({"error": "Los datos ingresados no coinciden con los datos del cliente"}), 400
































### Otras rutas

@auth_bp.route('/redireccionar', methods=['GET'])
@jwt_required()
def redireccionar():
    """Redirige a cada usuario según su tipo después del login"""
    claims = get_jwt()
    tipo_usuario = claims.get("tipoUsuario", "Cliente")  # Si no se encuentra, por defecto es Cliente

    if tipo_usuario == "Admin":
        return redirect(url_for('auth_bp.inicio'))
    elif tipo_usuario == "Cliente":
        return redirect(url_for('auth_bp.misServicios'))  # Si más adelante necesitas una vista específica
    elif tipo_usuario == "Tecnico":
        return redirect(url_for('auth_bp.inicio'))
    
    # Si el tipo de usuario no está definido, redirigir al login
    return redirect(url_for('auth_bp.login_page'))

## ------------------- NUEVA RUTA PARA GENERAR EL REFRESH TOKEN

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Solo permite el uso del Refresh Token
def refresh():
    """Generar un nuevo Access Token usando el Refresh Token"""
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    nuevo_access_token = create_access_token(
        identity=usuario_id,
        additional_claims={"tipoUsuario": usuario.tipoUsuario, "nombreUsuario": usuario.nombreUsuario},  # Usar el tipo de usuario real
        expires_delta=timedelta(minutes=15)
    )

    return jsonify({"access_token": nuevo_access_token}), 200