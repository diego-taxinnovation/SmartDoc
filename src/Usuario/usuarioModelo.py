#*******************************************************************************************
#   USUARIO   
#   Definimos la clase Usuario con la informacion del modelo
#*******************************************************************************************
class Usuario():

    # Definimos los campos que tiene el modelo Usuario
    def __init__(self, id, email, fullname, password, vigente, id_empresa, cve_empresa, nom_empresa, id_perfil, cve_perfil, nom_perfil, usuario_alta, fecha_alta=None, usuario_actualiza=None, fecha_actualiza=None) -> None:
        self.id = id
        self.email = email
        self.fullname = fullname
        self.password = password
        self.vigente = vigente
        self.id_empresa = id_empresa
        self.cve_empresa = cve_empresa
        self.nom_empresa = nom_empresa
        self.id_perfil = id_perfil
        self.cve_perfil = cve_perfil
        self.nom_perfil = nom_perfil
        self.id_usuario_alta = usuario_alta
        self.fecha_alta = fecha_alta
        self.id_usuario_actualiza = usuario_actualiza
        self.fecha_actualizacion = fecha_actualiza

    # Metodo para retornar el objeto como un Diccionario (simulando un JSON)
    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'fullname': self.fullname,
            'password': self.password,
            'vigente': self.vigente,
            'id_empresa': self.id_empresa,
            'cve_empresa': self.cve_empresa,
            'nom_empresa': self.nom_empresa,
            'id_perfil': self.id_perfil,
            'cve_perfil': self.cve_perfil,
            'nom_perfil': self.nom_perfil,
            'id_usuario_alta': self.id_usuario_alta,
            'fecha_alta': self.fecha_alta,
            'id_usuario_actualiza': self.id_usuario_actualiza,
            'fecha_actualizacion': self.fecha_actualizacion
        }
    
    # Metodo para imprimir los valores de la Clase
    def to_print(self):
        print('\n')
        print('=' * 40)        
        print('       Datos en la Clase Usuario')
        print('-' * 40)
        print('                       id: ', self.id)
        print('                    email: ', self.email)
        print('                 fullname: ', self.fullname)
        print('                 password: ', self.password)
        print('                  vigente: ', self.vigente)
        print('               id_empresa: ', self.id_empresa)
        print('              cve_empresa: ', self.cve_empresa)
        print('              nom_empresa: ', self.nom_empresa)
        print('                id_perfil: ', self.id_perfil)
        print('               cve_perfil: ', self.cve_perfil)
        print('               nom_perfil: ', self.nom_perfil)
        print('          ID Usuario alta: ', self.id_usuario_alta)
        print('          Fecha Hora alta: ', self.fecha_alta)
        print('     ID Usuario actualizo: ', self.id_usuario_actualiza)
        print(' Fecha Hora actualizacion: ', self.fecha_actualizacion)
        print('=' * 40)
        print('\n')
