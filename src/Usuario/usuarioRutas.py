#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Usuario.usuarioModelo import Usuario
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos
#   Servicios. Del componente usuarioSvosBD.py importa la clase usuarioSvos
from src.Usuario.usuarioSvosBD import UsuarioSvos
#   Servicios. Del componente seguridadSvos.py importa la clase Seg_TokenSvos
from src.Seguridad.seguridadSvos import Seg_TokenSvos

from datetime import datetime
from flask import request, current_app, Blueprint
import json

import pprint

bp_usuarios = Blueprint('usuario_blueprint', __name__)


#   =====================================================================================================
#   EndPoint /smartdoc/usuario/v1/altaUsuario. Alta de usuario (v1)
#   Clave de operacion: altaus (Alta de usuario)
#   =====================================================================================================
@bp_usuarios.route('/v1/altaUsuario', methods=['GET', 'POST'])
def altaUsuario_v1():
    argEntrada = ""
    clave_operacion = "altaus"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'    
    callUser = 'None'

    try:
        errorData = False 

        # Obtenemos el Diccionario (JSON) de los argumentos de entrada para colocarlos en la bitacora
        argEntrada = json.dumps(request.get_json())
        # Obtenemos la cadena de entrada del API (JSON) y la converttimos en un Diccionario
        request_data = request.get_json()

        # Valida si en el JSON llega la clave "nombre"
        if 'nombre' in request_data and request_data['nombre'] != '':
            argNombreCompleto = request_data['nombre']
        else:
            errorData = True 
            msgError = 'El nombre del usuario es un dato requerido'


        # Valida si en el JSON llega la clave "email"
        if 'email' in request_data and request_data['email'] != '':
            argCorreo = request_data['email']
        else:
            errorData = True 
            msgError = 'El correo electronico es un dato requerido'

        # Valida si en el JSON llega la clave "password"
        if 'password' in request_data and request_data['password'] != '':
            argClaveSecreta = request_data['password']
        else:
            errorData = True 
            msgError = 'La contraseña es un dato requerido'

        # Valida si en el JSON llega la clave "id_perfil"
        if 'id_perfil' in request_data and request_data['id_perfil'] != '':
            argPerfil = request_data['id_perfil']
        else:
            errorData = True 
            msgError = 'El perfil es un dato requerido'

        # Valida si en el JSON llega la clave "empresa"
        if 'empresa' in request_data and request_data['empresa'] != '':
            argEmpresa = request_data['empresa']
            clave_empresa = argEmpresa
        else:
            errorData = True 
            msgError = 'La empresa a la que esta asociado el usuario es un dato requerido'

        # Valida si en el JSON llega la clave "aplicacion"
        if 'aplicacion' in request_data and request_data['aplicacion'] != '':
            argAplicacion = request_data['aplicacion']
            clave_app = argAplicacion
        else:
            errorData = True 
            msgError = 'La aplicacion que solicita el servicio es un dato requerido'

        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, callUser, clave_operacion, argEntrada)

        # Se valida si se encontraron errores al validar los datos
        if (errorData):
            resp = {
                    'error': True, 
                    'mensaje': msgError
            }

            # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
            _bitacora.realizado = datetime.now()
            _bitacora.estado = False
            _bitacora.salida = json.dumps(resp)
            # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
            return (resp, 200)


        # Si el email es diferente a "jalr@digitek.mx" entra a validar el token de seguridad
        if (argCorreo != "jalr@digitek.mx"):
            # Llama al servicio de seguridad para verificar Token
            tuplaValidaToken = Seg_TokenSvos.verifica_token(request.headers)
            validaError = tuplaValidaToken[0]
            # Se valida si hay error en la autorizacion del Token
            if (validaError):
                msgError = tuplaValidaToken[1]
                resp = {
                        'error': True, 
                        'mensaje': msgError
                    }
                # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
                _bitacora.realizado = datetime.now()
                _bitacora.estado = False
                _bitacora.salida = json.dumps(resp)
                # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
                tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
                return (resp, 200)

            # Token-Autorizado. Obtenemos los datos recuperados desde el Token y los colocamos en una instancia de la clase operador
            _operador = tuplaValidaToken[1]
            _bitacora.cve_usuario = _operador.id
            _bitacora.cve_empresa = _operador.cve_empresa
        else:
            argPerfil = 1              # Id Perfil: Administrador
            _bitacora.cve_usuario = 0  # jalr@digitek.mx

        # Crea una instancia de la clase User
        _user = Usuario(None, argCorreo, argNombreCompleto, argClaveSecreta, argPerfil, argEmpresa, "true", _bitacora.cve_usuario)
        # Llama al metodo altaUsuario para dar de alta el usuario en la BBDD. La respuesta es una tupla
        tuplaAltaUsuario = UsuarioSvos.alta_usuario(_user, current_app.config)

        # Se verifica si el valor de la tupla[0] es TRUE. Error en la funcion
        if (tuplaAltaUsuario[0]):
            resp = {
                'error': True, 
                'mensaje': tuplaAltaUsuario[1]
            }
            # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
            _bitacora.realizado = datetime.now()
            _bitacora.estado = False
            _bitacora.salida = json.dumps(resp)
            # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
            resp = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
            return (resp, 200)

        resp = {
                'error': False, 
                'mensaje': 'Alta de usuario realizada exitosamente'
        }

        # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(resp)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)

        return (resp, 200)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def altaUsuario_v1 (/smartdoc/usuario/v1/altaUsuario) ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())

        msgError = str(ex)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, callUser, clave_operacion, argEntrada)
        # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
        _bitacora.realizado = datetime.now()
        _bitacora.estado = False
        _bitacora.salida = msgError
        _bitacora.err_sistema = True
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora. Error de Sistema
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        resp = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
        return (resp, 200)


