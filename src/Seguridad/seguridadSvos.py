#   LIBRERIA. Permite leer variables de ambiente
from decouple import config

#   PAQUETE. Del paquete werkzeug.security importa los metodos generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback

#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Utilerias.utileriaModelo import Operador
from src.Usuario.usuarioModelo import Usuario


from datetime import datetime, timedelta

import jwt
import pytz
import pprint

class Seg_EncriptacionSvos():
    secret = config('JWT_KEY')

    @classmethod
    def encriptaDato(cls, dato):
        try:
            # Se encripta el valor de texto indicando que sea con el Algoritmo 'pbkdf2:sha256' y con 100 iteraciones
            datoEncriptado = generate_password_hash(dato, 'pbkdf2:sha256:30', 100 )
            return (False, datoEncriptado)
            
        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** class Seg_EncriptacionSvos.encriptaDato ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorClass = 'Servicio no disponible por el momento'
            return (True, msgErrorClass)
        
    @classmethod
    def desencriptaDato(cls, datoEncriptado, dato):
        try:
            # Este metodo nos permite traer un texto encriptado (datoEncriptado) y verificarlo contra el que se esta informando en claro (dayo) y confirmar si son iguales (Regresa: True o False)
            flagResultado = check_password_hash(datoEncriptado, dato)
            if (flagResultado):
                return (False, "Dato correcto")
            else:
                return (True, "Dato incorrecto")
            
        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** class Seg_EncriptacionSvos.desencriptaDato ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorClass = 'Servicio no disponible por el momento'
            return (True, msgErrorClass)

class Seg_TokenSvos():
    tz = pytz.timezone("America/Mexico_City")
    secret = config('JWT_KEY')
    
    @classmethod
    def genera_token(cls, _Usuario, argMinutos):       
        try:
            paylod = {
                'iat': datetime.now(tz=cls.tz),
                'exp': datetime.now(tz=cls.tz) + timedelta(minutes=argMinutos),
                'email': _Usuario.email,
                'id': _Usuario.id,
                'fullname': _Usuario.fullname,
                'id_empresa': _Usuario.id_empresa,
                'empresa': _Usuario.cve_empresa,
                'id_perfil': _Usuario.id_perfil,
                'perfil': _Usuario.cve_perfil
            }

            strToken = jwt.encode(paylod, cls.secret, algorithm='HS256')
            return (False, strToken)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** class TokenSvos.genera_token ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorClass = str(ex)
            return (True, msgErrorClass)

    @classmethod
    def verifica_token(cls, headers):
        try:
            # Valida que dentro del header este el de 'Authorization'
            if 'Authorization' in headers.keys():
                # Se obtiene el string que contiene el header 'Authorization'
                authorization = headers['Authorization']

                # Se obtiene el valor que este despues del primer espacio del valor en authorization (cadena token)
                encoded_token = authorization.split(" ")[1]

                # Valida que la longitud del token sea mayor a 0
                if (((len(encoded_token)) > 0) and (encoded_token != 'null')):
                    try:
                        # Creamos una instancia vacia de la clase Operador     
                        _operador = Operador(None, None, None, None)
                        # Obtiene un diccionario con la informacion que se encuentra en el Token
                        payload = jwt.decode(encoded_token, cls.secret, algorithms=['HS256'])
                            
                        # Se obtienen el ID del usuario asociado al Token
                        _operador.id = payload['id']
                        # Se obtienen el email del usuario asociado al Token
                        _operador.email = payload['email']
                        # Se obtienen la clave de empresa del usuario asociado al Token
                        _operador.cve_empresa = payload['empresa']
                        # Se obtienen el perfil asociado al usuario
                        _operador.cve_perfil = payload['perfil']
                        return (False, _operador)

                    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                        msgError = 'No se encuentra autorizado para ejecutar el servicio'
                        return (True, msgError)
            
            msgError = 'No se encuentra autorizado para ejecutar el servicio'
            return (True, msgError)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** class TokenSvos.verifica_token ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorClass = str(ex)
            return (True, msgErrorClass)

