#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from flask import current_app

from datetime import datetime as dt

class setupSvos():
    @classmethod
    def lista_endpointBAJA(cls, ArgCurrentApp):
        try:
            _glb_endPoints = []

            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''SELECT id, endpoint, observaciones, vigente
                        FROM endpoint WHERE vigente = false ;'''

            cursor.execute(query)
            respuesta = cursor.fetchall()
            datosResultado = respuesta
            if connection:
                cursor.close()
                connection.close()

            #Valida si datosResultado esta vacio
            if (len(datosResultado) <= 0):
                _glb_endPoints = []
                return _glb_endPoints

            # La respuesta es una lista de listas, la respuesta debe ser en un JSON
            resJSON = []
            for epoint in respuesta:
                lstRegistro = []
                str_id = epoint[0]                         # Id del endpoint
                str_endpoint = epoint[1]                   # URI del endpoint
                str_observaciones = epoint[2]              # Observaciones del endpoint
                str_vigente = epoint[3]                    # Estado del endpoint

                # Agregamos los datos de los EndPoints a lstRegistro
                lstRegistro.append(str_id)        
                lstRegistro.append(str_endpoint)        
                lstRegistro.append(str_observaciones)        
                lstRegistro.append(str_vigente)        

                # Agregamos lstRegistro a la lista de EndPoints
                _glb_endPoints.append(lstRegistro)    

            return _glb_endPoints

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def setupSvos.lista_endpointBAJA ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            return
        
    @classmethod
    def valida_soporteAPI(cls, uri_API):
    #   =====================================================================================================
    #   Funcion que valida si la uri_API solicitada a la APP SmartDOC, esta obsoleta o vigente
    #   =====================================================================================================
    # Obtiene el arreglo con las API obsoletas (Sin Soporte) en la variable 'endPoint_baja', de la configuracion de App
        endPoint_baja = current_app.config['endPoint_baja']
        # Se busca en la lista de EndPoint obsoletos (baja) si existe el endpoint invocado
        str_match = list(filter(lambda x: uri_API in x, endPoint_baja))
        numOcurrencia = len(str_match)

        if (numOcurrencia == 0):
            return (False, 'Vigente')            # No se encontro la uri_API ... vigente
        else: 
            strObs = (str_match[0][2])
            return (True, strObs)                # Se encontro la uri_API ... obsoleta

