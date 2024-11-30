#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Obtenemos de los componentes que estan en el directorio Bitacora las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos

#   MODELOS. Obtenemos de los componentes que estan en el directorio src Emp_Areas las clases a utilizar
from src.Emp_Procesos.empProcesoModelo import Empresa_Procesos

#   Servicios. Del componente empProcesoSvosBD.py importar la clase EmpresaProcesoSvos
from src.Emp_Procesos.empProcesoSvosBD import EmpresaProcesoSvos

#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Utilerias.utileriaModelo import Operador
#   Servicios. Del componente seguridadSvos.py importa la clase Seg_TokenSvos
from src.Seguridad.seguridadSvos import Seg_TokenSvos

from datetime import datetime
from flask import request
from config import Config
import json

#   =====================================================================================================
#   Consulta los Plantillas de Procesos relacionadas a una empresa en SmartDOC
#   Clave de operacion: lstepr (Consulta la lista de las Plantilllas de Procesos relacionadas a una empresa)
#   =====================================================================================================
def listaEmpresaProcesos(numVersion):
    argEntrada = ""
    clave_operacion = "lstepr"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        id_empresa = None
        if (numVersion != 0):
            DatosEntrada = request.get_json()    
            argEntrada = json.dumps(DatosEntrada)
            # Crea una instancia de la clase Bitacora
            _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)
            
            # Valida si en el JSON llega la clave "id_empresa"
            if 'id_empresa' in DatosEntrada and DatosEntrada['id_empresa'] != '':
                id_empresa = DatosEntrada['id_empresa']
            else:
                msgError = 'El ID de la empresa de la Plantilla Proceso-Empresa es un dato requerido'
                resp = {
                    'error': True, 
                    'mensaje': msgError
                }
                # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
                _bitacora.realizado = datetime.now()
                _bitacora.estado = False
                _bitacora.salida = json.dumps(resp)
                # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
                tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
                return resp
        else:
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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

        # Token-Autorizado. Obtenemos los datos recuperados desde el Token y los colocamos en una instancia de la clase operador
        _operador = tuplaValidaToken[1]
        _bitacora.cve_usuario = _operador.id
        _bitacora.cve_empresa = _operador.cve_empresa

        # Crea una instancia de la clase Empresa Area
        _Empresa_Proceso = Empresa_Procesos(None, id_empresa, None, None, None, None, None, None, None, None, None)

        # Llamamos al metodo lista_areas de la clase EmpresaProcesoSvos, que realiza la consulta para obtener las Plantillas-Proceso de una Empresa
        tuplaConsultaDatos = EmpresaProcesoSvos.lista_empresaProcesos(_Empresa_Proceso, numVersion, Config)

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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

        respuesta = tuplaConsultaDatos[1]
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
        return respuesta

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def listaEmpresaProcesos ***'))
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
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
        resp = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
        return resp


#   =====================================================================================================
#   Alta de la Plantilla-Proceso a Empresa en SmartDOC
#   Clave de operacion: altepr (Alta de la Plantilla-Proceso a Empresa)
#   =====================================================================================================
def altaEmpresaProceso(numVersion):
    argEntrada = ""
    callUser = "API"
    clave_operacion = "altepr"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        errorData = False
        # Obtenemos el Diccionario (JSON) de los argumentos de entrada para colocarlos en la bitacora
        argEntrada = json.dumps(request.get_json())
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)

        # Obtenenmos la cadena de entrada del API (JSON) y la converttimos en un Diccionario
        request_data = request.get_json()

        # Valida si en el JSON llega la clave "id_empresa"
        if 'id_empresa' in request_data and request_data['id_empresa'] != '':
            argIdEmpresa = request_data['id_empresa']
        else:
            errorData = True 
            msgError = 'El ID de la Empresa es un dato requerido'

        # Valida si en el JSON llega la clave "id_area"
        if 'id_area' in request_data and request_data['id_area'] != '':
            argIdArea = request_data['id_area']
        else:
            errorData = True 
            msgError = 'El ID del Area es un dato requerido'

        # Valida si en el JSON llega la clave "id_proceso"
        if 'id_proceso' in request_data and request_data['id_proceso'] != '':
            argIdProceso = request_data['id_proceso']
        else:
            errorData = True 
            msgError = 'El ID del Proceso es un dato requerido'

        argObservaciones = ""
        # Valida si en el JSON llega la clave "observaciones"
        if 'observaciones' in request_data:
            argObservaciones = request_data['observaciones']
        
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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

        # Token-Autorizado. Obtenemos los datos recuperados desde el Token y los colocamos en una instancia de la clase operador
        _operador = tuplaValidaToken[1]
        _bitacora.cve_usuario = _operador.id
        _bitacora.cve_empresa = _operador.cve_empresa
        idUsuarioAlta = _bitacora.cve_usuario

        # Crea una instancia de la clase Empresa Area
        _Empresa_Proceso = Empresa_Procesos(None, argIdEmpresa, argIdArea, None, argIdProceso, None, argObservaciones, None, idUsuarioAlta, None, None, None)

        # Llamamos al metodo consulta_tdocumento de la clase EmpresaProcesoSvosBD, que realiza la consulta del tipo de documento del ID
        tuplaAltaDatos = EmpresaProcesoSvos.alta_empresaProceso(_Empresa_Proceso, numVersion, Config)

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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

        respuesta = tuplaAltaDatos[1]
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
        return respuesta

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def altaEmpresaProceso ***'))
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
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
        resp = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
        return resp


