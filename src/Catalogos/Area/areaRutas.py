#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   SetUp. Del componente setupSvosBD.py importar la funcion para validad si el API es vigente
from src.Utilerias.setupSvosBD import setupSvos

#   Controlador. Del componente areaControlador.py.py importar las funciones actualizaArea, altaArea, consultaArea, listaAreas
from src.Catalogos.Area.areaControlador import actualizaArea, altaArea, consultaArea, listaAreas

from datetime import datetime
from flask import Blueprint
import json

bp_area = Blueprint('area_blueprint', __name__)

#   =====================================================================================================
#   EndPoint /smartdoc/area/v1/prueba. EndPoint para pruebas
#   =====================================================================================================
@bp_area.route('/v1/prueba', methods=['GET', 'POST'])
def prueba_v1():
    numVersion = 1
    uri_api = '/v1/prueba'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    resp = {
            'error': True, 
            'mensaje': apiObsoleto[1]
        }
    
    return (resp, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/area/v1/listaAreas. Consulta los Areas en SmartDOC
#   =====================================================================================================
@bp_area.route('/v1/listaAreas', methods=['GET', 'POST'])
def listaAreas_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/listaAreas'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = listaAreas(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/area/v1/altaArea. Alta de Areas en SmartDOC
#   =====================================================================================================
@bp_area.route('/v1/altaArea', methods=['GET', 'POST'])
def altaArea_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/altaArea'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = altaArea(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/area/v1/consultaArea. Consulta de Area en SmartDOC
#   =====================================================================================================
@bp_area.route('/v1/consultaArea', methods=['GET', 'POST'])
def consultaArea_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/consultaArea'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = consultaArea(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/area/v1/actualizaArea. Actualizacion Area en SmartDOC
#   =====================================================================================================
@bp_area.route('/v1/actualizaArea', methods=['GET', 'POST'])
def actualizaArea_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/actualizaArea'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = actualizaArea(numVersion)
    return (respuesta, 200)
