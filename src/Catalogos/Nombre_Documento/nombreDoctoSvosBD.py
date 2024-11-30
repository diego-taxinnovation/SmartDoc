#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Obtenemos de los componentes que estan en el directorio Catalogos / Nombre_Documento las clases a utilizar
from src.Catalogos.Nombre_Documento.nombreDoctoModelo import NombreDocumento

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime as dt

from pprint import pprint

class NombreDoctoSvos():
    @classmethod
    def lista_nombreDocto(cls, argNumVersion, ArgCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()

            cursor = db.cursor()
            query = f'''SELECT nd.id_nombre_docto, nd.nombre, nd.observaciones, nd.vigente, nd.id_tdocto, td.cve_tdocumento, td.nombre_corto,
                               nd.id_usuario_alta,  to_char(nd.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), nd.id_usuario_actualiza, 
                               to_char(nd.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS') 
                        FROM nombre_documento nd, tipos_documento td
                        WHERE nd.id_tdocto = td.id_tipo_docto;'''
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

            lstNombreDocto = []
            # La respuesta es una lista de listas, la respuesta debe ser en un JSON
            resJSON = []
            for tdocto in respuesta:
                lstRegistro = []
                str_id_nombre_docto = tdocto[0]            # Id del nombre de documento
                str_nombre = tdocto[1]                     # Nombre de documento
                str_observaciones = tdocto[2]              # Observaciones del nombre de documento
                str_vigente = tdocto[3]                    # Estado del nombre de documento
                str_id_tdocto = tdocto[4]                  # ID del tipo de documento asociado
                str_cve_tdocumento = tdocto[5]             # Clave del tipo de documento asociado
                str_nombre_corto = tdocto[6]               # Nombre corto del tipo de documento asociado
                str_usuarioAlta = tdocto[7]                # Id usuario de alta
                str_fechaAlta = tdocto[8]                  # Fecha de alta
                str_usuarioActualiza = tdocto[9]           # Id usuario que actualizo
                str_fechaActualizacion = tdocto[10]        # Fecha de actualizacion

                # Agregamos los datos del tipo de documento a lstRegistro
                lstRegistro.append(str_id_nombre_docto)        
                lstRegistro.append(str_nombre)        
                lstRegistro.append(str_observaciones)        
                lstRegistro.append(str_vigente)        
                lstRegistro.append(str_id_tdocto)        
                lstRegistro.append(str_cve_tdocumento)        
                lstRegistro.append(str_nombre_corto)        
                lstRegistro.append(str_usuarioAlta)        
                lstRegistro.append(str_fechaAlta)        
                lstRegistro.append(str_usuarioActualiza)        
                lstRegistro.append(str_fechaActualizacion)        

                # Agregamos lstRegistro a la lista de tipos de documemtos lstNombreDocto
                lstNombreDocto.append(lstRegistro)    

            campos = ('id','nombre','observaciones', 'vigente', 'id_tdocto', 'cve_tdocumemto', 'nombre_corto',  'id_usuario_alta', 'fecha_alta', 'id_usuario_actualiza', 'fecha_actualizacion')
            for registro in lstNombreDocto:
                resJSON.append(dict(zip(campos, registro)))

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = resJSON
            datosRespuesta['error'] = False
            ErrorSistema = False

            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def NombreDoctoSvos.lista_nombreDocto ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def alta_nombreDocto(cls, _NombreDocumento, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()

            cursor = db.cursor()
            query = f'''INSERT INTO nombre_documento 
                            (nombre, observaciones, id_tdocto, id_usuario_alta)
                        VALUES
                            (%s, %s, %s, %s);
                    '''
            datos = (_NombreDocumento.nombre, _NombreDocumento.observaciones, _NombreDocumento.id_tdocto, _NombreDocumento.id_usuario_alta)
            cursor.execute(query, (datos))

            rowUpdate = cursor.rowcount
            connection.commit()
            if connection:
                cursor.close()
                connection.close()

            if (rowUpdate <= 0):
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
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def NombreDoctoSvos.alta_nombreDocto ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def consulta_nombreDocto(cls, _NombreDocumento, argNumVersion, ArgCurrentApp):
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

            query = f'''SELECT nd.id_nombre_docto, nd.nombre, nd.observaciones, nd.vigente, nd.id_tdocto, td.cve_tdocumento , td.nombre_corto,
                               nd.id_usuario_alta,  to_char(nd.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), nd.id_usuario_actualiza, 
                               to_char(nd.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS') 
                        FROM nombre_documento nd, tipos_documento td
                        WHERE nd.id_tdocto = td.id_tipo_docto AND nd.id_nombre_docto = {_NombreDocumento.id};'''
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

            _NombreDocumento.id = regtoTDocto[0][0]
            _NombreDocumento.nombre = regtoTDocto[0][1]
            _NombreDocumento.observaciones = regtoTDocto[0][2]
            _NombreDocumento.vigente = regtoTDocto[0][3]
            _NombreDocumento.id_tdocto = regtoTDocto[0][4]
            _NombreDocumento.cve_tdocto = regtoTDocto[0][5]
            _NombreDocumento.nombre_corto = regtoTDocto[0][6]
            _NombreDocumento.id_usuario_alta = regtoTDocto[0][7]
            _NombreDocumento.fecha_alta = regtoTDocto[0][8]
            _NombreDocumento.id_usuario_actualiza = regtoTDocto[0][9]
            _NombreDocumento.fecha_actualizacion = regtoTDocto[0][10]
            # Obtiene del metodo to_json de la clase _NombreDocumento los valores en formato JSON          
            jsonNombreDocto = _NombreDocumento.to_json()

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = jsonNombreDocto
            datosRespuesta['error'] = False
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def NombreDoctoSvos.consulta_nombreDocto ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def actualiza_nombreDocto(cls, _NombreDocumento, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()

            fchActualizacion = dt.now()
            fchActualizacion = fchActualizacion.strftime("%m/%d/%Y %H:%M:%S")            
            cursor = db.cursor()

            query = f'''UPDATE nombre_documento SET nombre = %s, observaciones = %s, vigente = %s, id_tdocto = %s, 
                               id_usuario_actualiza = %s, fecha_actualizacion = %s WHERE id_nombre_docto = %s
                    '''
            datos = (_NombreDocumento.nombre, _NombreDocumento.observaciones, _NombreDocumento.vigente, _NombreDocumento.id_tdocto, _NombreDocumento.id_usuario_actualiza, fchActualizacion, _NombreDocumento.id)
            cursor.execute(query, (datos))

            rowUpdate = cursor.rowcount
            connection.commit()
            if connection:
                cursor.close()
                connection.close()

            if (rowUpdate <= 0):
                datosRespuesta = {
                    'error': True, 
                    'mensaje': 'Actualizacion no realizada. Verificar datos'
                }
            else:
                datosRespuesta = {
                    'error': False, 
                    'mensaje': 'Actualizacion realizada exitosamente'
                }
            
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def NombreDoctoSvos.actualiza_nombreDocto ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

