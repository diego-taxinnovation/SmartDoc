#*******************************************************************************************
#   EMPRESA   
#   Definimos la clase Empresa con la informacion del modelo
#*******************************************************************************************
class Empresa():

    # Definimos los campos que tiene el modelo Empresa
    def __init__(self, id, cve_empresa, nombre, observaciones, uso_webhook, vigente, id_usuario_alta, fecha_alta, id_usuario_actualiza=None, fecha_actualizacion=None) -> None:
        self.id = id
        self.cve_empresa = cve_empresa
        self.nombre = nombre
        self.observaciones = observaciones
        self.uso_webhook = uso_webhook
        self.vigente = vigente
        self.id_usuario_alta = id_usuario_alta
        self.fecha_alta = fecha_alta
        self.id_usuario_actualiza = id_usuario_actualiza
        self.fecha_actualizacion = fecha_actualizacion

    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'id': self.id,
            'cve_empresa': self.cve_empresa,
            'nombre': self.nombre,
            'observaciones': self.observaciones,
            'uso_webhook': self.uso_webhook,
            'vigente': self.vigente,
            'id_usuario_alta': self.id_usuario_alta,
            'fecha_alta': self.fecha_alta,
            'id_usuario_actualiza': self.id_usuario_actualiza,
            'fecha_actualizacion': self.fecha_actualizacion
        }
    
    # Metodo para imprimir los valores de la Clase
    def to_print(self):
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Empresa')
        print('-' * 40)
        print('                       id: ', self.id)
        print('              cve_empresa: ', self.cve_empresa)
        print('                   nombre: ', self.nombre)
        print('            observaciones: ', self.observaciones)
        print('               usoWebhook: ', self.uso_webhook)
        print('                  vigente: ', self.vigente)
        print('          ID Usuario alta: ', self.id_usuario_alta)
        print('          Fecha Hora alta: ', self.fecha_alta)
        print('     ID Usuario actualizo: ', self.id_usuario_actualiza)
        print(' Fecha Hora actualizacion: ', self.fecha_actualizacion)
        print('=' * 40)
        print('\n')

