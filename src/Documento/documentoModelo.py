import os
import io
import argparse
from datetime import datetime
from PIL import Image
from pdf2image import convert_from_path
from google.cloud import vision
from cv2 import imread, imwrite, rotate, ROTATE_180, ROTATE_90_CLOCKWISE, ROTATE_90_COUNTERCLOCKWISE
from pyzbar.pyzbar import decode
import base64

#*******************************************************************************************
#   DOCUMENTO   
#   Definimos la clase Documento con la informacion del modelo
#*******************************************************************************************
class Documento():

    # Definimos los campos que tiene el modelo Documento
    def __init__(self, ruta: str, dir_carga: str) -> None:
        self.ruta = ruta
        self.nombre = os.path.splitext(ruta)[0].split('/')[-1]
        self.ext = os.path.splitext(ruta)[-1].lower()
        self.dir_cargas = dir_carga
        self.es_valido = self.imagen_es_valida(ruta)
        self.conversion_jpeg = False
        self.tipo_documento = 'generico'
        self.fecha_creacion = datetime.now().isoformat()


    def __str__(self) -> str:
        cadena = f'''
            RUTA DOC:               {self.ruta}
            NOMBRE DOC:             {self.nombre}
            EXTENCION DOC:          {self.ext}
            CONVERSION A JPEG:      {self.conversion_jpeg}
            DIRECTORIO CARGAS DOC:  {self.dir_cargas}
            DOCUMENTO ES VALIDO:    {self.es_valido}
            FECHA DE CREACION:      {self.fecha_creacion}
            '''
        return cadena


    def __repr__(self) -> str:
        if not self.conversion_jpeg:
            return f"Documento('{self.ruta}')"
        else:
            return f"Documento('{self.dir_cargas}{self.nombre}.jpeg')"
        

    def imagen_es_valida(self, ruta: str):
        if self.ext == '.pdf':
            return True

        try:
            Image.open(ruta).verify()
            return True
        except (IOError, SyntaxError) as e:
            print(f'Invalid or corrupt image file {ruta}. Error: {e}')
            return False


    def convertir_jpeg(self):
        nueva_ruta = []
        if not self.es_valido:
            nueva_ruta.append('No hay ruta porque el archivo esta corrupto')
            return nueva_ruta

        if self.ext == '.pdf':
            imagenes = convert_from_path(self.ruta)
            for i in range(len(imagenes)):
                nombre_nueva_pag = self.dir_cargas + self.nombre + 'pagina' + str(i) +'.jpeg'
                nueva_ruta.append(nombre_nueva_pag)
                imagenes[i].save(nombre_nueva_pag, 'JPEG')
        elif self.ext in ['.png', '.jpg']:
            nueva_ruta.append(self.dir_cargas + self.nombre + '.jpeg')
            nueva_img = Image.open(self.ruta)
            if self.ext == '.png':
                nueva_img = nueva_img.convert('RGB')
            nueva_img.save(nueva_ruta[0])
        elif self.ext == '.jpeg':
            nueva_ruta.append(self.ruta)
    
        self.conversion_jpeg = True
        return nueva_ruta


    def extraer_texto_google(self, nueva_ruta=''):
        info_paginas = []
        if not self.es_valido:
            info_paginas.append('No hay información porque el archivo esta corrupto')
            return info_paginas

        client = vision.ImageAnnotatorClient()
        if (self.ext != '.jpeg') and (nueva_ruta == ''):
            nueva_ruta = self.convertir_jpeg()
        elif (self.ext == '.jpeg') and (nueva_ruta == ''):
            nueva_ruta = [self.ruta]
        else:
            nueva_ruta = [nueva_ruta]

        for pag in nueva_ruta:
            #print(pag)
            with io.open(pag, 'rb') as image:
                content = image.read()
            image = vision.Image(content=content)
            response = client.document_text_detection(image = image)
            info_paginas.append(response.text_annotations)

        return info_paginas


    def rotar_imagen(self, orientacion: int):
        if not self.conversion_jpeg:
            ruta = self.convertir_jpeg()[0]
        else:
            ruta = self.dir_cargas + self.nombre + '.jpeg'
    
        imagen = imread(ruta)

        if orientacion == 1:
            imageOut = rotate(imagen, ROTATE_90_COUNTERCLOCKWISE)
        elif orientacion == 2:
            imageOut = rotate(imagen, ROTATE_180)
        elif orientacion == 3:
            imageOut = rotate(imagen, ROTATE_90_CLOCKWISE)
        imwrite(ruta, imageOut)

        return
            
 
    def leer_codigo_QR(self):
        if not self.conversion_jpeg:
            ruta = self.convertir_jpeg()
        else:
            ruta = [self.dir_cargas + self.nombre + '.jpeg']
        
        values = []
        for r in ruta:
            image = imread(r)
            qr_codes = decode(image)
            if qr_codes:
                for qr_code in qr_codes:
                    qr_data = qr_code.data.decode('utf-8')
                    values.append(qr_data)
        return values


    def convertir_base64(self):
        if not self.conversion_jpeg:
            ruta = self.convertir_jpeg()[0]
        else:
            ruta = self.dir_cargas + self.nombre + '.jpeg'
    
        with open(ruta, 'rb') as doc:
            doc_codificado = base64.b64encode(doc.read())

        doc_base64 = doc_codificado.decode('utf-8')
        return doc_base64
    

    def to_json(self):
        return {
            'ruta': self.ruta,
            'nombre': self.nombre,
            'ext': self.ext,
            'dir_cargas': self.dir_cargas,
            'es_valido': self.es_valido,
            'conversion_jpeg': self.conversion_jpeg,
            'tipo_documento': self.tipo_documento,
            'fecha_creacion': self.fecha_creacion,
        }
 

def get_args():
    "Obtener argumentos de la linea de comandos"

    parser = argparse.ArgumentParser(
        description='Crear objeto de la clase Documento',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('ruta',
                        metavar='ruta',
                        help='ruta del documento')

    return parser.parse_args()


if __name__ == '__main__':
    ruta = get_args().ruta
    doc = Documento(ruta)
    print(dir(doc))
    print(doc)

    #nueva_ruta = doc.convertir_jpeg()
