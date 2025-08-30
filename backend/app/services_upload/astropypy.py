from astropy.coordinates import SkyCoord, EarthLocation, FK5
from astropy.time import Time
import astropy.units as u
from astropy.coordinates import SkyCoord, ICRS, GCRS

def star_apparent(_ra, _dec, _pm_ra, _pm_dec, _rad_vel, _dist, _time='2000-01-01T12:00:00'):
    print (_ra, _dec, _pm_ra, _pm_dec, _rad_vel, _dist, _time)
    # Coordenadas astrofísicas en J2000 (ICRS) para un objeto con movimiento propio
    ra = _ra * u.deg  # Ascensión Recta (RA) en grados
    dec = _dec * u.deg  # Declinación (Dec) en grados
    pm_ra_cosdec = _pm_ra * u.mas/u.yr  # Movimiento propio en RA (mas/año)
    pm_dec = _pm_dec * u.mas/u.yr  # Movimiento propio en Dec (mas/año)
    radial_velocity = _rad_vel * u.km/u.s  # Velocidad radial (opcional)
    dist = _dist * u.pc  # Distancia en parsecs (opcional)
    

    # Fechas de referencia inicial y objetivo
    time_initial = Time('J2000.0')  # Época inicial de referencia
    time_target = Time(_time)  # Fecha objetivo

    # Coordenadas iniciales en ICRS con movimiento propio
    star = SkyCoord(ra=ra, dec=dec, distance=dist,
                pm_ra_cosdec=pm_ra_cosdec, pm_dec=pm_dec,
                radial_velocity=radial_velocity,
                frame='icrs', obstime='J2000')

    # Corrección 1: Movimiento propio
    star_proper_motion = star.apply_space_motion(dt=(time_target - time_initial))

    # Convertir a GCRS para incluir precesión, nutación y aberración
    star_gcrs = star_proper_motion.transform_to(GCRS(obstime=time_target))

    # Resultados
    ra_result = star_gcrs.ra.to(u.deg).value
    dec_result = star_gcrs.dec.to(u.deg).value

    return [ra_result, dec_result]

def get_apparent(df, time):
    
    df[['ar_app', 'dec_app']] = df.apply(lambda row: star_apparent(row['ra'], row['dec'], row['pmra_x'], row['pmdec_x'], row['rvz_radvel'], 100 if row['plx_value'] == 0 else 1000/row['plx_value'], time), axis=1, result_type='expand')
    
    # df.to_excel(file)

    return df
