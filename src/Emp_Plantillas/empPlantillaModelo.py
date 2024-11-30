#*******************************************************************************************
#   EMPRESA PLANTILLAS   
#   Definimos la clase Empresa_PlantillaDocto con la informacion del modelo
#*******************************************************************************************
class Empresa_PlantillaDocto():
    # Definimos los campos que tiene el modelo emp_plantilla
    def __init__(self, id, id_emp_proceso, id_tdocto, nom_tdocto, id_docto, nom_docto, observaciones, vigente, obligatorio, vigencia, id_usuario_alta, fecha_alta, id_usuario_actualiza=None, fecha_actualizacion=None) -> None:
        self.id = id
        self.id_emp_proceso = id_emp_proceso
        self.id_tdocto = id_tdocto
        self.nom_tdocto = nom_tdocto
        self.id_docto = id_docto
        self.nom_docto = nom_docto
        self.observaciones = observaciones
        self.vigente = vigente
        self.obligatorio = obligatorio
        self.vigencia = vigencia
        self.id_usuario_alta = id_usuario_alta
        self.fecha_alta = fecha_alta
        self.id_usuario_actualiza = id_usuario_actualiza
        self.fecha_actualizacion = fecha_actualizacion

    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'id': self.id,
            'id_emp_proceso': self.id_emp_proceso,
            'id_tdocto': self.id_tdocto,
            'nom_tdocto': self.nom_tdocto,
            'id_docto': self.id_docto,
            'nom_tdocto': self.nom_tdocto,
            'observaciones': self.observaciones,
            'vigente': self.vigente,
            'obligatorio': self.obligatorio,
            'vigencia': self.vigencia,
            'id_usuario_alta': self.id_usuario_alta,
            'fecha_alta': self.fecha_alta,
            'id_usuario_actualiza': self.id_usuario_actualiza,
            'fecha_actualizacion': self.fecha_actualizacion
        }
    
    # Metodo para imprimir los valores de la Clase
    def to_print(self):
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Empresa Plantilla - Docto')
        print('-' * 40)
        print('                       id: ', self.id)
        print('           id_emp_proceso: ', self.id_emp_proceso)
        print('                id_tdocto: ', self.id_tdocto)
        print('               nom_tdocto: ', self.nom_tdocto)
        print('                 id_docto: ', self.id_docto)
        print('               nom_tdocto: ', self.nom_tdocto)
        print('            observaciones: ', self.observaciones)
        print('                  vigente: ', self.vigente)
        print('              obligatorio: ', self.obligatorio)
        print('                 vigencia: ', self.vigencia)
        print('          ID Usuario alta: ', self.id_usuario_alta)
        print('          Fecha Hora alta: ', self.fecha_alta)
        print('     ID Usuario actualizo: ', self.id_usuario_actualiza)
        print(' Fecha Hora actualizacion: ', self.fecha_actualizacion)
        print('=' * 40)
        print('\n')
