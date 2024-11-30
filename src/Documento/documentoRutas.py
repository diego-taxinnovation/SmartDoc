#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Documento.documentoModelo import Documento#, Expediente_Documento
#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Utilerias.utileriaModelo import Operador
#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos
#   Servicios. Del componente documentoSvosBD.py importa la clase DocumentoSvos
from src.Documento.documentoSvosBD import DocumentoSvos
#   Servicios. Del componente seguridadSvos.py importa la clase Seg_TokenSvos
from src.Seguridad.seguridadSvos import Seg_TokenSvos

from datetime import datetime
from flask import request, current_app, Blueprint
import os
import json
from werkzeug.utils import secure_filename

bp_documentos = Blueprint('documento_blueprint', __name__)


@bp_documentos.route('/v1/', methods = ['GET'])
def HW_doc():
    return 'Hello World !!!'


@bp_documentos.route('/v1/altaDocumento/', methods = ['POST'])
def alta_documento_v1():
    argEntrada = ""
    clave_operacion = "crgdocto"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'

    try:
        numVersion = 1

        try:
            ID = request.form['id']
        except:
            errorData = True 
            msgError = 'El ID es un dato requerido'

        try:
            idExpediente = request.form['id_exp_digital']
        except:
            errorData = True 
            msgError = 'El ID del expediente es un dato requerido'

        try:
            claveEmpresa = request.form['cve_empresa']
        except:
            errorData = True 
            msgError = 'La clave de empresa es un dato requerido'

        try:
            nombreDocto = request.form['nombre_docto']
        except:
            errorData = True 
            msgError = 'El nombre del documento es un dato requerido'

        try:
            observaciones = request.form['observaciones']
        except:
            errorData = True 
            msgError = 'La fecha de vencimiento es un dato requerido'

        try:
            archivo = request.files['imagen']
        except:
            errorData = True 
            msgError = 'La imagen es un dato requerido'
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

        # GUARDAMOS EL ARCHIVO EN UN DIRECTORIO LOCAL
        dir_carga = current_app.config['DIR_CARGAS']
        nombre_archivo = secure_filename(archivo.filename)
        ruta_temporal = os.path.join(dir_carga, nombre_archivo)
        archivo.save(ruta_temporal)

        # CREAMOS UN OBJETO DEL TIPO DOCUMENTO
        doc = Documento(ruta_temporal, dir_carga)
        doc_json = doc.to_json()
        texto_docto = doc.extraer_texto_google()[0][0].description

        # GUARDAMOS EL ARCHIVO EN GOOGLE STORAGE

        gs_json = {
            'id_exp_digital': idExpediente,
            'cve_empresa': claveEmpresa,
            'nombre_docto': nombreDocto,
            'ruta': ruta_temporal
        }
        altaGS = DocumentoSvos.alta_bucket_GS(gs_json, current_app.config)

        validaError = altaGS[0] 
        if (validaError):                                       
            msgError = altaGS[1]
            ErrorSistema = altaGS[2]                # Se verifica si el error es de sistema 
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

        # GUARDAMOS DATOS EN REDIS
        redis_json = {
            'id_docto': ID,
            'nombre_docto': nombreDocto,
            'id_exp_digital': idExpediente,
            'cve_empresa': claveEmpresa,
            'texto_documento': texto_docto,
            'url_bucket': altaGS[1]['datos'],
            'fecha_carga': doc_json['fecha_creacion']
        }
        altaRedis = DocumentoSvos.alta_documento_redis(redis_json, current_app.config)

        validaError = altaRedis[0] ### SI HAY ERROR BORRAR EL DOCTO DE GS
        if (validaError):                                      
            msgError = altaRedis[1]
            ErrorSistema = altaRedis[2]                # Se verifica si el error es de sistema 
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
        
        # GUARDAMOS DATOS EN POSTGRES
        post_json ={
            'id': ID,
            #'id_exp_digital': idExpediente,
            #'id_docto_plantilla': idDoctoPlantilla,
            #'id_docto': idDocto,
            #'obligatorio': obligatorio,
            #'vigencia': vigencia,
            'nombre_docto': nombreDocto,
            'texto_documento': texto_docto,
            'coleccion_datos': json.dumps({}),
            'observaciones': observaciones,
            'url_bucket': altaGS[1]['datos'],
            'url_externa': '',
            'fecha_carga': doc_json['fecha_creacion'],
            #'fecha_vencimiento': fechaVencimiento,
            'completado': True,
            #'id_usuario_alta': idUsuarioAlta
        }
        altaPostgres = DocumentoSvos.alta_documento_supabase(post_json, current_app.config)

        validaError = altaPostgres[0] ### SI HAY ERROR BORRAR EL DOCTO DE GS Y REDIS
        if (validaError):                                       
            msgError = altaPostgres[1]
            ErrorSistema = altaPostgres[2]                # Se verifica si el error es de sistema 
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

        respuesta = altaPostgres[1]
        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(respuesta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        return (respuesta, 200)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def consultar_ocr_v1 (/smartdoc/documento/v1/altaDocumento ***'))
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


@bp_documentos.route('/v1/consultarOCR/', methods=['GET', 'POST'])
def consulta_ocr_v1():
    print('\n\n ***************************************************************')
    argEntrada = ""
    clave_operacion = "consocr"
    clave_app = 'SmartDOC'
    clave_empresa = 'DIGITEK'
    print('Termina de Inicializar')

    try:
        numVersion = 1
        print('***************************************************************' )
        print('Antes de leer JSON')

        DatosEntrada = request.get_json()    
        print('Antes de realizar DUMP leer JSON')
        argEntrada = json.dumps(DatosEntrada)

        print('Antes de Bitacora')
        # Crea una instancia de la clase Bitacora
        _bitacora = Bitacora(None, clave_empresa, clave_app, 'API', clave_operacion, argEntrada)

        claveEmpresa = None
        idExpediente = None
        ID = None

        if 'cve_empresa' in DatosEntrada:
            claveEmpresa = DatosEntrada['cve_empresa']
        elif 'id_exp_digital' in DatosEntrada:
            idExpediente = DatosEntrada['id_exp_digital']
        elif 'id_docto' in DatosEntrada:
            ID = DatosEntrada['id_docto']
        else:
            msgError = 'Alguno de los campos cve_empres, id_exp_digital o id_docto es necesario'
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

        # Valida si en el JSON llega la clave "query"
        if 'query' in DatosEntrada:
            query = DatosEntrada['query']
        else:
            msgError = 'El query es necesario'
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

        # Llamamos al metodo consulta_ocr_redis de la clase DocumentoSvos, que realiza la consulta de OCR en redis
        tuplaConsultaDatos = DocumentoSvos.consulta_ocr_redis(query, current_app.config)

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

        resultadoConsulta = {}
        for r in respuesta:
            if (claveEmpresa) and (claveEmpresa == r['cve_empresa']):
                resultadoConsulta['id_docto'] = r
            elif (idExpediente) and (claveEmpresa == r['id_exp_digital']):
                resultadoConsulta['id_docto'] = r
            elif (ID) and (ID == r['id_docto']):
                resultadoConsulta['id_docto'] = r
            else:
                pass

        _bitacora.realizado = datetime.now()
        _bitacora.estado = True
        _bitacora.salida = json.dumps(resultadoConsulta)
        # Llama a la funcion para insertar en la bitacora, enviando la clase Bitacora
        tuplaDEF = BitacoraSvos.alta_bitacora(_bitacora, current_app.config)
        return (resultadoConsulta, 200)

    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def consultar_ocr_v1 (/smartdoc/documento/v1/consultarOCR ***'))
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


