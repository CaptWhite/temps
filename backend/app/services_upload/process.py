from more_itertools import unzip
from app.services_upload.astrometry import director
from app.services_upload.unzip import unzip
#from app.services_upload.astropypy import get_apparent
from app.services_calculate.calc_star import get_apparent
from app.services_upload.pilpy import add_star_names
from app.services_upload.simbad   import get_simbad_df
from app.services_upload.unities   import convert_units
from app.services_upload.plate_constants import calculate_plate
import io

import os
from dotenv import load_dotenv
load_dotenv()
MACHINE = os.getenv('MACHINE')
TRACE = os.getenv('TRACE')

def print_xlsx(filename, df, suffix):
    if MACHINE == 'localhost' and TRACE == '1':
        str = filename.rsplit('.', 1) [0]
        df.to_excel(f'./auxiliar/{str}{suffix}') 

def print_jpg(filename, image, suffix):
    if MACHINE == 'localhost' and TRACE == '1':
        str = filename.rsplit('.', 1) [0]
        image.save(f'./auxiliar/{str}{suffix}')         

async def main_process(file, date):
    filename = file.filename  
    filebytes = await file.read()

    #################  UNZIP.NET   #####################
    if filename.endswith('.zip'):
        df, fileImg = unzip(filename, filebytes) 
        filename = fileImg.name  
        filebytes = fileImg.content.getvalue()

    #################  ASTROMETRY.NET   #####################
    else:
        df = director(filename, filebytes) 
        print_xlsx(filename, df, '.corr.xlsx') 

    #################  SIMBAD   #####################
    stars = get_simbad_df(df)
    print_xlsx(filename, stars, '.simbad.xlsx') 

    #################  ASTROPY   #####################
    #stars = get_apparent(stars, date)
    #print_xlsx(filename, stars, '.astropy.xlsx')

    #################  CALCULS   #####################
    stars = get_apparent(stars, date)
    print_xlsx(filename, stars, '.calculs.xlsx')
    
    ##### CAMBIO DE UNIDADES de ANGULO ###########
    stars = convert_units(stars)
    print_xlsx(filename, stars, '.units.xlsx')

    ############ PLATE CONSTANTS #############
    stars, plate = calculate_plate(stars)
    print_xlsx(filename, stars, '.astropy-units.xlsx')  
    print_xlsx(filename, plate, '.plate-coefs.xlsx')  

    #################  PIL   ##################### 
    img_bytes, PIL_image = add_star_names(filebytes, stars)
    print_jpg(filename, PIL_image, '.named.jpg') 

    #################  RETORNO #####################
    csv_buffer = io.StringIO()
    csv_bytes = stars.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()

    csv2_buffer = io.StringIO()
    csv2_bytes = plate.to_csv(csv2_buffer, index=False)
    csv2_string = csv2_buffer.getvalue()

    print('Fin procesos')

    return img_bytes, csv_string, csv2_string  #  stars.to_json()