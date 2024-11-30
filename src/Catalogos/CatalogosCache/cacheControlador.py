#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Obtenemos de los componentes que estan en el directorio Bitacora las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos

#   Servicios. Del componente cacheSvosBD.py importar la clase cacheSvos
from src.Catalogos.CatalogosCache.cacheSvosBD import cacheSvos

#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Utilerias.utileriaModelo import Operador
#   Servicios. Del componente seguridadSvos.py importa la clase Seg_TokenSvos
from src.Seguridad.seguridadSvos import Seg_TokenSvos

from datetime import datetime
from flask import request
import json

#   =====================================================================================================
#   Consulta los Catalogos Comunes en SmartDOC
#   Clave de operacion: lstccm (Consulta los Catalogos Comunes)
#   =====================================================================================================
def listaCache(numVersion):
    argEntrada = ""
    clave_operacion = "lstccm"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, None)

        # La version 0 NO aplica Seguridad
        if (numVersion != 0):
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
                tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora)
                return resp

            # Token-Autorizado. Obtenemos los datos recuperados desde el Token y los colocamos en una instancia de la clase operador
            _operador = tuplaValidaToken[1]
            _bitacora.cve_usuario = _operador.id
            _bitacora.cve_empresa = _operador.cve_empresa

        # Llamamos al metodo lista_areas de la clase cacheSvos, que realiza la consulta para obtener los catalogos
        tuplaConsultaDatos = cacheSvos.consulta_catalogos(numVersion)

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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora)
            return resp

        respuesta = tuplaConsultaDatos[1]
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora)
        return respuesta

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def listaCache ***'))
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
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora)
        resp = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
        return resp


