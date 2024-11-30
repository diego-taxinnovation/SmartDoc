#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Del componente procesoModelo.py importa la clase Proceso
from src.Procesos.procesoModelo import Proceso

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime as dt

class ProcesosSvos():
    @classmethod
    def lista_procesos(cls, argNumVersion, ArgCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''SELECT id, cve_proceso, nombre, observaciones, vigente, id_usuario_alta,
                        to_char("fecha_alta", 'DD/MM/YYYY HH:MM:SS') , id_usuario_actualiza, to_char("fecha_actualizacion", 'DD/MM/YYYY HH:MM:SS') FROM proceso;'''

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

            lstProcesos = []
            # La respuesta es una lista de listas, la respuesta debe ser en un JSON
            resJSON = []
            for proceso in respuesta:
                lstRegistro = []
                str_id = proceso[0]                         # Id del proceso
                str_cve_proceso = proceso[1]                # Clave del proceso
                str_nombre = proceso[2]                     # Nombre del proceso
                str_observaciones = proceso[3]              # Observaciones del proceso
                str_vigente = proceso[4]                    # Estado del proceso
                str_usuarioAlta = proceso[5]                # Id usuario de alta
                str_fechaAlta = proceso[6]                  # Fecha de alta
                str_usuarioActualiza = proceso[7]           # Id usuario que actualizo
                str_fechaActualizacion = proceso[8]         # Fecha de actualizacion

                # Agregamos los datos de las Empresas a lstRegistro
                lstRegistro.append(str_id)        
                lstRegistro.append(str_cve_proceso)        
                lstRegistro.append(str_nombre)        
                lstRegistro.append(str_observaciones)        
                lstRegistro.append(str_vigente)        
                lstRegistro.append(str_usuarioAlta)        
                lstRegistro.append(str_fechaAlta)        
                lstRegistro.append(str_usuarioActualiza)        
                lstRegistro.append(str_fechaActualizacion)        

                # Agregamos lstRegistro a la lista de tipos de documemtos lstProcesos
                lstProcesos.append(lstRegistro)    

            campos = ('id','cve_proceso','nombre', 'observaciones', 'vigente', 'id_usuario_alta', 'fecha_alta', 'id_usuario_actualiza', 'fecha_actualizacion')
            for registro in lstProcesos:
                resJSON.append(dict(zip(campos, registro)))

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = resJSON
            datosRespuesta['error'] = False
            ErrorSistema = False

            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def ProcesosSvos.lista_procesos ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def alta_proceso(cls, _Proceso, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''INSERT INTO proceso 
                            (cve_proceso, nombre, observaciones, id_usuario_alta)
                        VALUES
                            (%s, %s, %s, %s);
                    '''
            datos = (_Proceso.cve_proceso, _Proceso.nombre, _Proceso.observaciones, _Proceso.id_usuario_alta)
            cursor.execute(query, (datos))
            connection.commit()
            if connection:
                cursor.close()
                connection.close()

            datosRespuesta = {
                'error': False, 
                'mensaje': 'Alta realizada exitosamente'
            }
            
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def ProcesosSvos.alta_proceso ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def consulta_proceso(cls, _Proceso, argNumVersion, ArgCurrentApp):
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
            query = f'''SELECT id, cve_proceso, nombre, observaciones, vigente, id_usuario_alta,
                        to_char("fecha_alta", 'DD/MM/YYYY HH:MM:SS') , id_usuario_actualiza, to_char("fecha_actualizacion", 'DD/MM/YYYY HH:MM:SS') 
                        FROM proceso WHERE id = {_Proceso.id};'''

            cursor.execute(query)

            respuesta = cursor.fetchall()
            regtoProceso = respuesta
            if connection:
                cursor.close()
                connection.close()

            #Valida si datdEmpoEmp esta vacio
            if (len(regtoProceso) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            _Proceso.id = regtoProceso[0][0]
            _Proceso.cve_proceso = regtoProceso[0][1]
            _Proceso.nombre = regtoProceso[0][2]
            _Proceso.observaciones = regtoProceso[0][3]
            _Proceso.vigente = regtoProceso[0][4]
            _Proceso.id_usuario_alta = regtoProceso[0][5]
            _Proceso.fecha_alta = regtoProceso[0][6]
            _Proceso.id_usuario_actualiza = regtoProceso[0][7]
            _Proceso.fecha_actualizacion = regtoProceso[0][8]
            # Obtiene del metodo to_json de la clase Empresa los valores en formato JSON          
            jsonProceso = _Proceso.to_json()

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = jsonProceso
            datosRespuesta['error'] = False
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def ProcesosSvos.consulta_proceso ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def actualiza_proceso(cls, _Proceso, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()

            fchActualizacion = dt.now()
            fchActualizacion = fchActualizacion.strftime("%m/%d/%Y %H:%M:%S")            
            query = f'''UPDATE proceso SET cve_proceso = %s, nombre = %s, observaciones = %s, vigente = %s, id_usuario_actualiza = %s, fecha_actualizacion = %s WHERE id = %s
                    '''
            datos = (_Proceso.cve_proceso, _Proceso.nombre, _Proceso.observaciones, _Proceso.vigente, _Proceso.id_usuario_actualiza, fchActualizacion, _Proceso.id)
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
            Logger.add_to_log("critical", str('*** def ProcesosSvos.actualiza_proceso ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

