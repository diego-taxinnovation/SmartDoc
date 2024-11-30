#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Usuario.usuarioModelo import Usuario
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Usuario.usuarioSvosBD import UsuarioSvos

from datetime import datetime
from flask import request, current_app, Blueprint
import json

bp_seguridad = Blueprint('seguridad_blueprint', __name__)

#   =====================================================================================================
#   EndPoint /smartdoc/seguridad/v1/tokenUsuario. Genera Token con una vigencia de n minutos, para un usuario
#   Clave de operacion: gntkus (Genera token para usuario)
#   =====================================================================================================
@bp_seguridad.route('/v1/tokenUsuario', methods=['GET', 'POST'])
def tokenUsuario_v1():
    try:
        num_version = 1
        errorData = False 
        # Obtenemos el Diccionario (JSON) de los argumentos de entrada para colocarlos en la bitacora
        argEntrada = json.dumps(request.get_json())
        callUser = 'None'
        clave_operacion = "gntkus"

        # Obtenenmos la cadena de entrada del API (JSON) y la converttimos en un Diccionario
        request_data = request.get_json()

        # Valida si en el JSON llega la clave "email"
        if 'email' in request_data and request_data['email'] != '':
            argCorreo = request_data['email']
        else:
            errorData = True 
            msgError = 'El correo electronico es un dato requerido'

        argVigencia = 60
        # Valida si en el JSON llega la clave "vigencia"
        if 'vigencia' in request_data and request_data['vigencia'] != '':
            argVigencia = request_data['vigencia']

        # Valida si en el JSON llega la clave "empresa"
        if 'empresa' in request_data and request_data['empresa'] != '':
            clave_empresa = request_data['empresa']
        else:
            errorData = True 
            msgError = 'La clave de empresa es un dato requerido'

        # Valida si en el JSON llega la clave "clave_app"
        if 'clave_app' in request_data and request_data['clave_app'] != '':
            clave_app = request_data['clave_app']
        else:
            errorData = True 
            msgError = 'La clave de la aplicacion es un dato requerido'


        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, callUser, clave_operacion, argEntrada)

        # Se valida si se encontraron errores al validar los datos
        if (errorData):
            resp = {
                    'datos': '',
                    'error': True, 
                    'mensaje': msgError
            }

            _bitacora.realizado = datetime.now()
            _bitacora.estado = False
            # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
            _bitacora.salida = json.dumps(resp)
            # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
            tuplaDEF = BitacoraSvos.alta_bitacora(current_app, _bitacora, current_app.config)
            return (resp, 200)

        # Crea una instancia de la clase User
        _user = Usuario(None, argCorreo, None, None, None, "True")
        # Llama al metodo autentica_usuario para validar si el usuario existe en la BBDD (sin validar password). La respuesta es una tupla
        tuplaAutenticaUsuario = UsuarioSvos.valida_usuario(num_version, current_app.config, _user, False, argVigencia)

        # Se verifica si el valor de la tupla[0] es TRUE. Error en la funcion (No existe cve usuario - email)
        if (tuplaAutenticaUsuario[0]):
            resp = {
                'datos': {},
                'error': True, 
                'mensaje': tuplaAutenticaUsuario[1]
            }
            # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
            _bitacora.realizado = datetime.now()
            _bitacora.estado = False
            _bitacora.salida = json.dumps(resp)
            # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
            tuplaDEF = BitacoraSvos.alta_bitacora(current_app, _bitacora, current_app.config)
            return (resp, 200)

        # El metodo autentica_usuario regresa la clase user actualizada con los datos del usuario validado y el token de autorizacion
        resUsuario =  tuplaAutenticaUsuario[1]
        resToken =  tuplaAutenticaUsuario[2]
        msg = 'Registro consultado correctamente '
        resp = {
                'nombre': resUsuario.fullname,
                'empresa': resUsuario.empresa,
                'token': resToken,
                'error': False, 
                'mensaje': msg
        }

        # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(resp)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(current_app, _bitacora, current_app.config)

        return (resp, 200)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def tokenUsuario_v1 (/smartdoc/seguridad/v1/tokenUsuario) ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())

        msgError = ex
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, callUser, clave_operacion, argEntrada)
        # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
        _bitacora.realizado = datetime.now()
        _bitacora.estado = False
        _bitacora.salida = msgError
        _bitacora.err_sistema = True
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora. Error de Sistema
        tuplaDEF = BitacoraSvos.alta_bitacora(current_app, _bitacora, current_app.config)
        resp = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
        return (resp, 200)


