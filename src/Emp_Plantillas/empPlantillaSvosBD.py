#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime as dt

from pprint import pprint

class EmpresaPlantillaSvos():
    @classmethod
    def lista_empPlantillaDoctos(cls, _empresaPlantilla, argNumVersion, ArgCurrentApp):
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
                query = f'''SELECT ep.id, ep.id_emp_proceso, epr.id_empresa, ep.id_tdocto, td.nombre_corto, ep.id_docto, nd.nombre,
                                   ep.observaciones, ep.vigente, ep.obligatorio, ep.vigencia, 
                                   ep.id_usuario_alta, to_char(ep.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), 
	                               ep.id_usuario_actualiza, to_char(ep.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS')		
                            FROM   emp_plantilla ep , emp_proceso epr , tipos_documento td , nombre_documento nd
                            WHERE ep.id_emp_proceso = epr.id 
                            AND ep.id_tdocto = td.id_tipo_docto 
                            AND ep.id_docto = nd.id_nombre_docto;'''
            else:            
                query = f'''SELECT ep.id, ep.id_emp_proceso, epr.id_empresa, ep.id_tdocto, td.nombre_corto, ep.id_docto, nd.nombre,
                                   ep.observaciones, ep.vigente, ep.obligatorio, ep.vigencia, 
                                   ep.id_usuario_alta, to_char(ep.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), 
	                               ep.id_usuario_actualiza, to_char(ep.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS')		
                            FROM   emp_plantilla ep , emp_proceso epr , tipos_documento td , nombre_documento nd
                            WHERE ep.id_emp_proceso = epr.id 
                            AND ep.id_tdocto = td.id_tipo_docto 
                            AND ep.id_docto = nd.id_nombre_docto AND ep.id_emp_proceso = {_empresaPlantilla.id_emp_proceso};'''
                
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

            lstempresaPlantilla = []
            # La respuesta es una lista de listas, la respuesta debe ser en un JSON
            resJSON = []
            for ePlantilla in respuesta:
                lstRegistro = [] 
                str_id = ePlantilla[0]                         # Id de la plantilla empresa-proceso
                str_id_emp_proceso = ePlantilla[1]             # Id de la empresa proceso
                str_id_empresa = ePlantilla[2]                 # Id de la empresa
                str_id_tdocto = ePlantilla[3]                  # Id del tipo de docto
                str_nom_tdocto = ePlantilla[4]                 # Nombre del tipo de docto
                str_id_docto = ePlantilla[5]                   # ID del documento
                str_nom_docto = ePlantilla[6]                  # Nombre del documento
                str_obs = ePlantilla[7]                        # Observaciones de la Plantilla
                str_vigente = ePlantilla[8]                    # Docto Vigente en la Plantilla
                str_obligatorio = ePlantilla[9]                # Docto es Obligatorio en la Plantilla
                str_vigencia = ePlantilla[10]                  # Vigencia del Docto en la Plantilla
                str_usuarioAlta = ePlantilla[11]               # Id usuario de alta
                str_fechaAlta = ePlantilla[12]                 # Fecha de alta
                str_usuarioActualiza = ePlantilla[13]          # Id usuario que actualizo
                str_fechaActualizacion = ePlantilla[14]        # Fecha de actualizacion

                # Agregamos los datos del tipo de documento a lstRegistro
                lstRegistro.append(str_id)        
                lstRegistro.append(str_id_emp_proceso)        
                lstRegistro.append(str_id_empresa)        
                lstRegistro.append(str_id_tdocto)        
                lstRegistro.append(str_nom_tdocto)        
                lstRegistro.append(str_id_docto)        
                lstRegistro.append(str_nom_docto)        
                lstRegistro.append(str_obs)        
                lstRegistro.append(str_vigente)        
                lstRegistro.append(str_obligatorio)        
                lstRegistro.append(str_vigencia)        
                lstRegistro.append(str_usuarioAlta)        
                lstRegistro.append(str_fechaAlta)        
                lstRegistro.append(str_usuarioActualiza)        
                lstRegistro.append(str_fechaActualizacion)        

                # Agregamos lstRegistro a la lista de tipos de documemtos lstempresaPlantilla
                lstempresaPlantilla.append(lstRegistro)    

            campos = ('id', 'id_emp_proceso', 'id_empresa', 'id_tdocto','nom_tdocto', 'id_docto', 'nom_docto', 'observaciones', 'vigente' , 'obligatorio','vigencia', 'id_usuario_alta', 'fecha_alta', 'id_usuario_actualiza', 'fecha_actualizacion')
            for registro in lstempresaPlantilla:
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
            Logger.add_to_log("critical", str('*** def empresaPlantillaSvos.lista_empPlantillaDoctos ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def alta_empPlantillaDocto(cls, _empresaPlantilla, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()

            query = f'''INSERT INTO emp_plantilla 
                            (id_emp_proceso, id_tdocto, id_docto, observaciones, vigente, obligatorio, vigencia, id_usuario_alta)
                        VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s);
                    '''
            datos = (_empresaPlantilla.id_emp_proceso, _empresaPlantilla.id_tdocto, _empresaPlantilla.id_docto, _empresaPlantilla.observaciones, _empresaPlantilla.vigente, _empresaPlantilla.obligatorio, _empresaPlantilla.vigencia, _empresaPlantilla.id_usuario_alta)
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
            Logger.add_to_log("critical", str('*** def empresaPlantillaSvos.alta_empPlantillaDocto ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def consulta_empPlantillaDocto(cls, _empresaPlantilla, argNumVersion, ArgCurrentApp):
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
            query = f'''SELECT ep.id, ep.id_emp_proceso, epr.id_empresa, ep.id_tdocto, td.nombre_corto, ep.id_docto, nd.nombre,
                                   ep.observaciones, ep.vigente, ep.obligatorio, ep.vigencia, 
                                   ep.id_usuario_alta, to_char(ep.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), 
	                               ep.id_usuario_actualiza, to_char(ep.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS')		
                            FROM   emp_plantilla ep , emp_proceso epr , tipos_documento td , nombre_documento nd
                            WHERE ep.id_emp_proceso = epr.id 
                            AND ep.id_tdocto = td.id_tipo_docto 
                            AND ep.id_docto = nd.id_nombre_docto AND ep.id = {_empresaPlantilla.id};'''

            cursor.execute(query)
            respuesta = cursor.fetchall()
            regtoePlantilla = respuesta
            if connection:
                cursor.close()
                connection.close()

            #Valida si datdEmpoEmp esta vacio
            if (len(regtoePlantilla) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            _empresaPlantilla.id = regtoePlantilla[0][0]
            _empresaPlantilla.id_emp_proceso = regtoePlantilla[0][1]
            _empresaPlantilla.id_empresa = regtoePlantilla[0][2]
            _empresaPlantilla.id_tdocto = regtoePlantilla[0][3]
            _empresaPlantilla.nom_tdocto = regtoePlantilla[0][4]
            _empresaPlantilla.id_docto = regtoePlantilla[0][5]
            _empresaPlantilla.nombre = regtoePlantilla[0][6]
            _empresaPlantilla.observaciones = regtoePlantilla[0][7]
            _empresaPlantilla.vigente = regtoePlantilla[0][8]
            _empresaPlantilla.obligatorio = regtoePlantilla[0][9]
            _empresaPlantilla.vigencia = regtoePlantilla[0][10]
            _empresaPlantilla.id_usuario_alta = regtoePlantilla[0][11]
            _empresaPlantilla.fecha_alta = regtoePlantilla[0][12]
            _empresaPlantilla.id_usuario_actualiza = regtoePlantilla[0][13]
            _empresaPlantilla.fecha_actualizacion = regtoePlantilla[0][14]
            # Obtiene del metodo to_json de la clase _empresaPlantilla los valores en formato JSON          
            jsonEmpPlantilla = _empresaPlantilla.to_json()

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = jsonEmpPlantilla
            datosRespuesta['error'] = False
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            if connection:
                cursor.close()
                connection.close()
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def empresaPlantillaSvos.consulta_empPlantillaDocto ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def actualiza_empPlantillaDocto(cls, _empresaPlantilla, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()

            fchActualizacion = dt.now()
            fchActualizacion = fchActualizacion.strftime("%m/%d/%Y %H:%M:%S")

            query = f'''UPDATE emp_plantilla SET id_tdocto = %s, id_docto = %s, observaciones = %s, vigente = %s, obligatorio = %s,
                               vigencia = %s, id_usuario_actualiza = %s, fecha_actualizacion = %s WHERE id = %s
                    '''
            datos = (_empresaPlantilla.id_tdocto, _empresaPlantilla.id_docto, _empresaPlantilla.observaciones, _empresaPlantilla.vigente, _empresaPlantilla.obligatorio, _empresaPlantilla.vigencia, _empresaPlantilla.id_usuario_actualiza, fchActualizacion, _empresaPlantilla.id)
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
            Logger.add_to_log("critical", str('*** def empresaPlantillaSvos.actualiza_empPlantillaDocto ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)


