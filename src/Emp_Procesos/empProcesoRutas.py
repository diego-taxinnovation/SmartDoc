#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   SetUp. Del componente setupSvosBD.py importar la funcion para validad si el API es vigente
from src.Utilerias.setupSvosBD import setupSvos

#   Controlador. Del componente empProcesoControlador.py importar las funciones ctualizaEmpresaProceso, altaEmpresaProceso, consultaEmpresaProceso, listaEmpresaProceso
from src.Emp_Procesos.empProcesoControlador import actualizaEmpresaProceso, altaEmpresaProceso, consultaEmpresaProceso, listaEmpresaProcesos 

from datetime import datetime
from flask import Blueprint
import json

bp_empresa_proceso = Blueprint('empresa_proceso_blueprint', __name__)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_procesos/v1/listaEmpProcesos. Consulta los Areas de la Empresa en SmartDOC
#   =====================================================================================================
@bp_empresa_proceso.route('/v0/listaEmpProcesos', methods=['GET', 'POST'])
def listaEmpProcesos_v0():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v0/listaEmpProcesos'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 0
    respuesta = listaEmpresaProcesos(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_procesos/v1/listaEmpProcesos. Consulta los Areas de la Empresa en SmartDOC
#   =====================================================================================================
@bp_empresa_proceso.route('/v1/listaEmpProcesos', methods=['GET', 'POST'])
def listaEmpProcesos_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/listaEmpProcesos'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = listaEmpresaProcesos(numVersion)
    return (respuesta, 200)



#   =====================================================================================================
#   EndPoint /smartdoc/emp_procesos/v1/altaEmpresaProceso. Alta de Areas en SmartDOC
#   =====================================================================================================
@bp_empresa_proceso.route('/v1/altaEmpresaProceso', methods=['GET', 'POST'])
def altaEmpresaProceso_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/altaEmpresaProceso'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = altaEmpresaProceso(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_procesos/v1/consultaEmpresaProceso. Consulta de Area en SmartDOC
#   =====================================================================================================
@bp_empresa_proceso.route('/v1/consultaEmpresaProceso', methods=['GET', 'POST'])
def consultaEmpresaProceso_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/consultaEmpresaProceso'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = consultaEmpresaProceso(numVersion)
    return (respuesta, 200)

#   =====================================================================================================
#   EndPoint /smartdoc/emp_procesos/v1/actualizaEmpresaProceso. Actualizacion Area en SmartDOC
#   =====================================================================================================
@bp_empresa_proceso.route('/v1/actualizaEmpresaProceso', methods=['GET', 'POST'])
def actualizaEmpresaProceso_v1():
    # Llama a la funcion para validar si el EndPoint es Vigente u Obsoleto
    uri_api = '/v1/actualizaEmpresaProceso'
    apiObsoleto = setupSvos.valida_soporteAPI(uri_api)
    if (apiObsoleto[0]):
        resp = {
                'error': True, 
                'mensaje': apiObsoleto[1]
            }
        return (resp, 200)

    numVersion = 1
    respuesta = actualizaEmpresaProceso(numVersion)
    return (respuesta, 200)
