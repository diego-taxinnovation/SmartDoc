#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Obtenemos de los componentes que estan en el directorio Bitacora las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos

#   MODELOS. Obtenemos de los componentes que estan en el directorio Catalogos / Tipos_Documento las clases a utilizar
from src.Catalogos.Tipos_Documento.tiposDoctoModelo import TiposDocumentos
#   Servicios. Del componente tiposDoctoSvosBD.py importa la clase TDocumentosSvos
from src.Catalogos.Tipos_Documento.tiposDoctoSvosBD import TDocumentosSvos

#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Utilerias.utileriaModelo import Operador
#   Servicios. Del componente seguridadSvos.py importa la clase Seg_TokenSvos
from src.Seguridad.seguridadSvos import Seg_TokenSvos

from datetime import datetime
from flask import request, current_app, Blueprint
import json

bp_tdocto = Blueprint('tdocto_blueprint', __name__)

#   =====================================================================================================
#   EndPoint /smartdoc/tdocto/v1/listaTDocto. Consulta los Tipos de Documentos en SamrtDoc
#   Clave de operacion: lsttdo (Consulta la lista de Tipos de Documentos)
#   =====================================================================================================
@bp_tdocto.route('/v1/listaTDocto', methods=['GET', 'POST'])
def listaTDocto_v1():
    argEntrada = ""
    clave_operacion = "lsttdo"
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

        # Llamamos al metodo lista_tdocumentos de la clase TDocumentosSvos, que realiza la consulta para obtener los procesos
        tuplaConsultaDatos = TDocumentosSvos.lista_tdocumentos(numVersion, current_app.config)

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
        Logger.add_to_log("critical", str('*** def listaTDocto_v1 (/smartdoc/tdocto/v1/listaTDocto ***'))
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
#   EndPoint /smartdoc/tdocto/v1/altaTDocto. Alta de Tipos de Documento en SamrtDoc
#   Clave de operacion: alttdo (Alta de Tipos de Documento)
#   =====================================================================================================
@bp_tdocto.route('/v1/altaTDocto', methods=['GET', 'POST'])
def altaTDocto_v1():
    argEntrada = ""
    callUser = "API"
    clave_operacion = "alttdo"
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

        # Valida si en el JSON llega la clave "cve_tdocumento"
        if 'cve_tdocumento' in request_data and request_data['cve_tdocumento'] != '':
            argCveTDocto = request_data['cve_tdocumento']
        else:
            errorData = True 
            msgError = 'La clave del Tipo de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "nombre_corto"
        if 'nombre_corto' in request_data and request_data['nombre_corto'] != '':
            argNombreCorto = request_data['nombre_corto']
        else:
            errorData = True 
            msgError = 'El nombre Corto del Tipo de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "nombre_largo"
        if 'nombre_largo' in request_data and request_data['nombre_largo'] != '':
            argNombreLargo = request_data['nombre_largo']
        else:
            argNombreLargo = ''

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
        _TDocto = TiposDocumentos(None, argCveTDocto, argNombreCorto, argNombreLargo, None, argObservaciones, idUsuarioAlta, None)

        # Llamamos al metodo consulta_tdocumento de la clase TDocumentosSvos, que realiza la consulta del tipo de documento del ID
        tuplaAltaDatos = TDocumentosSvos.alta_tdocumento(_TDocto, numVersion, current_app.config)

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
        Logger.add_to_log("critical", str('*** def altaTDocto_v1 (/smartdoc/tdocto/v1/altaTDocto ***'))
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
#   EndPoint /smartdoc/tdocto/v1/consultaTDocto. Consulta de  Tipos de Documento en SamrtDoc
#   Clave de operacion: contdo (Consulta de Tipos de Documento)
#   =====================================================================================================
@bp_tdocto.route('/v1/consultaTDocto', methods=['GET', 'POST'])
def consultaTDocto_v1():
    numVersion = 1
    clave_operacion = "contdo"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        DatosEntrada = request.get_json()    
        argEntrada = json.dumps(DatosEntrada)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)
        
        # Valida si en el JSON llega la clave "id"
        if 'id' in DatosEntrada:
            idTDocto = DatosEntrada['id']
        else:
            msgError = 'El ID del tipo de documento es un dato requerido'
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

        # Crea una instancia de la clase Tipo de Documento
        _TDocto = TiposDocumentos(idTDocto, None, None, None, None, None, None, None)

        # Llamamos al metodo consulta_tdocumento de la clase TDocumentosSvos, que realiza la consulta del tipo de documento del ID
        tuplaConsultaDatos = TDocumentosSvos.consulta_tdocumento(_TDocto, numVersion, current_app.config)

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
        Logger.add_to_log("critical", str('*** def consultaTDocto_v1 (/smartdoc/tdocto/v1/consultaTDocto ***'))
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
#   EndPoint /smartdoc/tdocto/v1/actualizaTDocto. Actualizacion de Tipos de Documento en SamrtDoc
#   Clave de operacion: acttdo (Actualizacion de Tipos de Documento)
#   =====================================================================================================
@bp_tdocto.route('/v1/actualizaTDocto', methods=['GET', 'POST'])
def actualizaTDocto_v1():
    argEntrada = ""
    callUser = "API"
    clave_operacion = "acttdo"
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

        # Valida si en el JSON llega la clave "id"
        if 'id' in request_data and request_data['id'] != '':
            argIdTDocto = request_data['id']
        else:
            errorData = True 
            msgError = 'El ID del Tipo de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "cve_tdocumento"
        if 'cve_tdocumento' in request_data and request_data['cve_tdocumento'] != '':
            argCveTDocto = request_data['cve_tdocumento']
        else:
            errorData = True 
            msgError = 'La clave del Tipo de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "nombre_corto"
        if 'nombre_corto' in request_data and request_data['nombre_corto'] != '':
            argNombreCorto = request_data['nombre_corto']
        else:
            errorData = True 
            msgError = 'El nombre Corto del Tipo de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "nombre_largo"
        if 'nombre_largo' in request_data and request_data['nombre_largo'] != '':
            argNombreLargo = request_data['nombre_largo']
        else:
            argNombreLargo = ''

        # Valida si en el JSON llega la clave "vigente"
        if 'vigente' in request_data and request_data['vigente'] != '':
            argVigente = request_data['vigente']
        else:
            errorData = True 
            msgError = 'La vigencia del Tipo de Documento es un dato requerido'

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
        idUsuarioActualiza = _bitacora.cve_usuario
        if (argVigente == "false"):
            argVigente = False
        else:
            argVigente = True

        # Crea una instancia de la clase Tipo de Documento
        _TDocto = TiposDocumentos(argIdTDocto, argCveTDocto, argNombreCorto, argNombreLargo, argVigente, argObservaciones, None, None, idUsuarioActualiza)

        # Llamamos al metodo consulta_tdocumento de la clase TDocumentosSvos, que realiza la consulta del tipo de documento del ID
        tuplaAltaDatos = TDocumentosSvos.actualiza_tdocumento(_TDocto, numVersion, current_app.config)

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
        Logger.add_to_log("critical", str('*** def actualizaTDocto_v1 (/smartdoc/tdocto/v1/actualizaTDocto ***'))
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


