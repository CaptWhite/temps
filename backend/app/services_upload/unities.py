from astropy.coordinates import Angle
import astropy.units as u
import math


def convert_units_item(ra_degrees, dec_degrees):

  # Convertir RA a formato horas:minutos:segundos
  ra = Angle(ra_degrees, unit=u.degree)
  ra_hms = ra.hms  # Obtiene horas, minutos, segundos como tupla
  ra_str = f"{int(ra_hms.h):02d}h{int(ra_hms.m):02d}m{ra_hms.s:05.3f}s"

  # Convertir DEC a formato grados:minutos:segundos
  dec = Angle(dec_degrees, unit=u.degree)
  dec_dms = dec.dms  # Obtiene grados, minutos, segundos como tupla
  dec_sign = '-' if dec_degrees < 0 else '+'  # Determinar el signo
  dec_str = f"{dec_sign}{abs(int(dec_dms.d)):02d}°{abs(int(dec_dms.m)):02d}'{abs(dec_dms.s):05.3f}\""

  ra_rad = ra_degrees * math.pi / 180
  dec_rad = dec_degrees * math.pi / 180
  return ra_str, dec_str, ra_rad, dec_rad

def convert_units(df):
    
    df[['ra_dms', 'dec_hms', 'ra_rad', 'dec_rad']] = df.apply(lambda row: convert_units_item(row['ar_app'], row['dec_app']), axis=1, result_type='expand')
    df[['field_ra_dms', 'field_dec_hms', 'field_ra_rad', 'field_dec_rad']] = df.apply(lambda row: convert_units_item(row['field_ra'], row['field_dec']), axis=1, result_type='expand')
    df[['ra_app_dms', 'dec_app_hms', 'ar_app_rad', 'dec_app_rad']] = df.apply(lambda row: convert_units_item(row['ar_app'], row['dec_app']), axis=1, result_type='expand')
    
    # df.to_excel(file)
    return df

