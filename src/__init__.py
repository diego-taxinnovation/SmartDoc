from flask import Flask
from flask_cors import CORS, cross_origin

# SetUp
from src.Utilerias.setupSvosBD import setupSvos

# Routes
from src.Bitacora import bitacoraRutas
from src.Empresa import empresaRutas
from src.Emp_Areas import empAreaRutas
from src.Emp_Plantillas import empPlantillaRutas
from src.Emp_Procesos import empProcesoRutas
from src.Procesos import procesoRutas
from src.Seguridad import seguridadRutas
from src.Catalogos.CatalogosCache import cacheRutas
from src.Catalogos.Nombre_Documento import nombreDoctoRutas
from src.Catalogos.Tipos_Documento import tiposDoctoRutas
from src.Catalogos.Area import areaRutas
from src.Usuario import usuarioRutas
from src.Documento import documentoRutas

app = Flask(__name__)

# https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
# This will enable CORS for all routes
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(areaRutas.bp_area, url_prefix='/smartdoc/area')
    app.register_blueprint(bitacoraRutas.bp_bitacora, url_prefix='/smartdoc/bitacora')
    app.register_blueprint(cacheRutas.bp_cache, url_prefix='/smartdoc/cache')
    app.register_blueprint(empresaRutas.bp_empresas, url_prefix='/smartdoc/empresa')
    app.register_blueprint(empAreaRutas.bp_empresa_area, url_prefix='/smartdoc/emp_areas')
    app.register_blueprint(empPlantillaRutas.bp_empresa_plantilla, url_prefix='/smartdoc/emp_plantillas')
    app.register_blueprint(empProcesoRutas.bp_empresa_proceso, url_prefix='/smartdoc/emp_procesos')
    app.register_blueprint(nombreDoctoRutas.bp_ndocto, url_prefix='/smartdoc/ndocto')
    app.register_blueprint(procesoRutas.bp_proceso, url_prefix='/smartdoc/proceso')
    app.register_blueprint(seguridadRutas.bp_seguridad, url_prefix='/smartdoc/seguridad')
    app.register_blueprint(tiposDoctoRutas.bp_tdocto, url_prefix='/smartdoc/tdocto')
    app.register_blueprint(usuarioRutas.bp_usuarios, url_prefix='/smartdoc/usuario')
    app.register_blueprint(documentoRutas.bp_documentos, url_prefix='/smartdoc/documento')

    # Llama funcion para obtener API obsoletas (Sin Soporte)
    glb_endPoints = setupSvos.lista_endpointBAJA(app.config)
    # Graba el arreglo con las API obsoletas (Sin Soporte) en la variable 'endPoint_baja', de la configuracion de App
    app.config['endPoint_baja'] = glb_endPoints

    return app
  