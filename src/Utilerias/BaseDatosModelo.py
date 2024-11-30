#*******************************************************************************************
#   BASE DE DATOS   
#   Definimos la clase BaseDatos con la informacion del modelo
#*******************************************************************************************
import psycopg2
from redis import Redis
from redis.commands.search.query import Query
#from rejson import Client, Path

class PostgresBase():

    def __init__(self, argCurrent_app) -> None:
        # Al usar _ decimos que esta variable no deberia usarse fuera de exta clase
        self._conexion = psycopg2.connect(
            host = argCurrent_app.config['SUPABASE_HOST'],
            port = argCurrent_app.config['SUPABASE_PORT'],
            database = argCurrent_app.config['SUPABASE_DATABASE'],
            user = argCurrent_app.config['SUPABASE_USER'],
            password = argCurrent_app.config['SUPABASE_PASSWORD']
        )
        self._cursor = self._conexion.cursor()


    # Definimos un metodo getter para regresar '_conexion' sin acceder a la variable
    @property
    def conexion(self):
        return self._conexion
    

    # Definimos un metodo getter para regresar '_conexion' sin acceder a la variable
    @property
    def cursor(self):
        return self._cursor
    

    def commit(self):
        if self._conexion:
            self._conexion.commit()
        else:
            raise Exception("No se ha establecido una conexión con la base de datos.")


    def close(self):
        if self._conexion:
            self._conexion.close()
            self._cursor.close()
        else:
            raise Exception("No se ha establecido una conexión con la base de datos.")


    def execute(self, query, datos = None):
        if self._cursor:
            try:
                self._cursor.execute(query, (datos) or ())
            except Exception as ex:
                raise Exception(str(ex))
        else:
            raise Exception("No se ha establecido un cursor.")


    def fetchall(self):
        return self._cursor.fetchall()


    def fetchone(self):
        return self._cursor.fetchone()
    

class RedisBase():
    def __init__(self, arg_current_app) -> None:
        self._conexion = Redis(host=arg_current_app['REDIS_HOST'],
            port=arg_current_app['REDIS_PORT'],
            #password=arg_current_app['REDIS_PASSWORD']
        ) 


    @property
    def conexion(self):
        return self._conexion
  

    def cargar_json(self, nombre, json_doc) -> None:
        #self._conexion.json().set('doc:{}'.format(nombre), Path.rootPath(), json_doc)
        self._conexion.json().set('doc:{}'.format(nombre), '$', json_doc)


    def consultar(self):
        redis_search = self._conexion.ft('docIdx')
        resultado = redis_search.search(
            Query('Diego')
        )
        return resultado.docs