#   =====================================================================================================
#   EndPoint /smartdoc/usuario/v1/validaUsuario. Autenticacion de usuario (v1)
#   Clave de operacion: login (Autenticacion de usuario)
#   =====================================================================================================
@bp_usuarios.route('/v1/validaUsuario', methods=['GET', 'POST'])
def validaUsuario_v1():
    try:
        errorData = False 
        numVersion = 1
        # Obtenemos el Diccionario (JSON) de los argumentos de entrada para colocarlos en la bitacora
        argEntrada = json.dumps(request.get_json())
        callUser = 'None'
        clave_operacion = "login"
        clave_empresa = 'login'
        clave_app = 'login'

        # Obtenenmos la cadena de entrada del API (JSON) y la converttimos en un Diccionario
        request_data = request.get_json()

        # Valida si en el JSON llega la clave "email"
        if 'email' in request_data and request_data['email'] != '':
            argCorreo = request_data['email']
        else:
            errorData = True 
            msgError = 'El correo electronico es un dato requerido'

        # Valida si en el JSON llega la clave "password"
        if 'password' in request_data and request_data['password'] != '':
            argClaveSecreta = request_data['password']
        else:
            errorData = True 
            msgError = 'La contraseña es un dato requerido'

        argVigencia = 60                        # Vigencia del Token ... 60 minutos
        # Valida si en el JSON llega la clave "vigencia"
        if 'vigencia' in request_data and request_data['vigencia'] != '':
            argVigencia = request_data['vigencia']
        

        argValidaPass = True                     # Bandera para verificar password
        # Valida si en el JSON llega la clave "validaP"
        if 'validaP' in request_data and request_data['validaP'] != '':
            argValidaPass = request_data['validaP']

        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, callUser, clave_operacion, request_data)

        # Se valida si se encontraron errores al validar los datos
        if (errorData):
            resp = {
                    'error': True, 
                    'mensaje': msgError
            }

            # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
            _bitacora.realizado = datetime.now()
            _bitacora.estado = False
            _bitacora.salida = json.dumps(resp)
            # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
            return (resp, 200)

        # Crea una instancia de la clase User
        _user = Usuario(None, argCorreo, None, argClaveSecreta, None, None, None, None, None, None, None, None)

        # Llama al metodo autentica_usuario para validar si el usuario existe en la BBDD. La respuesta es una tupla
        tuplaAutenticaUsuario = UsuarioSvos.valida_usuario(numVersion, current_app.config, _user, argValidaPass, argVigencia)

        # Se verifica si el valor de la tupla[0] es TRUE. Error en la funcion (No existe cve usuario - email)
        if (tuplaAutenticaUsuario[0]):
            resp = {
                'error': True, 
                'mensaje': tuplaAutenticaUsuario[1]
            }
            # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
            _bitacora.realizado = datetime.now()
            _bitacora.estado = False
            _bitacora.salida = json.dumps(resp)
            # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
            return (resp, 200)

        # El metodo autentica_usuario regresa la clase user actualizada con los datos del usuario validado y el token de autorizacion
        resUsuario =  tuplaAutenticaUsuario[1]
        resToken =  tuplaAutenticaUsuario[2]

        msg = 'Registro consultado correctamente '
        resp = {
                'nombre': resUsuario.fullname,
                'token': resToken,
                'error': False, 
                'mensaje': msg
        }

        # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(resp)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)

        return (resp, 200)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def validaUsuario_v1 (/smartdoc/usuario/v1/validaUsuario) ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())

        msgError = str(ex)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, callUser, clave_operacion, argEntrada)
        # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
        _bitacora.realizado = datetime.now()
        _bitacora.estado = False
        _bitacora.salida = msgError
        _bitacora.err_sistema = True
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora. Error de Sistema
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        resp = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
        return (resp, 200)


