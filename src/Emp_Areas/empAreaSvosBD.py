#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime as dt

from pprint import pprint

class EmpresaAreaSvos():
    @classmethod
    def lista_empresaAreas(cls, argNumVersion, ArgCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''SELECT ea.id, ea.id_empresa, ea.id_area, a.cve_area, a.nombre,
                               ea.id_usuario_alta,  to_char(ea.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), ea.id_usuario_actualiza, 
                               to_char(ea.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS') 
                        FROM emp_areas ea , area a 
                        WHERE ea.id_area = a.id;'''
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

            lstEmpresaAreas = []
            # La respuesta es una lista de listas, la respuesta debe ser en un JSON
            resJSON = []
            for eArea in respuesta:
                lstRegistro = [] 
                str_id = eArea[0]                         # Id del nombre de documento
                str_id_empresa = eArea[1]                 # Nombre de documento
                str_id_area = eArea[2]                    # Observaciones del nombre de documento
                str_cve_area = eArea[3]                   # Estado del nombre de documento
                str_nombre_area = eArea[4]                # ID del tipo de documento asociado
                str_usuarioAlta = eArea[5]                # Id usuario de alta
                str_fechaAlta = eArea[6]                  # Fecha de alta
                str_usuarioActualiza = eArea[7]           # Id usuario que actualizo
                str_fechaActualizacion = eArea[8]         # Fecha de actualizacion

                # Agregamos los datos del tipo de documento a lstRegistro
                lstRegistro.append(str_id)        
                lstRegistro.append(str_id_empresa)        
                lstRegistro.append(str_id_area)        
                lstRegistro.append(str_cve_area)        
                lstRegistro.append(str_nombre_area)        
                lstRegistro.append(str_usuarioAlta)        
                lstRegistro.append(str_fechaAlta)        
                lstRegistro.append(str_usuarioActualiza)        
                lstRegistro.append(str_fechaActualizacion)        

                # Agregamos lstRegistro a la lista de tipos de documemtos lstEmpresaAreas
                lstEmpresaAreas.append(lstRegistro)    

            campos = ('id','id_empresa','id_area', 'cve_area', 'nombre_area', 'id_usuario_alta', 'fecha_alta', 'id_usuario_actualiza', 'fecha_actualizacion')
            for registro in lstEmpresaAreas:
                resJSON.append(dict(zip(campos, registro)))

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = resJSON
            datosRespuesta['error'] = False
            ErrorSistema = False

            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def EmpresaAreaSvos.lista_empresaAreas ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def alta_empresaArea(cls, _EmpresaArea, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''INSERT INTO emp_areas 
                            (id_empresa, id_area, id_usuario_alta)
                        VALUES
                            (%s, %s, %s);
                    '''
            datos = (_EmpresaArea.id_empresa, _EmpresaArea.id_area, _EmpresaArea.id_usuario_alta)
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
            Logger.add_to_log("critical", str('*** def EmpresaAreaSvos.alta_empresaArea ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def consulta_empresaArea(cls, _EmpresaArea, argNumVersion, ArgCurrentApp):
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

            query = f'''SELECT ea.id, ea.id_empresa, ea.id_area, a.cve_area, a.nombre,
                               ea.id_usuario_alta,  to_char(ea.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), ea.id_usuario_actualiza, 
                               to_char(ea.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS') 
                        FROM emp_areas ea , area a 
                        WHERE ea.id_area = a.id AND ea.id = {_EmpresaArea.id};'''

            cursor.execute(query)
            respuesta = cursor.fetchall()
            regtoEArea = respuesta
            if connection:
                cursor.close()
                connection.close()

            #Valida si datdEmpoEmp esta vacio
            if (len(regtoEArea) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            _EmpresaArea.id = regtoEArea[0][0]
            _EmpresaArea.id_empresa = regtoEArea[0][1]
            _EmpresaArea.id_area = regtoEArea[0][2]
            _EmpresaArea.cve_area = regtoEArea[0][3]
            _EmpresaArea.nombre_area = regtoEArea[0][4]
            _EmpresaArea.id_usuario_alta = regtoEArea[0][5]
            _EmpresaArea.fecha_alta = regtoEArea[0][6]
            _EmpresaArea.id_usuario_actualiza = regtoEArea[0][7]
            _EmpresaArea.fecha_actualizacion = regtoEArea[0][8]
            # Obtiene del metodo to_json de la clase _EmpresaArea los valores en formato JSON          
            jsonNombreDocto = _EmpresaArea.to_json()

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = jsonNombreDocto
            datosRespuesta['error'] = False
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def EmpresaAreaSvos.consulta_empresaArea ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def actualiza_empresaArea(cls, _EmpresaArea, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()

            fchActualizacion = dt.now()
            fchActualizacion = fchActualizacion.strftime("%m/%d/%Y %H:%M:%S")            

            query = f'''UPDATE emp_areas SET id_area = %s,  
                               id_usuario_actualiza = %s, fecha_actualizacion = %s WHERE id = %s
                    '''
            datos = (_EmpresaArea.id_area, _EmpresaArea.id_usuario_actualiza, fchActualizacion, _EmpresaArea.id)
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
            Logger.add_to_log("critical", str('*** def EmpresaAreaSvos.actualiza_empresaArea ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)


