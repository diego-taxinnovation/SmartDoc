#*******************************************************************************************
#   AREAS
#   Definimos la clase Area con la informacion del modelo
#*******************************************************************************************
class Area():

    # Definimos los campos que tiene el modelo Area
    def __init__(self, id, cve_area, nombre, vigente, observaciones, id_usuario_alta, fecha_alta, id_usuario_actualiza=None, fecha_actualizacion=None) -> None:
        self.id = id
        self.cve_area = cve_area
        self.nombre = nombre
        self.vigente = vigente
        self.observaciones = observaciones
        self.id_usuario_alta = id_usuario_alta
        self.fecha_alta = fecha_alta
        self.id_usuario_actualiza = id_usuario_actualiza
        self.fecha_actualizacion = fecha_actualizacion

    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'id': self.id,
            'cve_area': self.cve_area,
            'nombre': self.nombre,
            'vigente': self.vigente,
            'observaciones': self.observaciones,
            'id_usuario_alta': self.id_usuario_alta,
            'fecha_alta': self.fecha_alta,
            'id_usuario_actualiza': self.id_usuario_actualiza,
            'fecha_actualizacion': self.fecha_actualizacion
        }
    
    # Metodo para imprimir los valores de la Clase
    def to_print(self):
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Area')
        print('-' * 40)
        print('                       id: ', self.id)
        print('                 cve_area: ', self.cve_area)
        print('                   nombre: ', self.nombre)
        print('                  vigente: ', self.vigente)
        print('            observaciones: ', self.observaciones)
        print('          ID Usuario alta: ', self.id_usuario_alta)
        print('          Fecha Hora alta: ', self.fecha_alta)
        print('     ID Usuario actualizo: ', self.id_usuario_actualiza)
        print(' Fecha Hora actualizacion: ', self.fecha_actualizacion)
        print('=' * 40)
        print('\n')

