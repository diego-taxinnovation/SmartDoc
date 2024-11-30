#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Obtenemos de los componentes que estan en el directorio Bitacora las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos

#   MODELOS. Obtenemos de los componentes que estan en el directorio src Emp_Plantillas las clases a utilizar
from src.Emp_Plantillas.empPlantillaModelo import Empresa_PlantillaDocto

#   Servicios. Del componente empPlantillaSvosBD.py importar la clase EmpresaPlantillaSvos
from src.Emp_Plantillas.empPlantillaSvosBD import EmpresaPlantillaSvos

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
#   Clave de operacion: lstepl (Consulta la lista de las Plantilllas de Procesos relacionadas a una empresa)
#   =====================================================================================================
def listaEmpresaPlantillas(numVersion):
    argEntrada = ""
    clave_operacion = "lstepl"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try: 
        id_empresa = None
        if (numVersion != 0):
            DatosEntrada = request.get_json()    
            argEntrada = json.dumps(DatosEntrada)
            # Crea una instancia de la clase Bitacora
            _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)
            
            # Valida si en el JSON llega la clave "id_emp_proceso"
            if 'id_emp_proceso' in DatosEntrada and DatosEntrada['id_emp_proceso'] != '':
                id_emp_proceso = DatosEntrada['id_emp_proceso']
            else:
                msgError = 'El ID de la Empresa Proceso de la Plantilla Proceso-Empresa es un dato requerido'
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
            id_emp_proceso = None
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

        # Crea una instancia de la clase Empresa Plantilla-Docto
        _Empresa_PlantillaDocto = Empresa_PlantillaDocto(None, id_emp_proceso, None, None, None, None, None, None, None, None, None, None, None, None)        

        # Llamamos al metodo lista_empPlantillaDoctos de la clase EmpresaPlantillaSvos, que realiza la consulta para obtener la Plantilla-Proceso de una Empresa
        tuplaConsultaDatos = EmpresaPlantillaSvos.lista_empPlantillaDoctos(_Empresa_PlantillaDocto, numVersion, Config)

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
        Logger.add_to_log("critical", str('*** def listaEmpresaPlantillas ***'))
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
#   Clave de operacion: altepl (Alta de la Plantilla-Proceso a Empresa)
#   =====================================================================================================
def altaEmpresaPlantilla(numVersion):
    argEntrada = ""
    callUser = "API"
    clave_operacion = "altepl"
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

        # Valida si en el JSON llega la clave "id_emp_proceso"
        if 'id_emp_proceso' in request_data and request_data['id_emp_proceso'] != '':
            argIdEmpProceso = request_data['id_emp_proceso']
        else:
            errorData = True 
            msgError = 'El ID de la Empresa-Proceso es un dato requerido'

        # Valida si en el JSON llega la clave "id_tdocto"
        if 'id_tdocto' in request_data and request_data['id_tdocto'] != '':
            argIdTDocto = request_data['id_tdocto']
        else:
            errorData = True 
            msgError = 'El ID del Tipo de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "id_docto"
        if 'id_docto' in request_data and request_data['id_docto'] != '':
            argIdDocto = request_data['id_docto']
        else:
            errorData = True 
            msgError = 'El ID del Documento es un dato requerido'

        argObservaciones = ""
        # Valida si en el JSON llega la clave "observaciones"
        if 'observaciones' in request_data:
            argObservaciones = request_data['observaciones']
        
        # Valida si en el JSON llega la clave "vigente"
        if 'vigente' in request_data and request_data['vigente'] != '':
            argVigente = request_data['vigente']
        else:
            argVigente = 'true' 

        # Valida si en el JSON llega la clave "obligatorio"
        if 'obligatorio' in request_data and request_data['obligatorio'] != '':
            argObligatorio = request_data['obligatorio']
        else:
            argObligatorio = 'true' 

        # Valida si en el JSON llega la clave "vigencia"
        if 'vigencia' in request_data and request_data['vigencia'] != '':
            argVigencia = request_data['vigencia']
        else:
            argVigencia = 'true' 

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

        if (argVigente == "false"):
            argVigente = False
        else:
            argVigente = True

        if (argObligatorio == "false"):
            argObligatorio = False
        else:
            argObligatorio = True

        if (argVigencia == "false"):
            argVigencia = False
        else:
            argVigencia = True

        # Crea una instancia de la clase Empresa Plantilla-Docto
        _Empresa_PlantillaDocto = Empresa_PlantillaDocto(None, argIdEmpProceso, argIdTDocto, None, argIdDocto, None, argObservaciones, argVigente, argObligatorio, argVigencia, idUsuarioAlta, None, None, None)

        # Llamamos al metodo alta_empPlantillaDocto de la clase EmpresaPlantillaSvosBD, que realiza el alta de la Plantilla-Proceso 
        tuplaAltaDatos = EmpresaPlantillaSvos.alta_empPlantillaDocto(_Empresa_PlantillaDocto, numVersion, Config)

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
        Logger.add_to_log("critical", str('*** def altaEmpresaPlantilla ***'))
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
#   Clave de operacion: conepl (Consulta de una Plantilla-Proceso relacionada a Empresa )
#   =====================================================================================================
def consultaEmpresaPlantilla(numVersion):
    clave_operacion = "conepl"
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

        # Crea una instancia de la clase Empresa Plantilla-Docto
        _Empresa_PlantillaDocto = Empresa_PlantillaDocto(id, None, None, None, None, None, None, None, None, None, None, None, None, None)

        # Llamamos al metodo consulta_empPlantillaDocto de la clase EmpresaPlantillaSvos, que realiza la consulta Plantilla-Proceso del ID
        tuplaConsultaDatos = EmpresaPlantillaSvos.consulta_empPlantillaDocto(_Empresa_PlantillaDocto, numVersion, Config)

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
        Logger.add_to_log("critical", str('*** def consultaEmpresaPlantilla ***'))
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
#   Clave de operacion: actepl (Actualizacion de una Plantilla-Proceso relacionada a Empresa )
#   =====================================================================================================
def actualizaEmpresaPlantilla(numVersion):
    argEntrada = ""
    callUser = "API"
    clave_operacion = "actepl"
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

        # Valida si en el JSON llega la clave "id_emp_proceso"
        if 'id_emp_proceso' in request_data and request_data['id_emp_proceso'] != '':
            argIdEmpProceso = request_data['id_emp_proceso']
        else:
            errorData = True 
            msgError = 'El ID de la Empresa-Proceso es un dato requerido'

        # Valida si en el JSON llega la clave "id_tdocto"
        if 'id_tdocto' in request_data and request_data['id_tdocto'] != '':
            argIdTDocto = request_data['id_tdocto']
        else:
            errorData = True 
            msgError = 'El ID del Tipo de Documento es un dato requerido'

        # Valida si en el JSON llega la clave "id_docto"
        if 'id_docto' in request_data and request_data['id_docto'] != '':
            argIdDocto = request_data['id_docto']
        else:
            errorData = True 
            msgError = 'El ID del Documento es un dato requerido'

        argObservaciones = ""
        # Valida si en el JSON llega la clave "observaciones"
        if 'observaciones' in request_data:
            argObservaciones = request_data['observaciones']
        
        # Valida si en el JSON llega la clave "vigente"
        if 'vigente' in request_data and request_data['vigente'] != '':
            argVigente = request_data['vigente']
        else:
            argVigente = 'true' 

        # Valida si en el JSON llega la clave "obligatorio"
        if 'obligatorio' in request_data and request_data['obligatorio'] != '':
            argObligatorio = request_data['obligatorio']
        else:
            argObligatorio = 'true' 

        # Valida si en el JSON llega la clave "vigencia"
        if 'vigencia' in request_data and request_data['vigencia'] != '':
            argVigencia = request_data['vigencia']
        else:
            argVigencia = 'true' 

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

        if (argObligatorio == "false"):
            argObligatorio = False
        else:
            argObligatorio = True

        if (argVigencia == "false"):
            argVigencia = False
        else:
            argVigencia = True

        # Crea una instancia de la clase Empresa Plantilla-Docto
        _Empresa_PlantillaDocto = Empresa_PlantillaDocto(argID, argIdEmpProceso, argIdTDocto, None, argIdDocto, None, argObservaciones, argVigente, argObligatorio, argVigencia, None, None, idUsuarioActualiza, None)
        
        # Llamamos al metodo actualiza_empPlantillaDocto de la clase EmpresaPlantillaSvosBD, que realiza la actualizacion del la Plantilla Empresa-Proceso del ID
        tuplaAltaDatos = EmpresaPlantillaSvos.actualiza_empPlantillaDocto(_Empresa_PlantillaDocto, numVersion, Config)

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
        Logger.add_to_log("critical", str('*** def actualizaEmpresaPlantilla ***'))
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

