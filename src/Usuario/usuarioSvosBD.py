#   LIBRERIA. Extract, format and print stack traces of Python programs
import traceback
#   LOG-TRACE. Del componente logger.py importa el metodo Logger (graba el LOG del stach trace del llamado)
from src.Utilerias.logs  import Logger

#   MODELOS. Del componente usuarioModelo.py importa la clase Usuario
from src.Usuario.usuarioModelo import Usuario

#   SERVICIOS. Del componente seguridadSvos.py importa la clase Seg_EncriptacionSvos
from src.Seguridad.seguridadSvos import Seg_EncriptacionSvos, Seg_TokenSvos

#   UTILERIAS. Del componente baseDatos.py importa la funcion conexionBD
from src.Utilerias.BaseDatosModelo import PostgresBase

from datetime import datetime


class UsuarioSvos():
    @classmethod
    def alta_usuario(cls, user, ArgCurrentApp):
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()

            # Llama al metodo encriptaDato de la clase Seg_EncriptacionSvos para encriptar el password del usuario
            tuplaEncriptado = Seg_EncriptacionSvos.encriptaDato(user.password)
            if (tuplaEncriptado[0]):                        # Error en la encriptacion
                return (True, 'Error al encriptar password')
            else:                                           # Encriptacion correcta
                passwordEncriptado = tuplaEncriptado[1]

            query = 'INSERT INTO usuario '
            query += f''' (email, fullname, password, id_perfil, cve_empresa, vigente, id_usuario_alta)
                           VALUES
                          (%s, %s, %s, %s, %s, %s, %s) RETURNING id;; 
                      '''
            datos = (user.email, user.fullname, passwordEncriptado, user.id_perfil, user.empresa, user.vigente, user.id_usuario_alta)
            cursor.execute(query, (datos))

            # Obtiene el ID generado en la BBDD
            count = cursor.rowcount
            ID_usuario = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
            connection.close()

            if (ID_usuario > 0):
                return (False, ID_usuario)
            else:
                return (True, "Error al intentar dar de alta el usuario")
            
        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def UsuarioSvos.alta_usuario ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            return (True, msgErrorDef)


    @classmethod
    def valida_usuario(cls, _version, ArgCurrentApp, user, validaPass=True, vigencia=60):    # Vigencia del Token (vigencia) es opcional, su default es 60 minutos
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            #cursor.execute(''' select * from usuario where email = %s ''', [user.email]) 

            cursor.execute(''' SELECT u.id, u.email, u.fullname, u."password", u.vigente,  
                                      u.id_empresa, e.cve_empresa, e.nombre, u.id_perfil, p.cve_perfil, p.descripcion,  
                                      u.id_usuario_alta,  to_char(u.fecha_alta, 'DD/MM/YYYY HH:MM:SS'), u.id_usuario_actualiza, 
                                      to_char(u.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS') 
                                FROM usuario u, empresa e, perfil p 
                                WHERE u.id_empresa = e.id and u.id_perfil = p.id AND email = %s ''', [user.email]);

            regto = cursor.fetchall()
            cursor.close()
            connection.close()
            # Validamos si la respuesta trae elementos o esta vacia
            if (regto):
                # Guarda en el password (claro) en la variable claveClaro
                claveClaro = user.password
                # Guarda en la variable usuario el primer registro recuperado de la consulta
                resID = regto[0][0]
                # Obtiene el campo con el nombre del usuario
                resNombre = regto[0][2]
                # Obtiene el password encriptado del registro del usuario recuperado
                resPassword = regto[0][3]
                # Obtiene si esta vigente el registro del usuario recuperado
                resVigente = regto[0][4]
                # Obtiene el id de la empresa asociada al usuario
                resIdEmpresa = regto[0][5]
                # Obtiene la clave de la empresa asociada al usuario
                resCveEmpresa = regto[0][6]
                # Obtiene nombre de la empresa asociada al usuario
                resEmpresa = regto[0][7]
                # Obtiene el campo que identifica el id del Perfil asignado
                resIdPerfil = regto[0][8]
                # Obtiene el campo que identifica la clave del Perfil asignado
                resCvePerfil = regto[0][9]
                # Obtiene el campo que identifica la descripcion del Perfil asignado
                resPerfil = regto[0][10]
                # Obtiene el campo que identifica ID del usuario que dio de alta el registro
                resIDAlta = regto[0][11]
                # Obtiene el campo que identifica Fecha y Hora que se dio de alta el registro
                resTSalta = regto[0][12]
                # Obtiene el campo que identifica ID del usuario que realizo la ultima actualizacion el registro
                resIDActualizo = regto[0][13]
                # Obtiene el campo que identifica Fecha y Hora cuando se realizo la ultima actualizacion el registro
                resTSactualizo = regto[0][14]

                user.id = resID
                user.fullname = resNombre
                user.password = resPassword
                user.vigente = resVigente
                user.id_empresa = resIdEmpresa
                user.cve_empresa = resCveEmpresa
                user.nom_empresa = resEmpresa
                user.id_perfil = resIdPerfil
                user.cve_perfil = resCvePerfil
                user.nom_perfil = resPerfil
                user.id_usuario_alta = resIDAlta
                user.fecha_alta = resTSalta
                user.id_usuario_actualiza = resIDActualizo
                user.fecha_actualizacion = resTSactualizo


                if (user.vigente):                  # El usuario esta vigente
                    # Se valida si la peticion solicita la validacion de password. validaPass = False (El default es True)
                    if (validaPass):
                        # Llama al metodo desencriptaDato de la clase Seg_EncriptacionSvos para validar si la clave proporcionada es correcta. TRUE = Mismo password
                        tuplaEncriptado = Seg_EncriptacionSvos.desencriptaDato(resPassword, claveClaro)
                        if (tuplaEncriptado[0]):                        # Error en la encriptacion. No coincide el password
                            return (True, 'Error en la clave de usuario o password')
                        else:                                           # Encriptacion correcta
                            validaPassword = True
                    else:    
                        validaPassword = validaPass

                    user.password = validaPassword

                    # Llama al metodo genera_token de la clase Seg_TokenSvos para generar el Token de autorizacion 
                    tuplaToken = Seg_TokenSvos.genera_token(user, vigencia)
                    if (tuplaToken[0]):                              # Error en la generacion de token
                        return (True, 'Error en la generacion de TOKEN')

                    argToken = tuplaToken[1]        
                    # Regresa bandera indica que no hay Error (False), clase Usuario actualizado y el token de autorizacion generado                
                    return (False, user, argToken)
                else:
                    return (True, 'La clave de usuario no es operativo')
            else:                                   # No existe registro con ese email
                return (True, 'Error en la clave de usuario o password')
            
        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def UsuarioSvos.valida_usuario ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            return (True, msgErrorDef)

    
    @classmethod
    def lista_usuarios(cls, argNumVersion, ArgCurrentApp):
        try:
            datosRespuesta = {
                'error': False, 
                'mensaje': ''
            }
            
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            query = f'''SELECT u.id, u.email, u.fullname, u.id_perfil, p.descripcion, u.id_empresa, e.cve_empresa, e.nombre, u.vigente,
                	    u.id_usuario_alta, to_char(u.fecha_alta, 'DD/MM/YYYY HH:MM:SS') , u.id_usuario_actualiza, 
                        to_char(u.fecha_actualizacion, 'DD/MM/YYYY HH:MM:SS')
                        FROM usuario u, perfil p, empresa e
                        WHERE u.id_perfil  = p.id
                        AND   u.id_empresa  = e.id;'''

            cursor.execute(query)
            respuesta = cursor.fetchall()
            datosResultado = respuesta
            if connection:
                cursor.close()
                connection.close()

            #Valida si datosResultado esta vacio
            if (len(datosResultado) <= 0):
                msgError = 'No se ha encontrado ningun resultado con los parametros de busqueda'
                ErrorSistema = False
                return (True, msgError, ErrorSistema)

            lstUsuario = []
            # La respuesta es una lista de listas, la respuesta debe ser en un JSON
            resJSON = []
            for usuario in respuesta:
                lstRegistro = []
                str_id = usuario[0]                         # Id del usuario
                str_email = usuario[1]                      # Email del correo
                str_nombre = usuario[2]                     # Nombre del usuario
                str_idPerfil = usuario[3]                   # Id del Perfil
                str_nombrePerfil = usuario[4]               # Nombre del Perfil
                str_cveEmpresa = usuario[5]                 # Clave de la empresa
                str_idEmpresa = usuario[6]                  # ID de la empresa
                str_nomEmpresa = usuario[7]                 # Nombre de la empresa
                str_vigente = usuario[8]                    # Estado del usuario
                str_usuarioAlta = usuario[9]                # Id usuario de alta
                str_fechaAlta = usuario[10]                 # Fecha de alta
                str_usuarioActualiza = usuario[11]          # Id usuario que actualizo
                str_fechaActualizacion = usuario[12]        # Fecha de actualizacion

                # Agregamos los datos de las Empresas a lstRegistro
                lstRegistro.append(str_id)        
                lstRegistro.append(str_email)        
                lstRegistro.append(str_nombre)        
                lstRegistro.append(str_idPerfil)        
                lstRegistro.append(str_nombrePerfil)        
                lstRegistro.append(str_cveEmpresa)        
                lstRegistro.append(str_idEmpresa)        
                lstRegistro.append(str_nomEmpresa)        
                lstRegistro.append(str_vigente)        
                lstRegistro.append(str_usuarioAlta)        
                lstRegistro.append(str_fechaAlta)        
                lstRegistro.append(str_usuarioActualiza)        
                lstRegistro.append(str_fechaActualizacion)        

                # Agregamos lstRegistro a la lista de tipos de documemtos lstUsuario
                lstUsuario.append(lstRegistro)    

            campos = ('id', 'email', 'nombre', 'id_perfil', 'nombre_perfil', 'cve_empresa', 'id_empresa', 'nombre_empresa', 'vigente', 'id_usuario_alta', 'fecha_alta', 'id_usuario_actualiza', 'fecha_actualizacion')
            for registro in lstUsuario:
                resJSON.append(dict(zip(campos, registro)))

            mensaje = 'Consulta realizada exitosamente'
            datosRespuesta['mensaje'] = mensaje
            datosRespuesta['datos'] = resJSON
            datosRespuesta['error'] = False
            ErrorSistema = False

            return (False, datosRespuesta, ErrorSistema)

        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def UsuarioSvos.lista_usuarios ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            ErrorSistema = True
            return (True, msgErrorDef, ErrorSistema)


    @classmethod
    def consulta_usuario(cls, ArgCurrentApp, user): 
        try:
            # Conexion a la BBDD (Postgres)    
            db = PostgresBase(ArgCurrentApp)    
            connection = db.conexion()
            cursor = db.cursor()
            cursor.execute(''' select * from usuario where email = %s ''', [user.email]) 
            regto = cursor.fetchall()
            cursor.close()
            connection.close()

            # Validamos si la respuesta trae elementos o esta vacia
            if (regto):
                # Guarda en la variable usuario el primer registro recuperado de la consulta
                resID = regto[0][0]
                # Obtiene el campo con el nombre del usuario
                resNombre = regto[0][2]
                # Obtiene el password encriptado del registro del usuario recuperado
                resPassword = regto[0][3]
                # Obtiene el campo que identifica el id del Perfil asignado
                resPerfil = regto[0][4]
                # Obtiene la clave de la empresa asociada al usuario
                resEmpresa = regto[0][5]
                # Obtiene el campo que identifica si el usuario es vigente
                resVigente = regto[0][6]
                # Obtiene el campo que identifica ID del usuario que dio de alta el registro
                resIDAlta = regto[0][7]
                # Obtiene el campo que identifica Fecha y Hora que se dio de alta el registro
                resTSalta = regto[0][8]
                # Obtiene el campo que identifica ID del usuario que realizo la ultima actualizacion el registro
                resIDActualizo = regto[0][9]
                # Obtiene el campo que identifica Fecha y Hora cuando se realizo la ultima actualizacion el registro
                resTSactualizo = regto[0][10]

                user.id = resID
                user.fullname = resNombre
                user.password = resPassword
                user.id_perfil = resPerfil
                user.empresa = resEmpresa
                user.vigente = resVigente
                user.id_usuario_alta = resIDAlta
                user.fecha_alta = resTSalta
                user.id_usuario_actualiza = resIDActualizo
                user.fecha_actualizacion = resTSactualizo

                return (False, user)

            else:                                   # No existe registro con ese email
                return (True, 'Error en la clave de usuario o password')
            
        except Exception as ex:
            Logger.add_to_log("critical", str('===================================================================='))
            Logger.add_to_log("critical", str('*** def UsuarioSvos.consulta_usuario ***'))
            Logger.add_to_log("critical", str(ex))
            Logger.add_to_log("critical", traceback.format_exc())
            msgErrorDef = str(ex)
            return (True, msgErrorDef)


    # @classmethod
    # def roles_usuario(cls, ArgCurrentApp, user):
    #     try:
    #         # Conexion a la BBDD (Postgres)    
    #         db = PostgresBase(ArgCurrentApp)    
    #         connection = db.conexion()
    #         cursor = db.cursor()

    #         # Llama al metodo encriptaDato de la clase SeguridadServicios para encriptar el password del 
    #         tuplaEncriptado = EncriptacionSvos.encriptaDato(user.password)
    #         if (tuplaEncriptado[0]):                        # Error en la encriptacion
    #             return (True, None)
    #         else:                                           # Encriptacion correcta
    #             passwordEncriptado = tuplaEncriptado[1]

    #         cursor = connection.cursor()
    #         query = 'INSERT INTO seg_usuarios '
    #         query += f''' (email, fullname, clave, cve_empresa, vigente)
    #                        VALUES
    #                       (%s, %s, %s, %s, %s) RETURNING id;; 
    #                   '''
    #         datos = (user.email, user.fullname, passwordEncriptado, user.empresa, user.vigente)
    #         cursor.execute(query, (datos))

    #         # Obtiene el ID generado en la BBDD
    #         count = cursor.rowcount
    #         ID_usuario = cursor.fetchone()[0]
    #         connection.commit()
    #         cursor.close()
    #         connection.close()

    #         if (ID_usuario > 0):
    #             return (False, ID_usuario)
    #         else:
    #             return (True, None)
            
    #     except Exception as ex:
    #         Logger.add_to_log("critical", str('===================================================================='))
    #         Logger.add_to_log("critical", str('*** def UsuarioSvos.roles_usuario ***'))
    #         Logger.add_to_log("critical", str(ex))
    #         Logger.add_to_log("critical", traceback.format_exc())
    #         msgErrorDef = 'Servicio no disponible por el momento'
    #         return (True, msgErrorDef)

