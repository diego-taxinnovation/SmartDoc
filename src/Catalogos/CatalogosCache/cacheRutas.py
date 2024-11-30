#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   SetUp. Del componente setupSvosBD.py importar la funcion para validad si el API es vigente
from src.Utilerias.setupSvosBD import setupSvos

#   Controlador. Del componente cacheControlador.py.py importar las funciones listaCache
from src.Catalogos.CatalogosCache.cacheControlador import listaCache

from datetime import datetime
from flask import Blueprint
import json

bp_cache = Blueprint('cache_blueprint', __name__)

#   =====================================================================================================
#   EndPoint /smartdoc/cache/v0/listaCache. Consulta los Catalogos Comunes en SmartDOC v0
#   =====================================================================================================
@bp_cache.route('/v0/listaCache', methods=['GET', 'POST'])
def listaCache_v0():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v0/listaCache'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 0
    respuesta = listaCache(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/cache/v1/listaCache. Consulta los Catalogos Comunes en SmartDOC v1
#   =====================================================================================================
@bp_cache.route('/v1/listaCache', methods=['GET', 'POST'])
def listaCache_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/listaCache'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = listaCache(numVersion)
    return (respuesta, 200)
