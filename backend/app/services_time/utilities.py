from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import numpy as np
import requests
from scipy.optimize import fsolve
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
import astropy.units as u

from app.services_calculate._rutines import mean_obliquity, nutation_parameters_2000


# def equinox_equation(jd):
#   T = (jd - 2451545.0) / 36525
#   [dpsi, deps, w] = nutation_parameters_2000(jd)
#   epsm = mean_obliquity (jd)
#   eps = epsm + deps
#   EE = dpsi * math.cos(eps)
#   return EE * 180 / math.pi / 15  # Devuelve la EE en horas


# Funciones auxiliares
def kepler(M, e):
    func = lambda E: E - e * np.sin(E) - M
    E0 = M if e < 0.8 else np.pi
    return fsolve(func, E0)[0]

def ecuacion_tiempo(date_time):
    e = 0.0167
    epsilon = np.radians(23.44),
    T = 365.25
    omega = np.radians(102.9372)

    dia_entero = date_time.timetuple().tm_yday
    fraccion = (date_time.hour + date_time.minute / 60 + date_time.second / 3600) / 24
    t = dia_entero + fraccion

    M = 2 * np.pi * t / T
    E = kepler(M, e) 
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                        np.sqrt(1 - e) * np.cos(E / 2))
    lamb = nu + omega
    lamb = np.mod(lamb, 2 * np.pi)

    alpha = np.arctan2(np.cos(epsilon) * np.sin(lamb), np.cos(lamb))
    delta = -np.arcsin(np.sin(epsilon) * np.sin(lamb))

    alpha_deg = np.degrees(alpha)
    lambda_mean_deg = np.degrees(np.mod(M + omega, 2 * np.pi))
    EoT_deg = - lambda_mean_deg + alpha_deg
    EoT_deg = (EoT_deg + 180) % 360 - 180
    EoT_hor = (EoT_deg / 15)
    return EoT_hor[0]

def convert_utc(date):
    # Crear datetime en UTC
    # Interpretar la hora como hora oficial de Madrid (con DST aplicado)
    fecha_local = datetime.fromisoformat(date)
    fecha_madrid = fecha_local.replace(tzinfo=ZoneInfo("Europe/Madrid"))

    # Convertir a UTC
    fecha_utc = fecha_madrid.astimezone(ZoneInfo("UTC"))

    # Convertir a string en formato "yyyy-MM-ddThh:mm:ss"
    fecha_formateada = fecha_utc.strftime("%Y-%m-%dT%H:%M:%S")
    return fecha_formateada

def gmst(jd):
    T = (jd - 2451545.0) / 36525
    gmst_deg = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * T**2
        - T**3 / 38710000
    )
    gmst_deg = gmst_deg % 360  # normalizar a [0, 360)
    gmst_hours = gmst_deg / 15
    return gmst_hours  # en horas

def segundos_a_hh_mm_ss(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos_restantes = segundos % 60
    return f"{horas:02}:{minutos:02}.{segundos_restantes:02}"

def obtener_hora_local(date):
    # Convertir a datetime con zona horaria UTC
    hora_utc = datetime.fromisoformat(date)
    # Convertir a hora local (ejemplo: España peninsular)
    hora_local = hora_utc.astimezone(ZoneInfo("Europe/Madrid"))
    # Obtener solo la hora formateada (HH:MM:SS)
    hora_str = hora_local.strftime("%H:%M:%S")
    return hora_str

def sunrise_sunset(date, lat_dms, lon_dms):

    lat = Angle(lat_dms).degree
    lon = Angle(lon_dms).degree    # Usar en la API
    date_ = date.split('T')[0]
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date_}&formatted=0"
 
    response = requests.get(url)
    data = response.json()['results']
 
    return obtener_hora_local(data['sunrise']), obtener_hora_local(data['sunset']),obtener_hora_local( data['solar_noon']), segundos_a_hh_mm_ss(data['day_length'])

def get_italica_babilonica(oficial, sunrise, sunset):
    fmt = "%H:%M:%S"
    oficial = datetime.strptime(oficial, fmt)
    sunrise = datetime.strptime(sunrise, fmt)
    sunset = datetime.strptime(sunset, fmt)

    if sunset > oficial:
        # 24:00:00 se representa como 1 día completo
        veinticuatro = timedelta(hours=24)
        diferencia = sunset - oficial
        italica_timedelta = veinticuatro - diferencia
    else:
        italica_timedelta = oficial - sunset

    if sunrise > oficial:
        # 24:00:00 se representa como 1 día completo
        veinticuatro = timedelta(hours=24)
        diferencia = sunrise - oficial
        babilonica_timedelta = veinticuatro - diferencia
    else:
        babilonica_timedelta = oficial - sunrise    

    # # Convertir timedelta a string hh:mm:ss
    # total_segundos = int(italica_timedelta.total_seconds())
    # horas = total_segundos // 3600
    # minutos = (total_segundos % 3600) // 60
    # segundos = total_segundos % 60
    # italica = f"{horas:02}:{minutos:02}:{segundos:02}"

    # # Convertir timedelta a string hh:mm:ss
    # total_segundos = int(babilonica_timedelta.total_seconds())
    # horas = total_segundos // 3600
    # minutos = (total_segundos % 3600) // 60
    # segundos = total_segundos % 60
    # babilonica = f"{horas:02}:{minutos:02}:{segundos:02}"

    italica = italica_timedelta.total_seconds() / 3600
    babilonica = babilonica_timedelta.total_seconds() / 3600


    return italica, babilonica


def main():

    result = ecuacion_tiempo(datetime(2023, 10, 1, 12, 0, 0))
    print(f"Ecuación del tiempo para el 1 de octubre de 2023 a las 12:00: {result*60:.5f} horas")  

    italica, babilonica = get_italica_babilonica('2025-07-28T04:00:00', '41°23\'19"N', '02°09\'32"E')
    print (f"Italica: {italica}, Babilonica: {babilonica}")

if __name__ == "__main__":
    main()
    #uvicorn app.main:app --reload

