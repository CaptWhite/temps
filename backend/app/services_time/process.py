from datetime import datetime
from app.services_calculate._rutines import convert_params, equation_of_equinoxes, radian_to_degree
from app.services_time.utilities   import ecuacion_tiempo, convert_utc, get_italica_babilonica, gmst, sunrise_sunset



async def main_process(data):
    date_time = data['date_time']
    longitude = data['longitude']
    latitude = data['latitude']

    utc = convert_utc(date_time)
    [jd, lon, lat]= convert_params(utc, longitude, latitude)
    eot_hour = ecuacion_tiempo(datetime.fromisoformat(date_time))
    gmst_hour = gmst (jd)
    eoe = equation_of_equinoxes (jd)
    eoe_hour = radian_to_degree(eoe) / 15

    sunrise, sunset, solar_noon, day_length = sunrise_sunset(date_time, latitude, longitude)

    hour_italica, hour_babilonica = get_italica_babilonica(date_time.split('T')[1], sunrise, sunset)

    return {
        "date_time_sol": date_time,
        "lon_hour": lon/15,  # Convertir a horas
        "eot_hour": eot_hour,  # Convertir a horas
        "date_time_julian": jd,
        "date_time_gmst": gmst_hour,
        "date_time_mst": gmst_hour + lon/15,
        "eoe_hour": eoe_hour,  
        "sunrise": sunrise,  
        "sunset": sunset,  
        "solar_noon": solar_noon,  
        "day_length": day_length, 
        "hour_italica": hour_italica,      
        "hour_babilonica": hour_babilonica   
    }

import os