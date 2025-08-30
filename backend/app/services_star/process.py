from app.services_calculate._rutines import degree_to_radian
from app.services_calculate.calc_star import get_apparent
from app.services_upload.simbad   import get_simbad_star
from app.services_upload.unities   import convert_units

from astropy.coordinates import Angle
import astropy.units as u
import math

import os
from dotenv import load_dotenv
load_dotenv()
MACHINE = os.getenv('MACHINE')
TRACE = os.getenv('TRACE')

def convert_units_item(ra, dec):
  
  # Convertir RA a formato horas:minutos:segundos
  ra = Angle(ra, unit=u.radian)
  ra_hms = ra.hms  # Obtiene horas, minutos, segundos como tupla
  ra_str = f"{int(ra_hms.h):02d}h{int(ra_hms.m):02d}m{ra_hms.s:05.3f}s"

  # Convertir DEC a formato grados:minutos:segundos
  dec = Angle(dec, unit=u.radian)
  dec_dms = dec.dms  # Obtiene grados, minutos, segundos como tupla
  dec_sign = '-' if dec < 0 else '+'  # Determinar el signo
  dec_str = f"{dec_sign}{abs(int(dec_dms.d)):02d}°{abs(int(dec_dms.m)):02d}'{abs(dec_dms.s):05.3f}\""

  ra_deg = float(ra.degree)
  dec_deg = float(dec.degree)
  return ra_str, dec_str, ra_deg, dec_deg

def reorganizar_json1(data):
    resultado = {}

    for seccion, contenido in data.items():
        nuevo_obj = {}

        # Extraer 'ar' y 'dec'
        if 'ar' in contenido:
            nuevo_obj['ar'] = contenido['ar']
        if 'dec' in contenido:
            nuevo_obj['dec'] = contenido['dec']

        # Coordenadas
        coords = {k: contenido[k] for k in ['x', 'y', 'z'] if k in contenido}
        if coords:
            nuevo_obj['coordenadas'] = coords

        # Resto en 'parametros'
        parametros = {k: v for k, v in contenido.items() if k not in ['ar', 'dec', 'x', 'y', 'z']}
        if parametros:
            nuevo_obj['parametros'] = parametros

        resultado[seccion] = nuevo_obj

    return resultado


def process_json(data):
    for key, subdict in data.items():
        if isinstance(subdict, dict):
            
            ar_str, dec_str, ar_deg, dec_deg = convert_units_item(subdict['ar'], subdict['dec'])
            subdict['ar_deg'] = ar_deg
            subdict['dec_deg'] = dec_deg
            subdict['ar_hms'] = ar_str
            subdict['dec_dms'] = dec_str
    return data



def print_xlsx(filename, df, suffix):
    if MACHINE == 'localhost' and TRACE == '1':
        str = filename.rsplit('.', 1) [0]
        df.to_excel(f'./auxiliar/{str}{suffix}') 

async def main_process(data):
    starName = data['starName']
    date_time = data['date_time']
    longitude = data['longitude']
    latitude = data['latitude']
    pressure = data['pressure']
    temperature = data['temperature']

    #################  SIMBAD   #####################
    stars = get_simbad_star(starName)
    #print_xlsx(filename, stars, '.simbad.xlsx') 

#################  CALCULS   #####################
    stars = get_apparent(stars, date_time[:19], longitude, latitude, pressure, temperature)
    #print_xlsx(filename, stars, '.calculs.xlsx')

    resp = reorganizar_json1(stars['result'][0])
    processed_data = process_json(resp)
    print(processed_data)
    return processed_data