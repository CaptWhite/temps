import time
import requests
import json
import os
import zipfile
import io
from dotenv import load_dotenv

from app.services_upload.fits_to_df import convert_to_df


import zipfile
import io
from dataclasses import dataclass

# from fits_to_df import convert_to_df

@dataclass
class File:
    name: str
    content: io.BytesIO

def unzip(filename, filebytes):
    with zipfile.ZipFile(io.BytesIO(filebytes)) as z:
        # Obtener la lista de archivos en el ZIP
        names = z.namelist()

        if len(names) != 2:
            raise ValueError(f"Se esperaban exactamente 2 archivos en el ZIP, pero se encontraron {len(names)}.")

        # Inicializar los objetos File
        fileCorr = None
        fileImg = None

        for name in names:
            # Leer el contenido del archivo
            with z.open(name) as f:
                content = io.BytesIO(f.read())

            file_obj = File(name=name, content=content)

            if name.endswith('.corr.fits'):
                if fileCorr is not None:
                    raise ValueError("Hay más de un archivo que termina en '.corr.fits'.")
                fileCorr = file_obj
            else:
                if fileImg is not None:
                    raise ValueError("Hay más de un archivo que no termina en '.corr.fits'.")
                fileImg = file_obj

        if fileCorr is None or fileImg is None:
            raise ValueError("No se encontraron ambos archivos esperados: uno con '.corr.fits' y otro distinto.")
        
        df = convert_to_df(fileCorr.content.getvalue())

        return df, fileImg  




########################################################################
########################################################################

def main():
    image = 'albireo.zip'
    image_name, image_extension = os.path.splitext(image)
    image_path = f'.\\auxiliar\\{image}'  # Reemplaza con la ruta a tu imagen
    
    with open(image_path, 'rb') as f:
        filebytes = f.read()
    filename = image
    unzip(filename, filebytes)

    try:
        # Paso 0: Login
        pass
        # print ({'session': session})

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == '__main__':
    main()
