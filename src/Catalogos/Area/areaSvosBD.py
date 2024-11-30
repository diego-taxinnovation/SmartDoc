#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Del componente procesoModelo.py importa la clase Proceso
from src.Catalogos.Area.areaModelo import Area

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime as dt

from pprint import pprint

class AreaSvos():
    @classmethod
    def lista_areas(cls, argNumVersion, argCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)   
            db = PostgresBase(argCurrentApp) 
            connection = db.conexion()

            cursor = db.cursor()
            query = f'''SELECT id, cve_area, nombre, vigente, observaciones, id_usuario_alta,
                        to_char("fecha_alta", 'DD/MM/YYYY HH:MM:SS') , id_usuario_actualiza, 
                        to_char("fecha_actualizacion", 'DD/MM/YYYY HH:MM:SS') FROM area;'''

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

                lstAreas = []
                # La respuesta es una lista de listas, la respuesta debe ser en un JSON
                resJSON = []
                for tdocto in respuesta:
                    lstRegistro = []
                    str_id = tdocto[0]                         # Id del tipo de documento
                    str_cve_area = tdocto[1]                   # Clave del tipo de documento
                    str_nombre = tdocto[2]                     # Nombre corto del tipo de documento
                    str_vigente = tdocto[3]                    # Estado del tipo de documento
                    str_Observaciones = tdocto[4]              # Observaciones del tipo de documento
                    str_usuarioAlta = tdocto[5]                # Id usuario de alta
                    str_fechaAlta = tdocto[6]                  # Fecha de alta
                    str_usuarioActualiza = tdocto[7]           # Id usuario que actualizo
                    str_fechaActualizacion = tdocto[8]         # Fecha de actualizacion

                    # Agregamos los datos del tipo de documento a lstRegistro
                    lstRegistro.append(str_id)        
                    lstRegistro.append(str_cve_area)        
                    lstRegistro.append(str_nombre)        
                    lstRegistro.append(str_vigente)        
                    lstRegistro.append(str_Observaciones)        
                    lstRegistro.append(str_usuarioAlta)        
                    lstRegistro.append(str_fechaAlta)        
                    lstRegistro.append(str_usuarioActualiza)        
                    lstRegistro.append(str_fechaActualizacion)        

                    # Agregamos lstRegistro a la lista de Areas lstAreas
                    lstAreas.append(lstRegistro)    

                campos = ('id','cve_area','nombre', 'vigente', 'observaciones' ,'id_usuario_alta', 'fecha_alta', 'id_usuario_actualiza', 'fecha_actualizacion')
                for registro in lstAreas:
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
                Logger.add_to_log("critical", str('*** def AreaSvos.lista_areas ***'))
                Logger.add_to_log("critical", str(ex))
                Logger.add_to_log("critical", traceback.format_exc())
                # No es un error de Sistema. El error esta en la operacion en la BBDD y la mayor parte de los casos es por datos
                ErrorSistema = False
                return (True, msgErrorDef, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def AreaSvos.lista_areas ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def alta_area(cls, _Area, argNumVersion, argCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)  
            db = PostgresBase(argCurrentApp)  
            connection = db.conexion()

            cursor = db.cursor()
            query = f'''INSERT INTO area 
                            (cve_area, nombre, observaciones, id_usuario_alta)
                        VALUES
                            (%s, %s, %s, %s);
                    '''
            datos = (_Area.cve_area, _Area.nombre, _Area.observaciones, _Area.id_usuario_alta)
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
                Logger.add_to_log("critical", str('*** def AreaSvos.alta_area ***'))
                Logger.add_to_log("critical", str(ex))
                Logger.add_to_log("critical", traceback.format_exc())
                # No es un error de Sistema. El error esta en la operacion en la BBDD y la mayor parte de los casos es por datos
                ErrorSistema = False
                return (True, msgErrorDef, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def AreaSvos.alta_area ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def consulta_area(cls, _Area, argNumVersion, argCurrentApp):
        try:
            datosRespuesta = {
                'datos': '',
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(argCurrentApp)  
            connection = db.conexion()

            cursor = db.cursor()
            query = f'''SELECT id, cve_area, nombre, vigente, observaciones, id_usuario_alta,
                        to_char("fecha_alta", 'DD/MM/YYYY HH:MM:SS') , id_usuario_actualiza, to_char("fecha_actualizacion", 'DD/MM/YYYY HH:MM:SS') 
                        FROM area WHERE id = {_Area.id};'''

            # try para manejo de excepciones en las operaciones a la BBDD
            try:
                cursor.execute(query)
                respuesta = cursor.fetchall()
                regtoArea = respuesta
                if connection:
                    cursor.close()
                    connection.close()

                #Valida si regtoArea esta vacio
                if (len(regtoArea) <= 0):
                    msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                    ErrorSistema = False
                    return (True, msgError, ErrorSistema)

                _Area.id = regtoArea[0][0]
                _Area.cve_area = regtoArea[0][1]
                _Area.nombre = regtoArea[0][2]
                _Area.vigente = regtoArea[0][3]
                _Area.observaciones = regtoArea[0][4]
                _Area.id_usuario_alta = regtoArea[0][5]
                _Area.fecha_alta = regtoArea[0][6]
                _Area.id_usuario_actualiza = regtoArea[0][7]
                _Area.fecha_actualizacion = regtoArea[0][8]
                # Obtiene del metodo to_json de la clase TiposDocumentos los valores en formato JSON          
                jsonTDocto = _Area.to_json()

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
                Logger.add_to_log("critical", str('*** def AreaSvos.consulta_area ***'))
                Logger.add_to_log("critical", str(ex))
                Logger.add_to_log("critical", traceback.format_exc())
                # No es un error de Sistema. El error esta en la operacion en la BBDD y la mayor parte de los casos es por datos
                ErrorSistema = False
                return (True, msgErrorDef, ErrorSistema)
            
        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def AreaSvos.consulta_area ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def actualiza_area(cls, _Area, argNumVersion, argCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(argCurrentApp)  
            connection = db.conexion()

            fchActualizacion = dt.now()
            fchActualizacion = fchActualizacion.strftime("%m/%d/%Y %H:%M:%S")            
            cursor = db.cursor()
            query = f'''UPDATE area SET cve_area = %s, nombre = %s, vigente = %s, observaciones = %s,
                               id_usuario_actualiza = %s, fecha_actualizacion = %s WHERE id = %s
                    '''
            datos = (_Area.cve_area, _Area.nombre, _Area.vigente, _Area.observaciones, _Area.id_usuario_actualiza, fchActualizacion, _Area.id)
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
                Logger.add_to_log("critical", str('*** def AreaSvos.actualiza_area ***'))
                Logger.add_to_log("critical", str(ex))
                Logger.add_to_log("critical", traceback.format_exc())
                # No es un error de Sistema. El error esta en la operacion en la BBDD y la mayor parte de los casos es por datos
                ErrorSistema = False
                return (True, msgErrorDef, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def AreaSvos.actualiza_area ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)


