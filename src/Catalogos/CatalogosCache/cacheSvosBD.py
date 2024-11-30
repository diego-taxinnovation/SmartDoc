#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Del componente procesoModelo.py importa la clase Proceso
from src.Catalogos.Area.areaModelo import Area

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

import itertools 

from datetime import datetime as dt

from pprint import pprint

# ===================================================================
# Obtiene la informacion del catalogo de Areas
# ===================================================================
def catalogos_cache(_argCursor, _argQuery):
    # try para manejo de excepciones en las operaciones a la BBDD
    try:
        flagError = False
        datosDetalle = {}
        _argCursor.execute(_argQuery)
        respuesta = _argCursor.fetchall()
        datosResultado = respuesta

        #Valida si datosResultado esta vacio
        if (len(datosResultado) <= 0):
            flagError = False
            return (flagError, datosDetalle)

        lstDatos = []
        for dato in respuesta:
            lstRegistro = []
            str_id = dato[0]                         # Id del dato
            str_cve_area = dato[1]                   # Clave del dato
            str_nombre = dato[2]                     # Nombre del dato
            str_idAsociado = dato[3]                 # ID de la registro Maestro asociado (SI aplica)

            # Agregamos los datos a lstRegistro
            lstRegistro.append(str_id)        
            lstRegistro.append(str_cve_area)        
            lstRegistro.append(str_nombre)        
            lstRegistro.append(str_idAsociado)        

            # Agregamos lstRegistro a la lista de Datos
            lstDatos.append(lstRegistro)    

        # La respuesta es una lista de Datos, la respuesta debe ser en un JSON
        resJSON = []
        campos = ('id','cve','nombre', 'id_asociado')
        for registro in lstDatos:
            resJSON.append(dict(zip(campos, registro)))

        return (resJSON)


    except Exception as ex:
        Logger.add_to_log("critical", str('===================================================================='))
        Logger.add_to_log("critical", str('*** def AreaSvos.lista_areas ***'))
        Logger.add_to_log("critical", str(ex))
        Logger.add_to_log("critical", traceback.format_exc())
        datosDetalle = {}
        return (datosDetalle)


class cacheSvos():
    @classmethod
    def consulta_catalogos(cls, argNumVersion, ArgCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()

            cursor = db.cursor()
            # Obtiene la informacion del catalogo de Areas
            query = f'''SELECT id, cve_area, nombre, '' as id_asociado FROM area WHERE vigente = True order by cve_area;'''
            detalleAreas = catalogos_cache(cursor, query)

            # Obtiene la informacion del catalogo de Tipos de Documentos
            query = f'''SELECT id_tipo_docto, cve_tdocumento, nombre_corto, '' as id_asociado  FROM tipos_documento WHERE vigente = True  order by cve_tdocumento;'''
            detalleTDoctos = catalogos_cache(cursor, query)

            # Obtiene la informacion del catalogo de Procesos
            query = f'''SELECT id, cve_proceso, nombre, '' as id_asociado  FROM proceso WHERE vigente = True  order by cve_proceso;'''
            detalleProcesos = catalogos_cache(cursor, query)

            # Obtiene la informacion del catalogo de Documentos
            query = f'''select id_nombre_docto, '' as cve_docto, nombre, id_tdocto  from nombre_documento where vigente = true order by nombre;'''
            detalleDoctos = catalogos_cache(cursor, query)

            # Obtiene la informacion del catalogo de Documentos ordenado por Tipo de Documento
            detalleDoctosXtdoc = {}
            query = f'''select id_nombre_docto, id_tdocto, nombre from nombre_documento where vigente = true order by id_tdocto;'''
            detalleDoctos_x_tdocto = catalogos_cache(cursor, query)                
            doctosAgrupados = {}
            for tmp_TDocto, group in itertools.groupby(detalleDoctos_x_tdocto, key=lambda x: x["cve"]):
                doctosAgrupados[tmp_TDocto]= list(group)

            datos = {
                "areas" : detalleAreas,
                "tdoctos": detalleTDoctos,
                "procesos": detalleProcesos,
                "doctos": detalleDoctos,
            }

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = datos
            datosRespuesta['error'] = False
            ErrorSistema = False

            if connection:
                cursor.close()
                connection.close()

            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def cacheSvos.consulta_catalogos ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)

