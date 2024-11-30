#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Empresa.empresaModelo import Empresa
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Utilerias.utileriaModelo import Operador
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos
#   Servicios. Del componente EmpresaServicios.py importa la clase EmpresaSvos
from src.Empresa.empresaSvosBD import EmpresaSvos
#   Servicios. Del componente seguridadSvos.py importa la clase Seg_TokenSvos
from src.Seguridad.seguridadSvos import Seg_TokenSvos

#   Servicios. Del componente SeguridadServicios.py importa la clase TokenSvos
#from app.admin.Servicios.SeguridadServicios import TokenSvos

from datetime import datetime
from flask import request, current_app, jsonify, Blueprint
import json

bp_empresas = Blueprint('empresa_blueprint', __name__)

#   =====================================================================================================
#   EndPoint /smartdoc/empresa/v1/test. Prueba de endpoint en la App SmartDOC
#   =====================================================================================================
@bp_empresas.route('/v1/test', methods=['GET', 'POST'])
def test():
    try: 
        respuesta = {
                'error': False, 
                'mensaje': 'Test ejecutado correctamente'
            }
        return (respuesta, 200)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def test (/smartdoc/test ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())

        respuesta = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
        return (respuesta, 200)


#   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#   Funcion para validar los datos de entrada del endpoint/smartdoc/v1/alta-empresa
#   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#def altaEmpresa_validaciones(argBitacora, argDatosEntrada, argVersion=0):
def altaEmpresa_validaciones(argDatosEntrada, argVersion=1):
    # Establece los valores de default para la bitacora
    try:
        errorData = False
        msgError = ''

        # Valida si en el JSON llega la clave "cve_empresa"
        if 'cve_empresa' in argDatosEntrada and argDatosEntrada['cve_empresa'] != '':
            clave_empresa = argDatosEntrada['cve_empresa']
        else:
            errorData = True 
            msgError = 'La clave de la empresa es un dato requerido'
        
        # Valida si en el JSON llega la clave "nombre"
        if 'nombre' in argDatosEntrada and argDatosEntrada['nombre'] != '':
            nombre = argDatosEntrada['nombre']
        else:
            errorData = True 
            msgError = 'El nombre de la empresa es un dato requerido'

        # Valida si en el JSON llega la clave "observaciones"
        if 'observaciones' in argDatosEntrada:
            observaciones = argDatosEntrada['observaciones']
        else:
            errorData = True 
            msgError = 'Las observaciones de la empresa es un dato requerido'

        # Valida si en el JSON llega la clave "usoWebhook"
        if 'uso_webhook' in argDatosEntrada:
            usoWebhook = argDatosEntrada['uso_webhook']
        else:
            errorData = True 
            msgError = 'El usoWebhook de la empresa es un dato requerido'

        ErrorSistema = False
        return (errorData, msgError, ErrorSistema)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def altaEmpresa_validaciones ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())

        errorData = True
        msgError = str(ex)
        ErrorSistema = True
        return(errorData, msgError, ErrorSistema)


#   =====================================================================================================
#   EndPoint /smartdoc/empresa/v1/listaEmpresas. Consulta las empresas con servicio en SamrtDoc
#   Clave de operacion: lstemp (Consulta la lista de empresas)
#   =====================================================================================================
@bp_empresas.route('/v1/listaEmpresas', methods=['GET', 'POST'])
def lista_empresas_v1():
    argEntrada = ""
    clave_operacion = "lstemp"
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

        # Llamamos al metodo lista_empresa de la clase EmpresaSvos, que realiza la consulta para obtener las empresas
        tuplaConsultaDatos = EmpresaSvos.lista_empresa(numVersion, current_app.config)

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
        Logger.add_to_log("critical", str('*** def lista_empresas_v1 (/smartdoc/empresa/v1/listaEmpresas ***'))
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


