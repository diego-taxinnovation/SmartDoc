#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   SetUp. Del componente setupSvosBD.py importar la funcion para validad si el API es vigente
from src.Utilerias.setupSvosBD import setupSvos

#   Controlador. Del componente empProcesoControlador.py importar las funciones actualizaEmpresaPlantilla, altaEmpresaPlantilla, consultaEmpresaPlantilla, listaEmpresaPlantillas
from src.Emp_Plantillas.empPlantillaControlador import actualizaEmpresaPlantilla, altaEmpresaPlantilla, consultaEmpresaPlantilla, listaEmpresaPlantillas 

from datetime import datetime
from flask import Blueprint
import json

bp_empresa_plantilla = Blueprint('empresa_plantilla_blueprint', __name__)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_plantillas/v1/listaEmpPlantillas. Consulta los Plantillas de la Empresa en SmartDOC
#   =====================================================================================================
@bp_empresa_plantilla.route('/v0/listaEmpPlantillas', methods=['GET', 'POST'])
def listaEmpPlantillas_v0():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v0/listaEmpPlantillas'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 0
    respuesta = listaEmpresaPlantillas(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_plantillas/v1/listaEmpPlantillas. Consulta los Areas de la Empresa en SmartDOC
#   =====================================================================================================
@bp_empresa_plantilla.route('/v1/listaEmpPlantillas', methods=['GET', 'POST'])
def listaEmpPlantillas_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/listaEmpPlantillas'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = listaEmpresaPlantillas(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_plantillas/v1/altaEmpresaPlantilla. Alta de Plantilla en SmartDOC
#   =====================================================================================================
@bp_empresa_plantilla.route('/v1/altaEmpresaPlantilla', methods=['GET', 'POST'])
def altaEmpresaPlantilla_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/altaEmpresaPlantilla'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = altaEmpresaPlantilla(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_plantillas/v1/consultaEmpresaPlantilla. Consulta de Plantilla en SmartDOC
#   =====================================================================================================
@bp_empresa_plantilla.route('/v1/consultaEmpresaPlantilla', methods=['GET', 'POST'])
def consultaEmpresaPlantilla_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/consultaEmpresaPlantilla'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = consultaEmpresaPlantilla(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_plantillas/v1/actualizaEmpresaPlantilla. Actualizacion Plantilla en SmartDOC
#   =====================================================================================================
@bp_empresa_plantilla.route('/v1/actualizaEmpresaPlantilla', methods=['GET', 'POST'])
def actualizaEmpresaPlantilla_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/actualizaEmpresaPlantilla'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = actualizaEmpresaPlantilla(numVersion)
    return (respuesta, 200)

