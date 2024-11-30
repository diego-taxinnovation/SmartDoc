#*******************************************************************************************
#   TIPOS DE DOCUMENTO
#   Definimos la clase Tipos de Documento con la informacion del modelo
#*******************************************************************************************
class TiposDocumentos():

    # Definimos los campos que tiene el modelo Tipos de Documento
    def __init__(self, id_tipo_docto, cve_tdocumento, nombre_corto, nombre_largo, vigente, observaciones, id_usuario_alta, fecha_alta, id_usuario_actualiza=None, fecha_actualizacion=None) -> None:
        self.id = id_tipo_docto
        self.cve_tdocumento = cve_tdocumento
        self.nombre_corto = nombre_corto
        self.nombre_largo = nombre_largo
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
            'cve_tdocumento': self.cve_tdocumento,
            'nombre_corto': self.nombre_corto,
            'nombre_largo': self.nombre_largo,
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
        print('       Datos en la Clase Tipos de Documento')
        print('-' * 40)
        print('            id_tipo_docto: ', self.id)
        print('           cve_tdocumento: ', self.cve_tdocumento)
        print('             nombre_corto: ', self.nombre_corto)
        print('             nombre_largo: ', self.nombre_largo)
        print('                  vigente: ', self.vigente)
        print('            observaciones: ', self.observaciones)
        print('          ID Usuario alta: ', self.id_usuario_alta)
        print('          Fecha Hora alta: ', self.fecha_alta)
        print('     ID Usuario actualizo: ', self.id_usuario_actualiza)
        print(' Fecha Hora actualizacion: ', self.fecha_actualizacion)
        print('=' * 40)
        print('\n')


