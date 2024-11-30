#*******************************************************************************************
#   Operador   
#   Definimos la clase Operador con la informacion del modelo
#*******************************************************************************************
class Operador():

    # Definimos los campos que tiene el modelo Operador
    def __init__(self, id, email, cve_empresa, cve_perfil) -> None:
        self.id = id
        self.email = email
        self.cve_empresa = cve_empresa
        self.cve_perfil = cve_perfil


    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'cve_empresa': self.cve_empresa,
            'Cve_perfil': self.cve_perfil
        }
    
    # Metodo para imprimir los valores de la Clase
    def to_print(self):
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Operador')
        print('-' * 40)
        print('          id: ', self.id)
        print('       email: ', self.email)
        print(' cve_empresa: ', self.cve_empresa)
        print('  cve_perfil: ', self.cve_perfil)
        print('=' * 40)
        print('\n')


