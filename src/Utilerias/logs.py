import logging
import os
import traceback


#   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#   Funcion para obtener informacion de la excepcion generada
#   :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def excepcionInformacion(ex):
    printDebug = True

    trace = []
    tb = ex.__traceback__
    while tb is not None:
        trace.append({
            "componente": tb.tb_frame.f_code.co_filename,
            "funcion": tb.tb_frame.f_code.co_name,
            "numLinea": tb.tb_lineno
        })
        tb = tb.tb_next

    msgError = str({
        'type': type(ex).__name__,
        'message': str(ex),
        'trace': trace
    })

    if (printDebug):
        print('\t\t ' + str({
            'type': type(ex).__name__,
            'message': str(ex),
            'trace': trace
        }))

    return msgError


class Logger():

    def __set_logger(self):
        log_directory = 'logs'
        log_filename = 'app.log'

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        if (logger.hasHandlers()):
            logger.handlers.clear()

        logger.addHandler(file_handler)

        return logger
    
    @classmethod
    def add_to_log(cls, level, message):
        try:
            logger = cls.__set_logger(cls)
            
            if (level == "critical"):
                logger.critical(message)
            elif (level == "debug"):
                logger.debug(message)
            elif (level == "error"):
                logger.error(message)
            elif (level == "info"):
                logger.info(message)
            elif (level == "warn"):
                logger.warn(message)
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)
