#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   SetUp. Del componente setupSvosBD.py importar la funcion para validad si el API es vigente
from src.Utilerias.setupSvosBD import setupSvos

#   Controlador. Del componente empAreaControlador.py.py importar las funciones actualizaArea, altaArea, consultaArea, listaAreas
from src.Emp_Areas.empAreaControlador import actualizaEmpresaArea, altaEmpresaArea, consultaEmpresaArea, listaEmpresaAreas

from datetime import datetime
from flask import Blueprint
import json

bp_empresa_area = Blueprint('empresa_area_blueprint', __name__)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_areas/v1/listaEmpAreas. Consulta los Areas de la Empresa en SmartDOC
#   =====================================================================================================
@bp_empresa_area.route('/v1/listaEmpAreas', methods=['GET', 'POST'])
def listaEmpAreas_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/listaEmpAreas'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = listaEmpresaAreas(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_areas/v1/altaEmpresaArea. Alta de Areas en SmartDOC
#   =====================================================================================================
@bp_empresa_area.route('/v1/altaEmpresaArea', methods=['GET', 'POST'])
def altaEmpresaArea_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/altaEmpresaArea'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = altaEmpresaArea(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_areas/v1/consultaEmpresaArea. Consulta de Area en SmartDOC
#   =====================================================================================================
@bp_empresa_area.route('/v1/consultaEmpresaArea', methods=['GET', 'POST'])
def consultaEmpresaArea_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/consultaEmpresaArea'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = consultaEmpresaArea(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_areas/v1/actualizaEmpresaArea. Actualizacion Area en SmartDOC
#   =====================================================================================================
@bp_empresa_area.route('/v1/actualizaEmpresaArea', methods=['GET', 'POST'])
def actualizaEmpresaArea_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/actualizaEmpresaArea'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = actualizaEmpresaArea(numVersion)
    return (respuesta, 200)

