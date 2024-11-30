#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback

#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   UTILERIAS. Del componente logger.py importa la funcion excepcionInformacion
from src.Utilerias.logs import excepcionInformacion

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime
#*******************************************************************************************
#   BITACORA   
#   Definimos la clase BitacoraSvos
#*******************************************************************************************
class BitacoraSvos():
    @classmethod
    #   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #   Metodo para insertar registro en la bitacora, considerando Aplicacion y Tipo de operacion
    #   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def alta_bitacora(cls, argBitacora, argCurrentApp):
        try: 
            if argBitacora.cve_empresa != '':
                argEmpresa = argBitacora.cve_empresa
            else:
                argEmpresa = 'DIGITEK' 

            argAplicacion = argBitacora.cve_aplicacion 
            argUsuario = argBitacora.cve_usuario
            argOperacion = argBitacora.cve_operacion
            argEstado = argBitacora.estado
            argEntrada = argBitacora.entrada
            argSalida = argBitacora.salida
            argModulo = argBitacora.modulo
            argPantalla = argBitacora.pantalla
            argErrSistema = argBitacora.err_sistema
            argLatitud = argBitacora.latitud
            arglongitud = argBitacora.longitud
            argIPcliente = argBitacora.ip_cliente
            argRealizado = argBitacora.realizado

            db = PostgresBase(argCurrentApp)
            connection = db.conexion()
            if (connection == False):
                msgErrorClass = 'Servicio no disponible por el momento. (cod0100)'
                return (True, msgErrorClass)
            
            cursor = db.cursor()
            query = 'INSERT INTO bitacora '
            query += f''' (cve_empresa, cve_aplicacion, cve_usuario, cve_operacion, estado, contenido_in, contenido_ou, modulo, pantalla, err_sistema, latitud, longitud, ip_cliente, realizado)
                        VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    '''
            datos = (argEmpresa, argAplicacion, argUsuario, argOperacion, argEstado, argEntrada, argSalida, argModulo, argPantalla, argErrSistema, argLatitud, arglongitud, argIPcliente, argRealizado)

            cursor.execute(query, (datos))
            connection.commit()
            cursor.close()
            connection.close()
            resp = {
                    'error': False, 
                    'mensaje': 'Registro en bitacora realizada exitosamente'
            }
            return (False, resp)

        except Exception as ex:
            Logger.add_to_log("warn", str('===================================================================='))
            Logger.add_to_log("warn", str('*** class BitacoraSvos.alta_bitacora ***'))
            Logger.add_to_log("warn", str(ex))
            Logger.add_to_log("warn", traceback.format_exc())
            msgErrorClass = 'Servicio no disponible por el momento'
            return (True, msgErrorClass)
            