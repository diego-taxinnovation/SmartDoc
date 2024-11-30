#*******************************************************************************************
#   PROCESO   
#   Definimos la clase Proceso con la informacion del modelo
#*******************************************************************************************
class Proceso():

    # Definimos los campos que tiene el modelo Proceso
    def __init__(self, id, cve_proceso, nombre, observaciones, vigente, id_usuario_alta, fecha_alta, id_usuario_actualiza=None, fecha_actualizacion=None) -> None:
        self.id = id
        self.cve_proceso = cve_proceso
        self.nombre = nombre
        self.observaciones = observaciones
        self.vigente = vigente
        self.id_usuario_alta = id_usuario_alta
        self.fecha_alta = fecha_alta
        self.id_usuario_actualiza = id_usuario_actualiza
        self.fecha_actualizacion = fecha_actualizacion

    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'id': self.id,
            'cve_proceso': self.cve_proceso,
            'nombre': self.nombre,
            'observaciones': self.observaciones,
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
        print('       Datos en la Clase Proceso')
        print('-' * 40)
        print('                       id: ', self.id)
        print('              cve_proceso: ', self.cve_proceso)
        print('                   nombre: ', self.nombre)
        print('            observaciones: ', self.observaciones)
        print('                  vigente: ', self.vigente)
        print('          ID Usuario alta: ', self.id_usuario_alta)
        print('          Fecha Hora alta: ', self.fecha_alta)
        print('     ID Usuario actualizo: ', self.id_usuario_actualiza)
        print(' Fecha Hora actualizacion: ', self.fecha_actualizacion)
        print('=' * 40)
        print('\n')

