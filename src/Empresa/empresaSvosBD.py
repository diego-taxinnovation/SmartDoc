#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Del componente ModeloEmpresa.py importa la clase Empresa
from src.Empresa.empresaModelo import Empresa

#   SERVICIOS. Del componente SeguridadServicios.py importa la clase EncriptacionSvos
#from app.admin.Servicios.SeguridadServicios import EncriptacionSvos, TokenSvos

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime as dt

class EmpresaSvos():
    @classmethod
    def lista_empresa(cls, argNumVersion, ArgCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''SELECT id, cve_empresa, nombre, observaciones, uso_webhook, vigente, id_usuario_alta,
                        to_char("fecha_alta", 'DD/MM/YYYY HH:MM:SS') , id_usuario_actualiza, to_char("fecha_actualizacion", 'DD/MM/YYYY HH:MM:SS') FROM empresa;'''

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

            lstEmpresas = []
            # La respuesta es una lista de listas, la respuesta debe ser en un JSON
            resJSON = []
            for empresa in respuesta:
                lstRegistro = []
                str_id = empresa[0]                         # Id de la empresa
                str_cveEmpresa = empresa[1]                 # Clave de la Empresa
                str_nombre = empresa[2]                     # Nombre de la Empresa
                str_observaciones = empresa[3]              # Observaciones de la Empresa
                str_usoWebhook = empresa[4]                 # Uso de Webhook (url)
                str_vigente = empresa[5]                    # Estado de la Empresa
                str_usuarioAlta = empresa[6]                # Id usuario de alta
                str_fechaAlta = empresa[7]                  # Fecha de alta
                str_usuarioActualiza = empresa[8]           # Id usuario que actualizo
                str_fechaActualizacion = empresa[9]         # Fecha de actualizacion

                # Agregamos los datos de las Empresas a lstRegistro
                lstRegistro.append(str_id)        
                lstRegistro.append(str_cveEmpresa)        
                lstRegistro.append(str_nombre)        
                lstRegistro.append(str_observaciones)        
                lstRegistro.append(str_usoWebhook)        
                lstRegistro.append(str_vigente)        
                lstRegistro.append(str_usuarioAlta)        
                lstRegistro.append(str_fechaAlta)        
                lstRegistro.append(str_usuarioActualiza)        
                lstRegistro.append(str_fechaActualizacion)        

                # Agregamos lstRegistro a la lista de tipos de documemtos lstEmpresas
                lstEmpresas.append(lstRegistro)    

            campos = ('id','cve_empresa','nombre', 'observaciones', 'uso_webhook', 'vigente', 'id_usuario_alta', 'fecha_alta', 'id_usuario_actualiza', 'fecha_actualizacion')
            for registro in lstEmpresas:
                resJSON.append(dict(zip(campos, registro)))

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = resJSON
            datosRespuesta['error'] = False
            ErrorSistema = False

            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def EmpresaSvos.lista_empresa ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def alta_empresa(cls, argEmpresa, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''INSERT INTO empresa 
                            (cve_empresa, nombre, observaciones, uso_webhook, id_usuario_alta)
                        VALUES
                            (%s, %s, %s, %s, %s);
                    '''
            datos = (argEmpresa.cve_empresa, argEmpresa.nombre, argEmpresa.observaciones, argEmpresa.uso_webhook, argEmpresa.id_usuario_alta)
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
            Logger.add_to_log("critical", str('*** def EmpresaSvos.alta_empresa ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def consulta_empresa(cls, argIdEmpresa, argNumVersion, ArgCurrentApp):
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
            query = f'''SELECT id, cve_empresa, nombre, observaciones, uso_webhook, vigente, id_usuario_alta,
                        to_char("fecha_alta", 'DD/MM/YYYY HH:MM:SS'), id_usuario_actualiza, to_char("fecha_actualizacion", 'DD/MM/YYYY HH:MM:SS')
                        FROM empresa WHERE id = {argIdEmpresa} ;'''

            cursor.execute(query)
            respuesta = cursor.fetchall()
            dEmp = respuesta
            if connection:
                cursor.close()
                connection.close()

            #Valida si datdEmpoEmp esta vacio
            if (len(dEmp) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            # Crea una instancia de la clase Empresa con los valores obtenidos de la consulta a la BBDD
            _empresa = Empresa(dEmp[0][0], dEmp[0][1], dEmp[0][2], dEmp[0][3], dEmp[0][4], dEmp[0][5], dEmp[0][6], dEmp[0][7], dEmp[0][8], dEmp[0][9])
            # Obtiene del metodo to_json de la clase Empresa los valores en formato JSON          
            jsonEmpresa = _empresa.to_json()

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = jsonEmpresa
            datosRespuesta['error'] = False
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def EmpresaSvos.consulta_empresa ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

    @classmethod
    def actualiza_empresa(cls, argEmpresa, argNumVersion, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()

            fchActualizacion = dt.now()
            fchActualizacion = fchActualizacion.strftime("%m/%d/%Y %H:%M:%S")            
            query = f'''UPDATE empresa SET cve_empresa = %s, nombre = %s, observaciones = %s, uso_webhook = %s, vigente = %s, id_usuario_actualiza = %s, fecha_actualizacion = %s WHERE id = %s
                    '''
            datos = (argEmpresa.cve_empresa, argEmpresa.nombre, argEmpresa.observaciones, argEmpresa.uso_webhook, argEmpresa.vigente, argEmpresa.id_usuario_actualiza, fchActualizacion, argEmpresa.id)
            cursor.execute(query, (datos))
            connection.commit()
            if connection:
                cursor.close()
                connection.close()

            datosRespuesta = {
                'error': False, 
                'mensaje': 'Actualizacion realizada exitosamente'
            }
            
            ErrorSistema = False
            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def EmpresaSvos.alta_empresa ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

