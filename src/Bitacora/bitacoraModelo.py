#*******************************************************************************************
#   BITACORA   
#   Definimos la clase bitacora con la informacion del modelo
#*******************************************************************************************
class Bitacora():
    # Definimos los campos que tiene la clase Bitacora
    def __init__(self, id, cve_empresa, cve_aplicacion, cve_usuario, cve_operacion, entrada) -> None:
        self.id = id
        self.cve_empresa = cve_empresa
        self.cve_aplicacion = cve_aplicacion
        self.cve_usuario = cve_usuario
        self.cve_operacion = cve_operacion
        self.estado = True
        self.entrada = entrada
        self.salida = "Consulta realizada"        
        self.modulo = ""
        self.pantalla = ""
        self.err_sistema = False
        self.latitud = ""
        self.longitud = ""
        self.ip_cliente = ""
        self.realizado = ""

    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'id': self.id,
            'cve_empresa': self.cve_empresa,
            'cve_aplicacion': self.cve_aplicacion,
            'cve_usuario': self.cve_usuario,
            'cve_operacion': self.cve_operacion,
            'estado': self.estado,
            'entrada': self.entrada,
            'salida': self.salida,
            'modulo': self.modulo,
            'pantalla': self.pantalla,
            'err_sistema': self.err_sistema,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'ip_cliente': self.ip_cliente,
            'realizado': self.realizado
        }

    # Metodo para imprimir los valores de la Clase
    def to_print(self):
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Bitacora')
        print('-' * 40)
        print('            id: ', self.id)
        print('   cve_empresa: ', self.cve_empresa)
        print('cve_aplicacion: ', self.cve_aplicacion)
        print('   cve_usuario: ', self.cve_usuario)
        print(' cve_operacion: ', self.cve_operacion)
        print('        estado: ', self.estado)
        print('       entrada: ', self.entrada)
        print('        salida: ', self.salida)
        print('        modulo: ', self.modulo)
        print('      pantalla: ', self.pantalla)
        print('   err_sistema: ', self.err_sistema)
        print('       latitud: ', self.latitud)
        print('      longitud: ', self.longitud)
        print('    ip_cliente: ', self.ip_cliente)
        print('     realizado: ', self.realizado)
        print('=' * 40)
        print('\n')
