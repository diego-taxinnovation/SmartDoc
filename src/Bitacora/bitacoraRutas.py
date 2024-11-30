#   LIBRERIA. Microframework basado en Werkzeug para crear aplicaciones WEB
from flask import Blueprint, jsonify, request

#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs import Logger

#   MODELOS. Obtenemos de los componentes que estan en el directorio Modelos las clases a utilizar
from src.Bitacora.bitacoraModelo import Bitacora

#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Bitacora.bitacoraSvosBD import BitacoraSvos

#   Servicios. Del componente BitacoraServicios.py importa la clase BitacoraSvos
from src.Seguridad.seguridadSvos import Seg_TokenSvos


from datetime import datetime
from flask import request, current_app, jsonify
import json
import re
from flask_cors import CORS

#   LIBRERIA. Es una liberia que ofrece imprimir valores ordenadamente
from pprint import pprint

bp_bitacora = Blueprint('bitacora_blueprint', __name__)

@bp_bitacora.route('consultaID', methods=['GET'])
def consulta_ID():
    try:
        # Se valida que las claves y valores requeridos vengan en el JSON
        key = 'email_PARA'
        if not(key in request.json):
            return jsonify({'message': "ERROR EN LA ESTRUCTURA JSON", 'success': False})

        key = 'mensaje'
        if not(key in request.json):
            return jsonify({'message': "ERROR EN LA ESTRUCTURA JSON", 'success': False})

        key = 'asunto'
        if not(key in request.json):
            return jsonify({'message': "ERROR EN LA ESTRUCTURA JSON", 'success': False})

        email_FROM = request.json['email_DE']
        email_TO = request.json['email_PARA']
        msg = request.json['mensaje']
        subject = request.json['asunto']

        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        # Se valida que el campo email_TO tenga estructura de una direccion de correo valida
        if ((re.match(expresion_regular, email_TO)) == None):
            return jsonify({'message': "ERROR EN EL FORMATO DE CORREO (PARA)", 'success': False})

        # Se valida que la longitud del mensage NO exceda los 2056 caracteres o sea vacio
        if ((len(msg) == 0) or (len(msg) > 2056)):
            return jsonify({'message': "ERROR EN DATOS (Cuerpo del mensaje)", 'success': False})

        # Se valida que asunto no venga vacio
        if (len(subject) == 0):
            subject = '...'

        # Llama al servicio de seguridad para verificar Token
        has_access = Seg_TokenSvos.verifica_token(request.headers)

        # ******************************************************************
        # Lineas (activas) para No realizar validacion de Token
        # ******************************************************************
        MicroSvos_SinJWT=True    
        if (MicroSvos_SinJWT):
        # ******************************************************************
        #if (has_access):
            try:
                # Llama al servicio envio()
                envioCORREO = gmailService.envio(subject, email_FROM, email_TO, msg)
                # Verifica si la respuesta trae informacion
                if (envioCORREO):
                    return jsonify({'message': "SUCCESS", 'success': True})
                else:
                    return jsonify({'message': "NO SE LOGRO ENVIAR EL CORREO", 'success': True})
                
            except Exception as ex:
                Logger.add_to_log("error", str(ex))
                Logger.add_to_log("error", traceback.format_exc())

                return jsonify({'message': "ERROR. Servicio intermitente", 'success': False})
        else:    
            # Token invalido, no se autoriza servicio
            response = jsonify({'message': "Unauthorizes", 'success': False})
            return (response, 401)

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())

        return jsonify({'message': "ERROR. Servicio intermitente", 'success': False})
