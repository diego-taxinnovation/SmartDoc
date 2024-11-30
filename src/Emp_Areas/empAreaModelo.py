#*******************************************************************************************
#   EMPRESA AREAS   
#   Definimos la clase Empresa_Areas con la informacion del modelo
#*******************************************************************************************
class Empresa_Areas():

    # Definimos los campos que tiene el modelo emp_areas
    def __init__(self, id, id_empresa, id_area, cve_area, nombre_area, id_usuario_alta, fecha_alta, id_usuario_actualiza=None, fecha_actualizacion=None) -> None:
        self.id = id
        self.id_empresa = id_empresa
        self.id_area = id_area
        self.cve_area = cve_area
        self.nombre_area = nombre_area
        self.id_usuario_alta = id_usuario_alta
        self.fecha_alta = fecha_alta
        self.id_usuario_actualiza = id_usuario_actualiza
        self.fecha_actualizacion = fecha_actualizacion


    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'id': self.id,
            'id_empresa': self.id_empresa,
            'id_area': self.id_area,
            'cve_area': self.cve_area,
            'nombre_area': self.nombre_area,
            'id_usuario_alta': self.id_usuario_alta,
            'fecha_alta': self.fecha_alta,
            'id_usuario_actualiza': self.id_usuario_actualiza,
            'fecha_actualizacion': self.fecha_actualizacion
        }
    
    # Metodo para imprimir los valores de la Clase
    def to_print(self):
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Empresa Area')
        print('-' * 40)
        print('                       id: ', self.id)
        print('               id_empresa: ', self.id_empresa)
        print('                  id_area: ', self.id_area)
        print('                 cve_area: ', self.cve_area)
        print('              nombre_area: ', self.nombre_area)
        print('          ID Usuario alta: ', self.id_usuario_alta)
        print('          Fecha Hora alta: ', self.fecha_alta)
        print('     ID Usuario actualizo: ', self.id_usuario_actualiza)
        print(' Fecha Hora actualizacion: ', self.fecha_actualizacion)
        print('=' * 40)
        print('\n')

