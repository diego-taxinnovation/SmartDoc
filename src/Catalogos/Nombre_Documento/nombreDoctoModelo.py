#*******************************************************************************************
#   NOMBRE DE DOCUMENTO
#   Definimos la clase Nombre de Documento con la informacion del modelo
#*******************************************************************************************
class NombreDocumento():

    # Definimos los campos que tiene el modelo Nombre de Documento
    def __init__(self, id, nombre, observaciones, vigente, id_tdocto, cve_tdocto, nombre_corto, id_usuario_alta, fecha_alta, id_usuario_actualiza=None, fecha_actualizacion=None) -> None:
        self.id = id
        self.nombre = nombre
        self.observaciones = observaciones
        self.vigente = vigente
        self.id_tdocto = id_tdocto
        self.cve_tdocto = cve_tdocto
        self.nombre_corto = nombre_corto
        self.id_usuario_alta = id_usuario_alta
        self.fecha_alta = fecha_alta
        self.id_usuario_actualiza = id_usuario_actualiza
        self.fecha_actualizacion = fecha_actualizacion

    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'observaciones': self.observaciones,
            'vigente': self.vigente,
            'id_tdocto': self.id_tdocto,
            'cve_tdocto': self.cve_tdocto,
            'nombre_corto': self.nombre_corto,
            'id_usuario_alta': self.id_usuario_alta,
            'fecha_alta': self.fecha_alta,
            'id_usuario_actualiza': self.id_usuario_actualiza,
            'fecha_actualizacion': self.fecha_actualizacion
        }
    
    # Metodo para imprimir los valores de la Clase
    def to_print(self):
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Nombre de Documento')
        print('-' * 40)
        print('                       id: ', self.id)
        print('                   nombre: ', self.nombre)
        print('            observaciones: ', self.observaciones)
        print('                  vigente: ', self.vigente)
        print('                id_tdocto: ', self.id_tdocto)
        print('               cve_tdocto: ', self.cve_tdocto)
        print('             nombre_corto: ', self.nombre_corto)
        print('          ID Usuario alta: ', self.id_usuario_alta)
        print('          Fecha Hora alta: ', self.fecha_alta)
        print('     ID Usuario actualizo: ', self.id_usuario_actualiza)
        print(' Fecha Hora actualizacion: ', self.fecha_actualizacion)
        print('=' * 40)
        print('\n')
