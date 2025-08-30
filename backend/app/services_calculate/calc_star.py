from app.services_calculate._rutines import calculate, julian_date, radian_to_degree, scale_angle



lon_dms = '02°09\'33.0\"E'
lat_dms = '41°28\'08.0\"N'
press = 1013.25 # Presión en hPa
temp = 10.0     # Temperatura en grados Celsius


def star_apparent(row, date, lon_dms, lat_dms, press, temp):
    date = date.replace('T', ' ')
    spl = date.replace('-', ' ').replace(':', ' ').split(' ')
    jdate = julian_date(int(spl[0]), int(spl[1]), int(spl[2]), int(spl[3]), int(spl[4]))
    result = calculate(row['main_id'], date, jdate, lon_dms, lat_dms, temp, press)
    
    return [radian_to_degree(scale_angle(result['refraction']['ar'])), radian_to_degree(scale_angle(result['refraction']['dec'])), result]



def get_apparent(df, time, longitude=lon_dms, latitude=lat_dms, pressure=press, temperature=temp):
    
    df[['ar_app', 'dec_app', 'result']] = df.apply(lambda row: star_apparent(row, time, longitude, latitude, pressure, temperature), axis=1, result_type='expand')

    # df.to_excel(file)

    return df