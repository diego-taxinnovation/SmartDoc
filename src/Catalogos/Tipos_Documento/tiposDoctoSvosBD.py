#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Del componente procesoModelo.py importa la clase Proceso
from src.Catalogos.Tipos_Documento.tiposDoctoModelo import TiposDocumentos

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime as dt

from pprint import pprint

class TDocumentosSvos():
    @classmethod
    def lista_tdocumentos(cls, argNumVersion, ArgCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''SELECT id_tipo_docto, cve_tdocumento, nombre_corto, nombre_largo, vigente, observaciones, id_usuario_alta,
                        to_char("fecha_alta", 'DD/MM/YYYY HH:MM:SS') , id_usuario_actualiza, 
                        to_char("fecha_actualizacion", 'DD/MM/YYYY HH:MM:SS') FROM tipos_documento;'''

            # try para manejo de excepciones en las operaciones a la BBDD
            try:
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

                lstTDocumentos = []
                # La respuesta es una lista de listas, la respuesta debe ser en un JSON
                resJSON = []
                for tdocto in respuesta:
                    lstRegistro = []
                    str_id_tipo_docto = tdocto[0]              # Id del tipo de documento
                    str_cve_tdocumento = tdocto[1]             # Clave del tipo de documento
                    str_nombre_corto = tdocto[2]               # Nombre corto del tipo de documento
                    str_nombre_largo = tdocto[3]               # Nombre largo del tipo de documento
                    str_vigente = tdocto[4]                    # Estado del tipo de documento
                    str_Observaciones = tdocto[5]              # Observaciones del tipo de documento
                    str_usuarioAlta = tdocto[6]                # Id usuario de alta
                    str_fechaAlta = tdocto[7]                  # Fecha de alta
                    str_usuarioActualiza = tdocto[8]           # Id usuario que actualizo
                    str_fechaActualizacion = tdocto[9]         # Fecha de actualizacion

                    # Agregamos los datos del tipo de documento a lstRegistro
                    lstRegistro.append(str_id_tipo_docto)        
                    lstRegistro.append(str_cve_tdocumento)        
                    lstRegistro.append(str_nombre_corto)        
                    lstRegistro.append(str_nombre_largo)        
                    lstRegistro.append(str_vigente)        
                    lstRegistro.append(str_Observaciones)        
                    lstRegistro.append(str_usuarioAlta)        
                    lstRegistro.append(str_fechaAlta)        
                    lstRegistro.append(str_usuarioActualiza)        
                    lstRegistro.append(str_fechaActualizacion)        

                    # Agregamos lstRegistro a la lista de tipos de documemtos lstTDocumentos
                    lstTDocumentos.append(lstRegistro)    

                campos = ('id','cve_tdocumento','nombre_corto', 'nombre_largo', 'vigente', 'observaciones' ,'id_usuario_alta', 'fecha_alta', 'id_usuario_actualiza', 'fecha_actualizacion')
                for registro in lstTDocumentos:
                    resJSON.append(dict(zip(campos, registro)))

                mensaje = 'Consulta realizada exitosamente'
                datosRespuesta['mensaje'] = mensaje
                datosRespuesta['datos'] = resJSON
                datosRespuesta['error'] = False
                ErrorSistema = False

                return (False, datosRespuesta, ErrorSistema)

            except Exception as ex:
                strError = str(ex)
                if ('DETAIL:' in strError):
                    msgErrorDef = str(ex)
                else:                    
                    indice = strError.find('\n')
                    msgErrorDef = 'ERROR: ' + strError[0:indice]

                Logger.add_to_log("critical", str('===================================================================='))
                Logger.add_to_log("critical", str('*** def TDocumentosSvos.lista_tdocumentos ***'))
                Logger.add_to_log("critical", str(ex))
                Logger.add_to_log("critical", traceback.format_exc())
                # No es un error de Sistema. El error esta en la operacion en la BBDD y la mayor parte de los casos es por datos
                ErrorSistema = False
                return (True, msgErrorDef, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def TDocumentosSvos.lista_tdocumentos ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def alta_tdocumento(cls, _TiposDocumentos, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''INSERT INTO tipos_documento 
                            (cve_tdocumento, nombre_corto, nombre_largo, observaciones, id_usuario_alta)
                        VALUES
                            (%s, %s, %s, %s, %s);
                    '''
            datos = (_TiposDocumentos.cve_tdocumento, _TiposDocumentos.nombre_corto, _TiposDocumentos.nombre_largo, _TiposDocumentos.observaciones, _TiposDocumentos.id_usuario_alta)
            # try para manejo de excepciones en las operaciones a la BBDD
            try:
                cursor.execute(query, (datos))
                rowAdd = cursor.rowcount
                connection.commit()
                if connection:
                    cursor.close()
                    connection.close()

                if (rowAdd <= 0):
                    datosRespuesta = {
                        'error': True, 
                        'mensaje': 'Alta NO realizada. Verificar datos'
                    }
                else:
                    datosRespuesta = {
                        'error': False, 
                        'mensaje': 'Alta realizada exitosamente'
                    }

                ErrorSistema = False
                return (False, datosRespuesta, ErrorSistema)

            except Exception as ex:
                strError = str(ex)
                if ('DETAIL:' in strError):
                    msgErrorDef = str(ex)
                else:                    
                    indice = strError.find('\n')
                    msgErrorDef = 'ERROR: ' + strError[0:indice]
                Logger.add_to_log("critical", str('===================================================================='))
                Logger.add_to_log("critical", str('*** def TDocumentosSvos.alta_tdocumento ***'))
                Logger.add_to_log("critical", str(ex))
                Logger.add_to_log("critical", traceback.format_exc())
                # No es un error de Sistema. El error esta en la operacion en la BBDD y la mayor parte de los casos es por datos
                ErrorSistema = False
                return (True, msgErrorDef, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def TDocumentosSvos.alta_tdocumento ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def consulta_tdocumento(cls, _TiposDocumentos, argNumVersion, ArgCurrentApp):
        try:
            datosRespuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''SELECT id_tipo_docto, cve_tdocumento, nombre_corto, nombre_largo, vigente, observaciones, id_usuario_alta,
                        to_char("fecha_alta", 'DD/MM/YYYY HH:MM:SS') , id_usuario_actualiza, to_char("fecha_actualizacion", 'DD/MM/YYYY HH:MM:SS') 
                        FROM tipos_documento WHERE id_tipo_docto = {_TiposDocumentos.id};'''

            # try para manejo de excepciones en las operaciones a la BBDD
            try:
                cursor.execute(query)
                respuesta = cursor.fetchall()
                regtoTDocto = respuesta
                if connection:
                    cursor.close()
                    connection.close()

                #Valida si datdEmpoEmp esta vacio
                if (len(regtoTDocto) <= 0):
                    msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                    ErrorSistema = False
                    return (True, msgError, ErrorSistema)

                _TiposDocumentos.id = regtoTDocto[0][0]
                _TiposDocumentos.cve_tdocumento = regtoTDocto[0][1]
                _TiposDocumentos.nombre_corto = regtoTDocto[0][2]
                _TiposDocumentos.nombre_largo = regtoTDocto[0][3]
                _TiposDocumentos.vigente = regtoTDocto[0][4]
                _TiposDocumentos.observaciones = regtoTDocto[0][5]
                _TiposDocumentos.id_usuario_alta = regtoTDocto[0][6]
                _TiposDocumentos.fecha_alta = regtoTDocto[0][7]
                _TiposDocumentos.id_usuario_actualiza = regtoTDocto[0][8]
                _TiposDocumentos.fecha_actualizacion = regtoTDocto[0][9]
                # Obtiene del metodo to_json de la clase TiposDocumentos los valores en formato JSON          
                jsonTDocto = _TiposDocumentos.to_json()

                mensaje = 'Consulta realizada exitosamente'
                datosRespuesta['mensaje'] = mensaje
                datosRespuesta['datos'] = jsonTDocto
                datosRespuesta['error'] = False
                ErrorSistema = False
                return (False, datosRespuesta, ErrorSistema)

            except Exception as ex:
                strError = str(ex)
                if ('DETAIL:' in strError):
                    msgErrorDef = str(ex)
                else:                    
                    indice = strError.find('\n')
                    msgErrorDef = 'ERROR: ' + strError[0:indice]

                Logger.add_to_log("critical", str('===================================================================='))
                Logger.add_to_log("critical", str('*** def TDocumentosSvos.consulta_tdocumento ***'))
                Logger.add_to_log("critical", str(ex))
                Logger.add_to_log("critical", traceback.format_exc())
                # No es un error de Sistema. El error esta en la operacion en la BBDD y la mayor parte de los casos es por datos
                ErrorSistema = False
                return (True, msgErrorDef, ErrorSistema)
            
        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def TDocumentosSvos.consulta_tdocumento ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def actualiza_tdocumento(cls, _TiposDocumentos, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()

            fchActualizacion = dt.now()
            fchActualizacion = fchActualizacion.strftime("%m/%d/%Y %H:%M:%S")            
            cursor = db.cursor()
            query = f'''UPDATE tipos_documento SET cve_tdocumento = %s, nombre_corto = %s, nombre_largo = %s, vigente = %s, observaciones = %s,
                               id_usuario_actualiza = %s, fecha_actualizacion = %s WHERE id_tipo_docto = %s
                    '''
            datos = (_TiposDocumentos.cve_tdocumento, _TiposDocumentos.nombre_corto, _TiposDocumentos.nombre_largo, _TiposDocumentos.vigente, _TiposDocumentos.observaciones, _TiposDocumentos.id_usuario_actualiza, fchActualizacion, _TiposDocumentos.id)
            # try para manejo de excepciones en las operaciones a la BBDD
            try:
                cursor.execute(query, (datos))
                rowUpdate = cursor.rowcount
                connection.commit()
                if connection:
                    cursor.close()
                    connection.close()

                if (rowUpdate <= 0):
                    datosRespuesta = {
                        'error': True, 
                        'mensaje': 'Actualizacion NO realizada. Verificar datos'
                    }
                else:
                    datosRespuesta = {
                        'error': False, 
                        'mensaje': 'Actualizacion realizada exitosamente'
                    }
                
                ErrorSistema = False
                return (False, datosRespuesta, ErrorSistema)

            except Exception as ex:
                strError = str(ex)
                if ('DETAIL:' in strError):
                    msgErrorDef = str(ex)
                else:                    
                    indice = strError.find('\n')
                    msgErrorDef = 'ERROR: ' + strError[0:indice]

                Logger.add_to_log("critical", str('===================================================================='))
                Logger.add_to_log("critical", str('*** def TDocumentosSvos.actualiza_tdocumento ***'))
                Logger.add_to_log("critical", str(ex))
                Logger.add_to_log("critical", traceback.format_exc())
                # No es un error de Sistema. El error esta en la operacion en la BBDD y la mayor parte de los casos es por datos
                ErrorSistema = False
                return (True, msgErrorDef, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def TDocumentosSvos.actualiza_tdocumento ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