#   =====================================================================================================
#   EndPoint /smartdoc/usuario/v1/listaUsuarios. Consulta los usuarios con servicio en SamrtDoc
#   Clave de operacion: lstusu (Consulta la lista de usuarios)
#   =====================================================================================================
@bp_usuarios.route('/v1/listaUsuarios', methods=['GET', 'POST'])
def listaUsuarios_v1():
    argEntrada = ""
    clave_operacion = "lstusu"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        numVersion = 1

        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, None)

        # Llama al servicio de seguridad para verificar Token
        tuplaValidaToken = Seg_TokenSvos.verifica_token(request.headers)
        validaError = tuplaValidaToken[0]
        # Se valida si hay error en la autorizacion del Token
        if (validaError):
            msgError = tuplaValidaToken[1]
            resp = {
                    'error': True, 
                    'mensaje': msgError
                }
            # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
            _bitacora.realizado = datetime.now()
            _bitacora.estado = False
            _bitacora.salida = json.dumps(resp)
            # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
            return (resp, 200)

        # Token-Autorizado. Obtenemos los datos recuperados desde el Token y los colocamos en una instancia de la clase operador
        _operador = tuplaValidaToken[1]
        _bitacora.cve_usuario = _operador.id
        _bitacora.cve_empresa = _operador.cve_empresa

        # Llamamos al metodo lista_empresa de la clase usuarioSvosBD, que realiza la consulta para obtener los usuarios
        tuplaConsultaDatos = UsuarioSvos.lista_usuarios(numVersion, current_app.config)

        validaError = tuplaConsultaDatos[0]
        # Se valida si hay error en el resultado del metodo
        if (validaError):                                       # El metodo informa que hubo error
            msgError = tuplaConsultaDatos[1]
            ErrorSistema = tuplaConsultaDatos[2]                # Se verifica si el error es de sistema 
            if (ErrorSistema):
                _bitacora.salida = msgError
                _bitacora.err_sistema = True
                resp = {
                        'error': True, 
                        'mensaje': 'Servicio no disponible por el momento'
                    }
            else:        
                _bitacora.err_sistema = False
                resp = {
                        'error': True, 
                        'mensaje': msgError
                    }
                # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
                _bitacora.salida = json.dumps(resp)

            _bitacora.realizado = datetime.now()
            _bitacora.estado = False
            # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
            return (resp, 200)

        respuesta = tuplaConsultaDatos[1]
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        return (respuesta, 200)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def listaUsuario_v1 (/smartdoc/usuario/v1/listaUsuario ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())

        msgError = str(ex)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, None)
        # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
        _bitacora.realizado = datetime.now()
        _bitacora.estado = False
        _bitacora.salida = msgError
        _bitacora.err_sistema = True
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora. Error de Sistema
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        resp = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
        return (resp, 200)


