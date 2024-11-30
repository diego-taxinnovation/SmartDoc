#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Del componente procesoModelo.py importa la clase Proceso
from src.Procesos.procesoModelo import Proceso

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase, RedisBase

import json
from google.cloud import storage

class DocumentoSvos():
    #===================================
    #   SERVICIOS DE POSTGRES
    #===================================
    @classmethod
    def lista_documentos(cls, ArgCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)
            connection = db.conexion()

            cursor = db.cursor()
            query = f'''SELECT id, id_exp_digital, id_plantilla_docto, id_docto, obligatorio, vigencia, nombre_docto, texto_documento,
                        coleccion_datos, observaciones, url_bucket, url_externa,  to_char("fecha_carga", 'DD/MM/YYYY HH:MM:SS'),
                        to_char("fecha_vencimiento", 'DD/MM/YYYY HH:MM:SS'), completado, id_usuario_alta, to_char("fecha_alta", 'DD/MM/YYYY HH:MM:SS'),
                        id_ususario_actualiza, to_char("fecha_actualizacion", 'DD/MM/YYYY HH:MM:SS') FROM sd_exp_digital_doctos;'''

            cursor.execute(query)
            respuesta = cursor.fetchall()
            datosResultado = respuesta
            if connection:
                cursor.close()
                connection.close()

            #Valida si datosResultado esta vacio
            if (len(datosResultado) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            lstDocumentos = []
            # Procesar la respuesta y convertirla a formato JSON
            for documento in respuesta:
                lstRegistro = []
                str_id = documento['id']                         
                str_id_exp_digital = documento['id_exp_digital']                
                str_id_plantilla_docto = documento['id_plantilla_docto']                     
                str_id_docto = documento['id_docto']             
                str_obligatorio = documento['obligatorio']                    
                str_vigencia = documento['vigencia']                 
                str_nombre_docto = documento['nombre_docto']                
                str_texto_documento = documento['texto_documento']                 
                str_coleccion_datos = documento['coleccion_datos']                  
                str_observaciones = documento['observaciones']         
                str_url_bucket = documento['url_bucket']                
                str_url_externa = documento['url_externa']                
                str_fecha_carga = documento['fecha_carga']             
                str_fecha_vencimiento = documento['fecha_vencimiento']           
                str_completado = documento['completado']              
                str_id_usuario_alta = documento['id_usuario_alta']                  
                str_fecha_alta = documento['fecha_alta']                
                str_id_usuario_actualiza = documento['id_ususario_actualiza']              
                str_fecha_actualizacion = documento['fecha_actualizacion']        

                # Agregamos los datos de las Empresas a lstRegistro
                lstRegistro.append(str_id)        
                lstRegistro.append(str_id_exp_digital)        
                lstRegistro.append(str_id_plantilla_docto)        
                lstRegistro.append(str_id_docto)        
                lstRegistro.append(str_obligatorio)        
                lstRegistro.append(str_vigencia)        
                lstRegistro.append(str_nombre_docto)        
                lstRegistro.append(str_texto_documento)        
                lstRegistro.append(str_coleccion_datos)        
                lstRegistro.append(str_observaciones)        
                lstRegistro.append(str_url_bucket)        
                lstRegistro.append(str_url_externa)        
                lstRegistro.append(str_fecha_carga)        
                lstRegistro.append(str_fecha_vencimiento)        
                lstRegistro.append(str_completado)        
                lstRegistro.append(str_id_usuario_alta)        
                lstRegistro.append(str_fecha_alta)        
                lstRegistro.append(str_id_usuario_actualiza)        
                lstRegistro.append(str_fecha_actualizacion)        

                # Agregamos lstRegistro a la lista de tipos de documemtos lstDocumentos
                lstDocumentos.append(lstRegistro)    

            campos = ('id', 'id_exp_digital', 'id_plantilla_docto', 'id_docto', 'obligatorio', 'vigencia', 'nombre_docto', 'texto_documento', 'coleccion_datos', 'observaciones', 'url_bucket', 'url_externa', 'fecha_carga', 'fecha_vencimiento', 'completado', 'id_usuario_alta', 'fecha_alta', 'id_ususario_actualiza', 'fecha_actualizacion')
            resJSON = [dict(zip(campos, documento)) for documento in lstDocumentos]

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = resJSON
            datosRespuesta['error'] = False
            ErrorSistema = False

            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def DocumentoSvos.lista_documentos ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)


    @classmethod
    def alta_documento_supabase(cls, arg_doc_post, ArgCurrentApp):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }

            db = PostgresBase(ArgCurrentApp)
            connection = db.conexion()

            # Verifica que la persona no este registrada
            query = f'''INSERT INTO expediente 
                            (id_empresa, id_persona, tipo_carga, texto, ruta_google_storage, ext, informacion, vigente, fecha_alta, tipo_documento)
                        VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    '''
            
            datos = (arg_doc_post['id_empresa'], arg_doc_post['id_persona'], arg_doc_post['tipo_carga'], arg_doc_post['texto'], arg_doc_post['ruta_gs'], arg_doc_post['ext'], arg_doc_post['informacion'], arg_doc_post['vigente'], arg_doc_post['fecha_alta'], arg_doc_post['tipo_documento'])
            connection.execute(query, (datos))
            connection.commit()
            if connection.conexion:
                connection.close()

            datos_respuesta['error'] = False
            datos_respuesta['mensaje'] = 'Alta de documento en POSTGRES realizada exitosamente'
            error_sistema = False
            return (False, datos_respuesta, error_sistema)
        
        except Exception as ex:
            msg_error = str(ex)
            error_sistema = True
            print('DocumentoServicios.alta_documento_supabase: ', ex)
            return (True, msg_error, error_sistema)
    

    @classmethod
    def baja_documento_supabase(cls, arg_documento, ArgCurrentApp):
        return
        

    #===================================
    #   SERVICIOS DE REDIS
    #===================================
    @classmethod
    def alta_documento_redis(cls, arg_doc_redis: dict, ArgCurrentApp):
        try:
            datosRespuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }

            redis_con = RedisBase(ArgCurrentApp)

            nombre = arg_doc_redis.pop('nombre')
            redis_con.cargar_json(nombre, arg_doc_redis)

            datosRespuesta['error'] = False
            datosRespuesta['mensaje'] = 'Alta de documento en REDIS realizada exitosamente'
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)
        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def DocumentoSvos.alta_documento_redis ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)
    

    @classmethod
    def baja_documento_redis(cls, arg_doc_redis, ArgCurrentApp):
        return
    

    @classmethod
    def consulta_ocr_redis(cls, query, ArgCurrentApp):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }

            redis_con = RedisBase(ArgCurrentApp)
            consulta = redis_con.consultar()
            resultados = []
            for r in consulta:
                resultados.append(json.loads(r.json))

            datos_respuesta['datos'] = resultados
            datos_respuesta['error'] = False
            datos_respuesta['mensaje'] = 'Consulta de documento en REDIS realizada exitosamente'
            error_sistema = False
            return (False, datos_respuesta, error_sistema)
        except Exception as ex:
            msg_error = str(ex)
            error_sistema = True
            print('DocumentoServicios.consulta_ocr_redis: ', ex)
            return (True, msg_error, error_sistema)
    

    #===================================
    #   SERVICIOS DE GOOGLE CLOUD
    #===================================
    @classmethod
    def alta_bucket_GS(cls, arg_documento, ArgCurrentApp):
        try:
            datos_respuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }
            
            bucket_name = ArgCurrentApp['GOOGLE_CLOUD_BUCKET']
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            blob_name = f"{arg_documento['cve_empresa']}/{arg_documento['cve_persona']}/{arg_documento['tipo_documento']}/{arg_documento['nombre']}"
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(arg_documento['ruta'])

            datos_respuesta['datos'] = f'gs://{bucket_name}/{blob_name}'
            datos_respuesta['mensaje'] = 'Carga en GS realizada correctamente'
            return datos_respuesta
        except Exception as ex:
            print('DocumentoServicios.alta_bucket_GS: ',ex)
            datos_respuesta['error'] = True
            datos_respuesta['mensaje'] = ex
            return datos_respuesta