#   =====================================================================================================
#   EndPoint /smartdoc/empresa/v1/altaEmpresa. Alta de empresa con servicio en SamrtDoc
#   Clave de operacion: altemp (Alta de empresa)
#   =====================================================================================================
@bp_empresas.route('/v1/altaEmpresa', methods=['GET', 'POST'])
def alta_empresa_v1():
    numVersion = 1
    clave_operacion = "altemp"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        DatosEntrada = request.get_json()
        # Obtenemos el Diccionario (JSON) de los argumentos de entrada para colocarlos en la bitacora
        argEntrada = json.dumps(request.get_json())
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)

        tuplaValidaDatos = altaEmpresa_validaciones(DatosEntrada)
        errorData = tuplaValidaDatos[0]
        msgError = tuplaValidaDatos[1]

        if (errorData):                                       # El metodo informa que hubo error
            msgError = tuplaValidaDatos[1]
            ErrorSistema = tuplaValidaDatos[2]                # Se verifica si el error es de sistema 
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

        idUsuarioAlta = _bitacora.cve_usuario
        clave_empresa = DatosEntrada['cve_empresa']
        nombre = DatosEntrada['nombre']
        observaciones = DatosEntrada['observaciones']
        usoWebhook = DatosEntrada['uso_webhook']

        # Crea una instancia de la clase Empresa
        _empresa = Empresa(None, clave_empresa, nombre, observaciones, usoWebhook, True, idUsuarioAlta, None)
        # Llamamos al metodo alta_empresa de la clase EmpresaSvos
        tuplaAltaDatos = EmpresaSvos.alta_empresa(_empresa, numVersion, current_app.config)

        validaError = tuplaAltaDatos[0]
        # Se valida si hay error en el resultado del metodo
        if (validaError):                                   # El metodo informa que hubo error
            msgError = tuplaAltaDatos[1]
            ErrorSistema = tuplaAltaDatos[2]                # Se verifica si el error es de sistema 
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

        respuesta = tuplaAltaDatos[1]
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        #_bitacora.salida = json.dumps(resp)
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        return (respuesta, 200)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def alta_empresa_v1 (/smartdoc/empresa/v1/altaEmpresa ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())

        msgError = str(ex)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)
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
#   EndPoint /smartdoc/empresa/v1/consultaEmpresa. Consulta de empresa con servicio en SmartDoc
#   Clave de operacion: conemp (Consulta de empresa)
#   =====================================================================================================
@bp_empresas.route('/v1/consultaEmpresa', methods=['GET', 'POST'])
def consulta_empresa_v1():
    argEntrada = ""
    numVersion = 1
    clave_operacion = "conemp"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        DatosEntrada = request.get_json()    
        argEntrada = json.dumps(DatosEntrada)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)
        
        # Valida si en el JSON llega la clave "cveEmpresa"
        if 'id' in DatosEntrada:
            idEmpresa = DatosEntrada['id']
        else:
            msgError = 'El ID de empresa es un dato requerido'
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

        # Token-Autorizado. Actualizamos el id del usuario en la clase _bitacora, que nos regresa la autorizacion del Token
        _operador = tuplaValidaToken[1]
        _bitacora.cve_usuario = _operador.id
        _bitacora.cve_empresa = _operador.cve_empresa

        # Llamamos al metodo consulta_empresa de la clase EmpresaSvos, que realiza la consulta en empresas del ID
        tuplaConsultaDatos = EmpresaSvos.consulta_empresa(idEmpresa, numVersion, current_app.config)

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
        #_bitacora.salida = json.dumps(resp)
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        return (respuesta, 200)


    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def consulta_empresa_v1 (/smartdoc/empresav1/consultaEmpresa ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())

        msgError = str(ex)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)
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
#   EndPoint /smartdoc/proceso/v1/actualizaEmpresa. Actualizacion de empresa con servicio en SmartDoc
#   Clave de operacion: actemp (Actualizacion de empresa)
#   =====================================================================================================
@bp_empresas.route('/v1/actualizaEmpresa', methods=['GET', 'POST'])
def actualizaEmpresa_v1():
    argEntrada = ""
    callUser = "API"
    clave_operacion = "actemp"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        errorData = False
        numVersion = 1

        DatosEntrada = request.get_json()
        # Obtenemos el Diccionario (JSON) de los argumentos de entrada para colocarlos en la bitacora
        argEntrada = json.dumps(request.get_json())
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)

        tuplaValidaDatos = altaEmpresa_validaciones(DatosEntrada)
        errorData = tuplaValidaDatos[0]
        msgError = tuplaValidaDatos[1]

        # Se valida si no se encontraron errores al validar los datos. Se lee el id de la empresa
        if not (errorData):
            # Obtenenmos la cadena de entrada del API (JSON) y la converttimos en un Diccionario
            request_data = request.get_json()

            # Valida si en el JSON llega la clave "id"
            if 'id' in request_data and request_data['id'] != '':
                argID = request_data['id']
            else:
                errorData = True 
                msgError = 'EL ID de la empresa es un dato requerido'

            # Valida si en el JSON llega la clave "vigente"
            if 'vigente' in request_data and request_data['vigente'] != '':
                argVigente = request_data['vigente']
            else:
                argVigente = 'true' 


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

        idUsuarioActualiza = _bitacora.cve_usuario
        clave_empresa = DatosEntrada['cve_empresa']
        nombre = DatosEntrada['nombre']
        observaciones = DatosEntrada['observaciones']
        usoWebhook = DatosEntrada['uso_webhook']
        if (argVigente == "false"):
            argVigente = False
        else:
            argVigente = True

        # Crea una instancia de la clase Empresa
        _empresa = Empresa(argID, clave_empresa, nombre, observaciones, usoWebhook, argVigente, idUsuarioActualiza, None)
        # Llamamos al metodo alta_empresa de la clase EmpresaSvos
        tuplaAltaDatos = EmpresaSvos.actualiza_empresa(_empresa, numVersion, current_app.config)

        validaError = tuplaAltaDatos[0]
        # Se valida si hay error en el resultado del metodo
        if (validaError):                                   # El metodo informa que hubo error
            msgError = tuplaAltaDatos[1]
            ErrorSistema = tuplaAltaDatos[2]                # Se verifica si el error es de sistema 
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

        respuesta = tuplaAltaDatos[1]
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        return (respuesta, 200)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def actualizaProceso_v1 (/smartdoc/proceso/v1/actualizaProceso ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())

        msgError = str(ex)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)
        # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
        _bitacora.realizado = datetime.now()
        _bitacora.estado = False
        _bitacora.salida = msgError
        _bitacora.err_sistema = True
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora. Error de Sistema
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        resp = {
                'error': True, 
                'mensaje': msgError
            }
        return (resp, 200)

