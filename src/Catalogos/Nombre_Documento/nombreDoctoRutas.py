#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Obtenemos de los componentes que estan en el directorio Bitacora las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos

#   MODELOS. Obtenemos de los componentes que estan en el directorio Catalogos / Nombre_Documento las clases a utilizar
from src.Catalogos.Nombre_Documento.nombreDoctoModelo import NombreDocumento

#   Servicios. Del componente nombreDoctoSvosBD.py importa la clase TDocumeNombreDoctoSvosntosSvos
from src.Catalogos.Nombre_Documento.nombreDoctoSvosBD import NombreDoctoSvos

#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Utilerias.utileriaModelo import Operador
#   Servicios. Del componente seguridadSvos.py importa la clase Seg_TokenSvos
from src.Seguridad.seguridadSvos import Seg_TokenSvos

from datetime import datetime
from flask import request, current_app, Blueprint
import json

bp_ndocto = Blueprint('ndocto_blueprint', __name__)
#   =====================================================================================================
#   EndPoint /smartdoc/ndocto/v1/listaNDocto. Consulta los Nombre de Documentos en SamrtDoc
#   Clave de operacion: lstndo (Consulta la lista de Nombres de Documentos)
#   =====================================================================================================
@bp_ndocto.route('/v1/listaNDocto', methods=['GET', 'POST'])
def listaNDocto_v1():
    argEntrada = ""
    clave_operacion = "lstndo"
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

        # Llamamos al metodo lista_tdocumentos de la clase NombreDoctoSvos, que realiza la consulta para obtener los procesos
        tuplaConsultaDatos = NombreDoctoSvos.lista_nombreDocto(numVersion, current_app.config)

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
        Logger.add_to_log("critical", str('*** def listaNDocto_v1 (/smartdoc/ndocto/v1/listaNDocto ***'))
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
#   EndPoint /smartdoc/ndocto/v1/altaNDocto. Alta de Nombre de Documento en SamrtDoc
#   Clave de operacion: altndo (Alta de Nombre de Documento)
#   =====================================================================================================
@bp_ndocto.route('/v1/altaNDocto', methods=['GET', 'POST'])
def altaNDocto_v1():
    argEntrada = ""
    callUser = "API"
    clave_operacion = "altndo"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        errorData = False
        numVersion = 1
        # Obtenemos el Diccionario (JSON) de los argumentos de entrada para colocarlos en la bitacora
        argEntrada = json.dumps(request.get_json())
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)

        # Obtenenmos la cadena de entrada del API (JSON) y la converttimos en un Diccionario
        request_data = request.get_json()

        # Valida si en el JSON llega la clave "nombre"
        if 'nombre' in request_data and request_data['nombre'] != '':
            argNombre= request_data['nombre']
        else:
            errorData = True 
            msgError = 'El Nombre de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "id_tdocto"
        if 'id_tdocto' in request_data and request_data['id_tdocto'] != '':
            argIDtdocto= request_data['id_tdocto']
        else:
            errorData = True 
            msgError = 'El ID del Tipo de Documento asociado es un dato requerido'

        # Valida si en el JSON llega la clave "observaciones"
        if 'observaciones' in request_data and request_data['observaciones'] != '':
            argObservaciones = request_data['observaciones']
        else:
            argObservaciones = ''

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
        idUsuarioAlta = _bitacora.cve_usuario

        # Crea una instancia de la clase Tipo de Documento
        _NDocto = NombreDocumento(None, argNombre, argObservaciones, None, argIDtdocto, None, None, idUsuarioAlta, None)

        # Llamamos al metodo alta_nombreDocto de la clase NombreDoctoSvos, que realiza el Alta de un Nombre de Documento
        tuplaAltaDatos = NombreDoctoSvos.alta_nombreDocto(_NDocto, numVersion, current_app.config)

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
        Logger.add_to_log("critical", str('*** def altaNDocto_v1 (/smartdoc/ndocto/v1/altaNDocto ***'))
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
#   EndPoint /smartdoc/ndocto/v1/consultaNDocto. Consulta de Nombre de Documento en SamrtDoc
#   Clave de operacion: conndo (Consulta de Nombre de Documento)
#   =====================================================================================================
@bp_ndocto.route('/v1/consultaNDocto', methods=['GET', 'POST'])
def consultaNDocto_v1():
    numVersion = 1
    clave_operacion = "conndo"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        DatosEntrada = request.get_json()    
        argEntrada = json.dumps(DatosEntrada)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)
        
        # Valida si en el JSON llega la clave "id"
        if 'id' in DatosEntrada:
            idDocumento = DatosEntrada['id']
        else:
            msgError = 'El ID del nombre de documento es un dato requerido'
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

        # Crea una instancia de la clase Documento
        _Documento = NombreDocumento(idDocumento, None, None, None, None, None, None, None, None)

        # Llamamos al metodo consulta_nombreDocto de la clase NombreDoctoSvos, que realiza la consulta del tipo de documento del ID
        tuplaConsultaDatos = NombreDoctoSvos.consulta_nombreDocto(_Documento, numVersion, current_app.config)

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
        Logger.add_to_log("critical", str('*** def consultaNDocto_v1 (/smartdoc/ndocto/v1/consultaNDocto ***'))
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
#   EndPoint /smartdoc/ndocto/v1/actualizaNDocto. Actualizacion de Nombre de Documento en SamrtDoc
#   Clave de operacion: actndo (Actualizacion de Nombre de Documento)
#   =====================================================================================================
@bp_ndocto.route('/v1/actualizaNDocto', methods=['GET', 'POST'])
def actualizaNDocto_v1():
    argEntrada = ""
    callUser = "API"
    clave_operacion = "actndo"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        errorData = False
        numVersion = 1
        # Obtenemos el Diccionario (JSON) de los argumentos de entrada para colocarlos en la bitacora
        argEntrada = json.dumps(request.get_json())
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)

        # Obtenenmos la cadena de entrada del API (JSON) y la convertimos en un Diccionario
        request_data = request.get_json()

        # Valida si en el JSON llega la clave "id_nombre_docto"
        if 'id' in request_data and request_data['id'] != '':
            argID = request_data['id']
        else:
            errorData = True 
            msgError = 'El ID del Nombre de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "nombre"
        if 'nombre' in request_data and request_data['nombre'] != '':
            argNombre= request_data['nombre']
        else:
            errorData = True 
            msgError = 'El Nombre de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "id_tdocto"
        if 'id_tdocto' in request_data and request_data['id_tdocto'] != '':
            argIDtdocto= request_data['id_tdocto']
        else:
            errorData = True 
            msgError = 'El ID del Tipo de Documento asociado es un dato requerido'

        # Valida si en el JSON llega la clave "observaciones"
        if 'observaciones' in request_data and request_data['observaciones'] != '':
            argObservaciones = request_data['observaciones']
        else:
            argObservaciones = ''

        # Valida si en el JSON llega la clave "vigente"
        if 'vigente' in request_data and request_data['vigente'] != '':
            argVigente = request_data['vigente']
        else:
            errorData = True 
            msgError = 'La vigencia del Tipo de Documento es un dato requerido'
            
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
        if (argVigente == "false"):
            argVigente = False
        else:
            argVigente = True

        # Crea una instancia de la clase Tipo de Documento
        _NDocto = NombreDocumento(argID, argNombre, argObservaciones, argVigente, argIDtdocto, None, None, None, None, idUsuarioActualiza)

        # Llamamos al metodo actualiza_nombreDocto de la clase NombreDoctoSvos, que realiza el Actualizacion de un Nombre de Documento
        tuplaAltaDatos = NombreDoctoSvos.actualiza_nombreDocto(_NDocto, numVersion, current_app.config)

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
        Logger.add_to_log("critical", str('*** def actualizaNDocto_v1 (/smartdoc/ndocto/v1/actualizaNDocto ***'))
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


