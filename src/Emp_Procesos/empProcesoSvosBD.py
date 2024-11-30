#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime as dt

from pprint import pprint

class EmpresaProcesoSvos():
    @classmethod
    def lista_empresaProcesos(cls, _EmpresaProceso, argNumVersion, ArgCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()

            if (argNumVersion == 0):
                query = f'''SELECT ep.id, ep.id_empresa, ep.id_area, a.nombre, ep.id_proceso, p.nombre, ep.observaciones, ep.vigente, 
                                ep.id_usuario_alta, to_char(ep.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), ep.id_usuario_actualiza, 
                                to_char(ep.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS')	
                            FROM emp_proceso ep, area a, proceso p 
                            WHERE ep.id_area = a.id and ep.id_proceso = p.id;'''
            else:            
                query = f'''SELECT ep.id, ep.id_empresa, ep.id_area, a.nombre, ep.id_proceso, p.nombre, ep.observaciones, ep.vigente, 
                                ep.id_usuario_alta, to_char(ep.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), ep.id_usuario_actualiza, 
                                to_char(ep.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS')	
                            FROM emp_proceso ep, area a, proceso p 
                            WHERE ep.id_area = a.id AND  ep.id_proceso = p.id AND ep.id_empresa = {_EmpresaProceso.id_empresa};'''
                
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

            lstEmpresaProceso = []
            # La respuesta es una lista de listas, la respuesta debe ser en un JSON
            resJSON = []
            for eProceso in respuesta:
                lstRegistro = [] 
                str_id = eProceso[0]                         # Id de la plantilla empresa-proceso
                str_id_empresa = eProceso[1]                 # Id de la empresa
                str_id_area = eProceso[2]                    # Id del area
                str_nom_area = eProceso[3]                   # Nombre del area
                str_id_proceso = eProceso[4]                 # ID del Proceso
                str_nom_proceso = eProceso[5]                # Nombre del proceso
                str_obs = eProceso[6]                        # Observaciones de la Plantilla
                str_vigente = eProceso[7]                    # Vigencia de la Plantilla
                str_usuarioAlta = eProceso[8]                # Id usuario de alta
                str_fechaAlta = eProceso[9]                  # Fecha de alta
                str_usuarioActualiza = eProceso[10]          # Id usuario que actualizo
                str_fechaActualizacion = eProceso[11]        # Fecha de actualizacion

                # Agregamos los datos del tipo de documento a lstRegistro
                lstRegistro.append(str_id)        
                lstRegistro.append(str_id_empresa)        
                lstRegistro.append(str_id_area)        
                lstRegistro.append(str_nom_area)        
                lstRegistro.append(str_id_proceso)        
                lstRegistro.append(str_nom_proceso)        
                lstRegistro.append(str_obs)        
                lstRegistro.append(str_vigente)        
                lstRegistro.append(str_usuarioAlta)        
                lstRegistro.append(str_fechaAlta)        
                lstRegistro.append(str_usuarioActualiza)        
                lstRegistro.append(str_fechaActualizacion)        

                # Agregamos lstRegistro a la lista de tipos de documemtos lstEmpresaProceso
                lstEmpresaProceso.append(lstRegistro)    

            campos = ('id','id_empresa','id_area','nombre_area', 'id_proceso', 'nombre_proceso', 'observaciones', 'vigente' ,'id_usuario_alta', 'fecha_alta', 'id_usuario_actualiza', 'fecha_actualizacion')
            for registro in lstEmpresaProceso:
                resJSON.append(dict(zip(campos, registro)))

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = resJSON
            datosRespuesta['error'] = False
            ErrorSistema = False

            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            if connection:
                cursor.close()
                connection.close()
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def EmpresaProcesoSvos.lista_empresaProcesos ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def alta_empresaProceso(cls, _EmpresaProceso, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()

            query = f'''INSERT INTO emp_proceso 
                            (id_empresa, id_area, id_proceso, observaciones, id_usuario_alta)
                        VALUES
                            (%s, %s, %s, %s, %s);
                    '''
            datos = (_EmpresaProceso.id_empresa, _EmpresaProceso.id_area, _EmpresaProceso.id_proceso, _EmpresaProceso.observaciones, _EmpresaProceso.id_usuario_alta)
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
            if connection:
                cursor.close()
                connection.close()
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def EmpresaProcesoSvos.alta_empresaProceso ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def consulta_empresaProceso(cls, _EmpresaProceso, argNumVersion, ArgCurrentApp):
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

            query = f'''SELECT ep.id, ep.id_empresa, ep.id_area, a.nombre, ep.id_proceso, p.nombre, ep.observaciones, ep.vigente, 
                               ep.id_usuario_alta, to_char(ep.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), ep.id_usuario_actualiza, 
                               to_char(ep.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS')	
                        FROM emp_proceso ep, area a, proceso p 
                        WHERE ep.id_area = a.id AND ep.id_proceso = p.id AND ep.id = {_EmpresaProceso.id};'''

            cursor.execute(query)
            respuesta = cursor.fetchall()
            regtoeProceso = respuesta
            if connection:
                cursor.close()
                connection.close()

            #Valida si datdEmpoEmp esta vacio
            if (len(regtoeProceso) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            _EmpresaProceso.id = regtoeProceso[0][0]
            _EmpresaProceso.id_empresa = regtoeProceso[0][1]
            _EmpresaProceso.id_area = regtoeProceso[0][2]
            _EmpresaProceso.nombre_area = regtoeProceso[0][3]
            _EmpresaProceso.id_proceso = regtoeProceso[0][4]
            _EmpresaProceso.nombre_proceso = regtoeProceso[0][5]
            _EmpresaProceso.observaciones = regtoeProceso[0][6]
            _EmpresaProceso.vigente = regtoeProceso[0][7]
            _EmpresaProceso.id_usuario_alta = regtoeProceso[0][8]
            _EmpresaProceso.fecha_alta = regtoeProceso[0][9]
            _EmpresaProceso.id_usuario_actualiza = regtoeProceso[0][10]
            _EmpresaProceso.fecha_actualizacion = regtoeProceso[0][11]
            # Obtiene del metodo to_json de la clase _EmpresaProceso los valores en formato JSON          
            jsonNombreDocto = _EmpresaProceso.to_json()

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = jsonNombreDocto
            datosRespuesta['error'] = False
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            if connection:
                cursor.close()
                connection.close()
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def EmpresaProcesoSvos.consulta_empresaProceso ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def actualiza_EmpresaProceso(cls, _EmpresaProceso, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()

            fchActualizacion = dt.now()
            fchActualizacion = fchActualizacion.strftime("%m/%d/%Y %H:%M:%S")            

            query = f'''UPDATE emp_proceso SET id_area = %s, id_proceso = %s, observaciones = %s, vigente = %s, 
                               id_usuario_actualiza = %s, fecha_actualizacion = %s WHERE id = %s
                    '''
            datos = (_EmpresaProceso.id_area, _EmpresaProceso.id_proceso, _EmpresaProceso.observaciones, _EmpresaProceso.vigente, _EmpresaProceso.id_usuario_actualiza, fchActualizacion, _EmpresaProceso.id)
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
            if connection:
                cursor.close()
                connection.close()
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def EmpresaProcesoSvos.actualiza_EmpresaProceso ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