#   =====================================================================================================
#   Consulta de una Plantilla-Proceso relacionada a Empresa en SmartDOC
#   Clave de operacion: conepr (Consulta de una Plantilla-Proceso relacionada a Empresa )
#   =====================================================================================================
def consultaEmpresaProceso(numVersion):
    clave_operacion = "conepr"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        DatosEntrada = request.get_json()    
        argEntrada = json.dumps(DatosEntrada)
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)
        
        # Valida si en el JSON llega la clave "id"
        if 'id' in DatosEntrada:
            id = DatosEntrada['id']
        else:
            msgError = 'El ID de la Plantilla Proceso-Empresa es un dato requerido'
            resp = {
                'error': True, 
                'mensaje': msgError
            }
            # Convierte el JSON de respuesta a un string para poder guardarlo en la BBDD
            _bitacora.realizado = datetime.now()
            _bitacora.estado = False
            _bitacora.salida = json.dumps(resp)
            # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

        # Token-Autorizado. Obtenemos los datos recuperados desde el Token y los colocamos en una instancia de la clase operador
        _operador = tuplaValidaToken[1]
        _bitacora.cve_usuario = _operador.id
        _bitacora.cve_empresa = _operador.cve_empresa

        # Crea una instancia de la clase Empresa Area
        _Empresa_Proceso = Empresa_Procesos(id, None, None, None, None, None, None, None, None, None, None)

        # Llamamos al metodo consulta_empresaArea de la clase EmpresaProcesoSvos, que realiza la consulta la relacion Empresa-Area del ID
        tuplaConsultaDatos = EmpresaProcesoSvos.consulta_empresaProceso(_Empresa_Proceso, numVersion, Config)

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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

        respuesta = tuplaConsultaDatos[1]
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        #_bitacora.salida = json.dumps(resp)
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
        return respuesta


    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def consultaEmpresaProceso ***'))
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
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
        resp = {
                'error': True, 
                'mensaje': 'Servicio no disponible por el momento'
            }
        return resp


#   =====================================================================================================
#   Actualizacion de una Plantilla-Proceso relacionada a Empresa en SmartDOC
#   Clave de operacion: actepr (Actualizacion de una Plantilla-Proceso relacionada a Empresa )
#   =====================================================================================================
def actualizaEmpresaProceso(numVersion):
    argEntrada = ""
    callUser = "API"
    clave_operacion = "actepr"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        errorData = False
        # Obtenemos el Diccionario (JSON) de los argumentos de entrada para colocarlos en la bitacora
        argEntrada = json.dumps(request.get_json())
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)

        # Obtenenmos la cadena de entrada del API (JSON) y la converttimos en un Diccionario
        request_data = request.get_json()

        # Valida si en el JSON llega la clave "id"
        if 'id' in request_data and request_data['id'] != '':
            argID = request_data['id']
        else:
            errorData = True 
            msgError = 'El ID de la Plantilla Empresa-Proceso es un dato requerido'

        # Valida si en el JSON llega la clave "id_empresa"
        if 'id_empresa' in request_data and request_data['id_empresa'] != '':
            argIdEmpresa = request_data['id_empresa']
        else:
            errorData = True 
            msgError = 'El ID de la Empresa es un dato requerido'

        # Valida si en el JSON llega la clave "id_area"
        if 'id_area' in request_data and request_data['id_area'] != '':
            argIdArea = request_data['id_area']
        else:
            errorData = True 
            msgError = 'El ID del Area es un dato requerido'

        # Valida si en el JSON llega la clave "id_proceso"
        if 'id_proceso' in request_data and request_data['id_proceso'] != '':
            argIdProceso = request_data['id_proceso']
        else:
            errorData = True 
            msgError = 'El ID del Proceso es un dato requerido'

        # Valida si en el JSON llega la clave "observaciones"
        if 'observaciones' in request_data and request_data['observaciones'] != '':
            argObservaciones = request_data['observaciones']
        else:
            errorData = True 
            msgError = 'El campo Obserevaciones es un dato requerido'

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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

        # Token-Autorizado. Obtenemos los datos recuperados desde el Token y los colocamos en una instancia de la clase operador
        _operador = tuplaValidaToken[1]
        _bitacora.cve_usuario = _operador.id
        _bitacora.cve_empresa = _operador.cve_empresa
        idUsuarioActualiza = _bitacora.cve_usuario
        if (argVigente == "false"):
            argVigente = False
        else:
            argVigente = True

        # Crea una instancia de la clase Empresa Area
        _Empresa_Proceso = Empresa_Procesos(argID, argIdEmpresa, argIdArea, None, argIdProceso, None, argObservaciones, argVigente, None, None, idUsuarioActualiza, None)

        # Llamamos al metodo consulta_tdocumento de la clase EmpresaProcesoSvosBD, que realiza la actualizacion del la Plantilla Empresa-Proceso del ID
        tuplaAltaDatos = EmpresaProcesoSvos.actualiza_EmpresaProceso(_Empresa_Proceso, numVersion, Config)

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
            tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
            return resp

        respuesta = tuplaAltaDatos[1]
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
        return respuesta

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def actualizaEmpresaProceso ***'))
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
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, Config)
        resp = {
                'error': True, 
                'mensaje': msgError
            }
        return resp


