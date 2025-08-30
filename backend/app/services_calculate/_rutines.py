import pandas as pd
from astroquery.simbad import Simbad
import math
from app.services_calculate._params import get_params_2000

def getSimbad_mod(star):
    query = f"""SELECT b.main_id, b.ra, b.dec, b.pmra, b.pmdec FROM basic AS b JOIN ident AS i ON b.oid = i.oidref WHERE i.id like'{star}'"""
    
    # Ejecutar la consulta
    result = Simbad.query_tap(query)
    [data] = result.to_pandas().to_dict('records')
    x_simbad = spherical_to_rectangular (data['dec'], data['ra'], 1)
    coord_simbad = {'x': x_simbad[0], 'y': x_simbad[1], 'z': x_simbad[2], 'ar': degree_to_radian(data['ra']), 'dec': degree_to_radian(data['dec']), 'ar_deg': data['ra'], 'dec_deg': data['dec'], 'pmra': data['pmra'], 'pmdec': data['pmdec']}    
    return coord_simbad

def julian_date (a, m, d, h, min=0, sec=0):
    # Module of spatio­temporal transforms
    if (m < 3):
        a = a - 1
        m = m + 12
    jd = int(365.25*a)
    jd = jd + int(30.6001*(m+1)) + d
    qq = a + m/100.0 + d/1e4
    if (qq > 1582.10145):
        ib = int(a/100.0)
        jd = jd + 2 - ib + int(ib/4.0)
    return jd + 1720994.5 + h/24 + min/1440 + sec/86400

def degree_to_radian(d): # convierte grados a radianes
    return d * math.pi/180.0

def radian_to_degree(r):  # Convierte radianes a grados
    return r * 180.0/ math.pi

def scale_angle (a):  # sitúa un ángulo en [0,2p)
    return a - 2*math.pi*math.floor(a/(2*math.pi))

def rectangular_to_spherical (x):  # transforma coordenadas rectangulares a esféricas (azimutal, polar)
    #phi = Angulo azimutal
    phi = math.atan2 (x[1], x[0])
    #theta = Angulo polar
    theta = math.atan2(x[2], math.sqrt(x[0]**2 + x[1]**2))
    r = math.sqrt(x[0]**2 + x[1]**2 + x[2]**2)
    return [theta, phi, r]

def rectangular_to_spherical (x):  # transforma coordenadas rectangulares a esféricas
    phi = math.atan2 (x[1], x[0])
    theta = math.atan (x[2]/math.sqrt(x[0]**2 + x[1]**2))
    #theta = math.atan2 (x[1], x[0])
    #phi = math.atan (x[2]/math.sqrt(x[0]**2 + x[1]**2))
    r = math.sqrt(x[0]**2 + x[1]**2 + x[2]**2)
    return [theta, phi, r]

def spherical_to_rectangular (theta, phi, r): # transforma coordenadas esféricas (azimutal, polar) a rectangulares
    x = [0,0,0]
    x[0] = r*math.cos(theta)*math.cos(phi)
    x[1] = r*math.cos(theta)*math.sin(phi)
    x[2] = r*math.sin(theta)
    return x

def decorate_hhmmss(h):
    dec = '+' if h[0] > 0  else '-'
    dec = dec + str(h[1]).zfill(2) + 'h'
    dec = dec + str(h[2]).zfill(2) + 'm'
    dec = dec + '{:05.2f}'.format(round(h[3], 5)) + 's'
    return dec

def degree_to_hour (d):  # convierte grados a horas 
    return d / 15

def degree_to_ddmmss(a):  # Convierte grados (u horas) decimales a grados (u horas), minutos y segundos
    sig = math.copysign (1, a)
    ad = abs(a)
    d = int(ad)
    dm = 60*(ad - d)
    m = int(dm)
    s = 60*(dm - m)
    return [sig, d, m, s]

def hour_to_hhmmss (h) : # convierte horas a horas), minutos y segundos
    return degree_to_ddmmss(h)

def decorate_ddmmss(h):
    dec = '+' if h[0] > 0  else '-'
    dec = dec + str(h[1]).zfill(2) + '°'
    dec = dec + str(h[2]).zfill(2) + '\''
    dec = dec + '{:05.2f}'.format(round(h[3], 5)) + '"'
    return dec

def ddmmss_compact_to_degree(a):  #  formato compacto
    s = math.copysign (1, a)
    dd = abs(a)
    fdd = int(dd + 1e-8)
    dm = 100*(dd - fdd)
    fdm = int(dm + 1e-8)    
    ds = 100*(dm - fdm)
    return s*(fdd + fdm/60 + ds/3600)

def split_julian_date (jd):     #  [jd0, h]
    jd0 = int (jd + 0.5) - 0.5
    h = 24*(jd - jd0)
    return [jd0, h]

def hour_to_radian (h):  # convierte horas a radianes
    g = h * 15
    return degree_to_radian(g)
### ####################################################################################
#########   PROPER MOTION   ###########

def properMotion(date, dataSimbad):
    pm_ar = dataSimbad['pmra'] if not pd.isna(dataSimbad['pmra']) else 0      # Proper motion in right ascension (mas/yr)
    pm_dec = dataSimbad['pmdec'] if not pd.isna(dataSimbad['pmdec']) else 0   # Proper motion in declination (mas/yr)

    spl = date.replace('-', ' ').replace(':', ' ').split(' ')
    jdate = julian_date(int(spl[0]), int(spl[1]), int(spl[2]), int(spl[3]), int(spl[4]))
    years = (jdate - 2451545.0) / 36525
    data_pm = { 'ar': pm_ar * years / 36000, 'dec': pm_dec * years / 36000}
    coordPM = {'ar': degree_to_radian(dataSimbad['ar_deg'] + data_pm['ar']), 'dec': degree_to_radian(dataSimbad['dec_deg'] + data_pm['dec']), 'pmra': pm_ar, 'pmdec': pm_dec} 
    return coordPM

### ####################################################################################
#########   PRECESION   ###########

def rotation (n, theta, x): # efectúa una rotación elemental alrededor de un eje cartesiano
    x1 = [0,0,0]
    if (n == 1):
        x1[0] = x[0]
        x1[1] = x[1]*math.cos(theta) + x[2]*math.sin(theta)
        x1[2] =-x[1]*math.sin(theta) + x[2]*math.cos(theta)
    elif (n == 2):
        x1[0] = x[0]*math.cos(theta) - x[2]*math.sin(theta)
        x1[1] = x[1]
        x1[2] = x[0]*math.sin(theta) + x[2]*math.cos(theta)
    elif (n == 3):
        x1[0] = x[0]*math.cos(theta) + x[1]*math.sin(theta)
        x1[1] =-x[0]*math.sin(theta) + x[1]*math.cos(theta)
        x1[2] = x[2]
    return x1

def rotation_Euler (phi, xi, zeta, x): # efectúa una rotación de Euler
    x1 = []
    a = rotation (3, phi, x)
    b = rotation (1, xi, a)
    x1 = rotation (3, zeta, b)
    return x1

def precession_parameters (jd0, jd1):
    t0 = (jd0 - 2451545)/36525
    t = (jd1 - 2451545)/36525 - t0

    # angulos ecuatoriales (s, th, z)
    # criterio IAU 1976
    s = t*(2306.2181 + t0*(1.39656 - 0.000139*t0) + t*((0.30188 - 0.000345*t0) + 0.017998*t))
    th = t*(2004.3109 + t0*(-0.85330 - 0.000217*t0) + t*((-0.42665 - 0.000217*t0) - 0.041833*t))
    z = s + t**2*(0.79280 + 0.000411*t0 + 0.000205*t) 
    s = degree_to_radian (s/3600)
    z = degree_to_radian (z/3600)
    th = degree_to_radian (th/3600)

    # criterio IAU 2000 
    s = 2.650545 + 2306.083227*t + 0.2988499*t**2 + 0.01801828*t**3 - 0.000005971*t**4 - 0.0000003173*t**5
    th = 2004.191903*t - 0.4294934*t**2 - 0.04182264*t**3 - 0.000007089*t**4 - 0.0000001274*t**5
    z = -2.650545 + 2306.077181*t + 1.0927348*t**2 + 0.01826837*t**3 - 0.000028596*t**4 - 0.0000002904*t**5   
    s = degree_to_radian (s/3600)
    z = degree_to_radian (z/3600)
    th = degree_to_radian (th/3600)

    # angulos eclipticos (P, ph, L)
    P = t0*(3289.4789 + 0.60622*t0) + t*(-869.8089 - 0.50491*t0 + 0.03536*t)
    pa = t*(5029.0966 + t0*(2.22226 - 0.000042*t0) + t*(1.11113 - 0.000042*t0 - 0.000006*t))
    ph = t*(47.0029 + t0*(- 0.06603 + 0.000598*t0) + t*(-0.03302 + 0.000598*t0 + 0.000060*t))

    P = scale_angle (degree_to_radian (174.876383889 + P/3600))
    pa = degree_to_radian (pa/3600)
    ph = degree_to_radian (ph/3600)
    L = P + pa
    return [s, th, z, P, ph, L]

def precession_equatorial(jd0, jd1, x):
    [zeta, theta, z, P, ph, L] = precession_parameters (jd0, jd1)
    x1 = rotation_Euler (math.pi/2 - zeta, theta, -math.pi/2 - z, x)
    return [x1, [zeta, theta, z, P, ph, L]]  

def precession(jdate, ar, dec):  
    x_equ = spherical_to_rectangular (dec, ar, 1) 
    [x_prec_equ, [zeta, theta, z, P, ph, L]] = precession_equatorial(jd0=2451545.0, jd1=jdate, x=x_equ)
    dec, ar, r = rectangular_to_spherical (x_prec_equ)
    return {'x': x_prec_equ[0], 'y': x_prec_equ[1], 'z': x_prec_equ[2], 'ar': scale_angle(ar), 'dec': scale_angle(dec), 'ang_zeta': zeta, 'ang_theta': theta, 'ang_z': z} 

def convert_to_spherical_unities(title, coord):
    dec, ar, r = rectangular_to_spherical ([coord['x'], coord['y'], coord['z']])
    print (f'{title}  en  Radianes')
    print(f"- {'ar':10}: {ar}")
    print(f"- {'dec':10}: {dec}")
    print (f'{title}   en Grados')
    print(f"- {'ar':10}: {radian_to_degree(ar)}")
    print(f"- {'dec':10}: {radian_to_degree(dec)}")
    print (f'{title}   en Grados, Minutos, Segundos')
    print(f"- {'ar':10}:  {decorate_hhmmss(hour_to_hhmmss(degree_to_hour(radian_to_degree(ar))))}")
    print(f"- {'dec':10}:  {decorate_ddmmss(degree_to_ddmmss(radian_to_degree(dec)))}")

#
###    NUTACION  ########################################################
# 

def mean_obliquity (jd):
    t = (jd - 2451545.0)/36525
    epsm =  ((84381.448 \
         + t*(- 46.81500 + t*(- 0.00059 + 0.001813*t)))/3600)
    return degree_to_radian(epsm)

def nutation_parameters_2000 (jd):
    # TABLA DE PARAMETROS DE LA NUTACION
    
    a = get_params_2000()

    t = (jd - 2451545)/36525
    # mean heliocentric ecliptic longitudes of Mercury
    phi1 = degree_to_radian(( 908103.259872 + 538101628.688982*t) / 3600)  

    # mean heliocentric ecliptic longitudes of Venus
    phi2 = degree_to_radian((  655127.283060 + 210664136.433548*t) / 3600)    
    
    # mean heliocentric ecliptic longitudes of Earth
    phi3 = degree_to_radian(( 361679.244588 + 129597742.283429*t) / 3600)
    
    # mean heliocentric ecliptic longitudes of Mars
    phi4 = degree_to_radian( (1279558.798488 + 68905077.493988*t) / 3600)

    # mean heliocentric ecliptic longitudes of Jupiter
    phi5 = degree_to_radian(( 123665.467464 + 10925660.377991*t) / 3600)

    # mean heliocentric ecliptic longitudes of Saturn
    phi6 = degree_to_radian(( 180278.799480 + 4399609.855732*t) / 3600)

    # mean heliocentric ecliptic longitudes of Uranus
    phi7 = degree_to_radian(( 1130598.018396+ 1542481.193933*t) / 3600)

    # mean heliocentric ecliptic longitudes of Neptune
    phi8 = degree_to_radian(( 1095655.195728 + 786550.320744*t) / 3600)

    #  approximation to the general precession in longitude
    phi9 = degree_to_radian(( 5028.8200*t +1.112022*t**2 ) / 3600)

    # Anomalía media de la Luna: phi-10
    lm = degree_to_radian((485868.249036 + 1717915923.2178*t + 31.8792*t**2 + 0.051635*t**3 - 0.00024470*t**4) / 3600)

    # Anomalía media del Sol (Tierra): phi-11
    ls = degree_to_radian((1287104.79305 + 129596581.0481*t - 0.5532*t**2 + 0.000136*t**3 - 0.00001149*t**4) / 3600)

    # Argumento de latitud de la Luna: phi-12
    f = degree_to_radian((335779.526232 + 1739527262.8478*t - 12.7512*t**2 - 0.001037*t**3 + 0.00000417*t**4) / 3600)

    # La elongación media de la Luna desde el Sol se calcula con la siguiente fórmula: phi-13
    d = degree_to_radian((1072260.70369 + 1602961601.2090*t - 6.3706*t**2 + 0.006593*t**3 - 0.00003169*t**4) / 3600)

    # Longitud del nodo ascendente de la órbita media de la Luna en la eclíptica, phi-14
    w = degree_to_radian((450160.398036 - 6962890.5431*t + 7.4722*t**2 + 0.007702*t**3 - 0.00005939*t**4) / 3600)

    dpsi = 0
    deps = 0
    for j in range (0, 1365):
        i = j+1
        arg = scale_angle(a[i][0]*phi1 + a[i][1]*phi2 + a[i][2]*phi3 + a[i][3]*phi4 + a[i][4]*phi5 + \
                          a[i][5]*phi6 + a[i][6]*phi7 + a[i][7]*phi8 + a[i][8]*phi9 + \
                          a[i][9]*lm + a[i][10]*ls + a[i][11]*f + a[i][12]*d + a[i][13]*w)
        dpsi+= (a[i][14] + a[i][15]*t)*math.sin(arg) + (a[i][16])*math.cos(arg)
        deps+= (a[i][17] + a[i][18]*t)*math.cos(arg) + (a[i][19])*math.sin(arg)

    return [degree_to_radian(dpsi/3.6e3), degree_to_radian(deps/3.6e3), w]

def nutation_equatorial(jd, x):
    [dpsi, deps, w] = nutation_parameters_2000(jd)
    epsm = mean_obliquity (jd)
    eps = epsm + deps
    xi = rotation (1, epsm, x)
    xj = rotation (3, -dpsi, xi)
    x1 = rotation (1, -eps, xj)
    return x1, dpsi, deps, epsm, w

def nutation(jdate, coordPrec):
    x_nut_equ, dpsi, deps, epsm, w = nutation_equatorial(jdate, [coordPrec['x'], coordPrec['y'], coordPrec['z']])
    dec, ar, r = rectangular_to_spherical (x_nut_equ)  
    return {'x': x_nut_equ[0], 'y': x_nut_equ[1], 'z': x_nut_equ[2], 'ar': scale_angle(ar), 'dec': scale_angle(dec),'dpsi': dpsi, 'deps': deps, 'epsm': epsm, 'w': w} 


def nutation_list(jdate, coordPrec):
    x_nut_equ, dpsi, deps, epsm, w = nutation_equatorial(jdate, [coordPrec['x'], coordPrec['y'], coordPrec['z']])
    return [x_nut_equ[0], x_nut_equ[1], x_nut_equ[2], dpsi, deps, epsm, w]  

def equation_of_equinoxes (jd):
    [dpsi, deps, w] = nutation_parameters_2000 (jd)
    epsm = mean_obliquity (jd)
    T = (jd - 2451545) / 36525
    omega_deg  = 125.045 - 1934.136*T
    omega  = degree_to_radian(omega_deg)

    ee = dpsi * math.cos(epsm) + \
          degree_to_radian(0.00264/3600) * math.sin (omega) + \
          degree_to_radian(0.000063/3600) * math.sin(2*omega)
    return ee



# #######################################################################
# ###    ANNUAL ABERRATION  ##############################################
# #######################################################################

def annual_aberration(date, ar, dec):
    years = (date - 2451545.0) / 36525
    lambda_s = degree_to_radian(280.466) + degree_to_radian(36000.770) * years     #  longitud eclíptica verdadera geométrica del Sol
    lambda_s = lambda_s - math.floor(lambda_s / (2 * math.pi)) * 2 * math.pi
    epsilon_m = degree_to_radian(23.439) - degree_to_radian(0.013) * years         #  oblicuidad media de la eclíptica
    omega_bar = degree_to_radian(282.938) + degree_to_radian(0.323) * years        #  longitud del perigeo del Sol
    paramA = degree_to_radian(20.490 / 3600) * (math.sin(lambda_s) * math.sin(ar) + math.cos(lambda_s) * math.cos(ar) * math.cos(epsilon_m))
    paramA_e = degree_to_radian(0.343 / 3600) * (math.sin(omega_bar) * math.sin(ar) + math.cos(omega_bar) * math.cos(ar) * math.cos(epsilon_m))
    paramD = degree_to_radian(20.490 / 3600) * (math.sin(dec) * math.cos(ar) * math.sin(lambda_s) +
                          math.cos(lambda_s) * ( math.sin(epsilon_m) * math.cos(dec) - math.cos(epsilon_m) * math.sin(dec) * math.sin(ar) ))
    paramD_e = degree_to_radian(0.343 / 3600) * (math.sin(dec) * math.cos(ar) * math.sin(omega_bar) +
                          math.cos(omega_bar) * ( math.sin(epsilon_m) * math.cos(dec) - math.cos(epsilon_m) * math.sin(dec) * math.sin(ar) ))
    ar_app = ar - (paramA + paramA_e) /  math.cos(dec)
    dec_app= dec - (paramD + paramD_e)
    return [ar_app, dec_app, lambda_s, epsilon_m, omega_bar] 

def aberration(coordNut, jdate):
    dec, ar, r = rectangular_to_spherical ([coordNut['x'], coordNut['y'], coordNut['z']])

    coord_ang = annual_aberration(jdate,  ar, dec)
    coord_rect = spherical_to_rectangular(coord_ang[1], coord_ang[0], r)
    coordAberr = { 'x': coord_rect[0], 'y': coord_rect[1], 'z': coord_rect[2], 'ar': scale_angle(coord_ang[0]), 'dec': scale_angle(coord_ang[1]), 'lambda_s': scale_angle(coord_ang[2]), 'epsilon_m': scale_angle(coord_ang[3]), 'omega_bar': scale_angle(coord_ang[4])}

    return coordAberr 

# #######################################################################
# ###   REFRACTION  #####################################################
# #######################################################################

def decorated_ddmmss_to_ddmmss_compact(a):  # misma que anterior, pero en formato compacto
    s = -1 if a[0] == '-' else 1
    a0 = a[1:]
    [dd, a1] = a0.split('°') 
    [mm, a2] = a1.split("'")
    [ss, a3] = a2.split('"')
    compact = s * (int(dd) + (int(mm)/100) + int(float(ss))/10000)
    return ddmmss_compact_to_degree(compact)  

def convert_params(date, lon_dms, lat_dms):
    spl = date.replace('-', ' ').replace(':', ' ').replace('T', ' ').split(' ')
    jdate = julian_date(int(spl[0]), int(spl[1]), int(spl[2]), int(spl[3]), int(spl[4]), int(spl[5]))
    lon_dms = '+' + lon_dms[:-1]   if lon_dms[-1] == 'E' else  '-' + lon_dms[:-1]   
    lat_dms = '+' + lat_dms[:-1]   if lat_dms[-1] == 'N' else  '-' + lat_dms[:-1]
    lon_degree = decorated_ddmmss_to_ddmmss_compact(lon_dms)   
    lat_degree = decorated_ddmmss_to_ddmmss_compact(lat_dms)
    return (jdate, lon_degree, lat_degree)  

def greenwich_mean_sidereal_time (jd): 
    T = (jd - 2451545) / 36525
    # Mean Sideral Time at Greenwich at 0h UT - Meeus 11.4
    st0_deg = 280.46061837 + 360.98564736629*(jd-2451545.0) + T*T*0.000387933 - T*T*T/38710000;
    st0_rad = degree_to_radian(st0_deg)
    st0_rad = scale_angle(st0_rad)
    st0_hour = radian_to_degree(st0_rad) / 24
    return st0_hour

def local_sideral_time (lon, jd): 
    gmst_rad = greenwich_mean_sidereal_time (jd)
    gmst_hor = degree_to_hour(radian_to_degree(gmst_rad))
    lon_hour = degree_to_hour(lon)
    lst_hour = gmst_hor + lon_hour
    return lst_hour

def equatorial_to_horizontal (jd, lon, lat, x):
    lst_hour = local_sideral_time (radian_to_degree(lon), jd)
    lst = hour_to_radian(lst_hour)
    r1 = rotation (3, lst, x)
    r2 = rotation (2, math.pi/2 - lat, r1)
    r2 = [-r2[0], r2[1], r2[2]]  # Cambiar el signo de x para que coincida con la convención de coordenadas
    return r2

def horizontal_to_equatorial (jd, lon, lat, x):
    lst_hour = local_sideral_time (radian_to_degree(lon), jd)
    lst = hour_to_radian(lst_hour)
    x = [-x[0], x[1], x[2]]  # Cambiar el signo de x para que coincida con la convención de coordenadas
    r1 = rotation (2, -(math.pi/2 - lat), x)
    r2 = rotation (3, -lst, r1)
    return r2

def refraction(date, lon_dms, lat_dms, temp, press, coord):
    [jd, lon, lat]= convert_params(date, lon_dms, lat_dms)
    coordHoriz_x = equatorial_to_horizontal (jd, degree_to_radian(lon), degree_to_radian(lat), [coord['x'], coord['y'], coord['z']])
    [alt_r, az, r] = rectangular_to_spherical(coordHoriz_x)
    alt = radian_to_degree(alt_r)
   
    R = (0.283 * press) / ((temp + 273) * math.tan(degree_to_radian(alt + 7.31 /(alt + 4.4))))    # 
    R = 60 * (0.283 * press) / (temp + 273) * 1.02 / math.tan(degree_to_radian(alt + 10.3 / (alt + 5.11)))   # en minutos de arco

    alt = alt + R / 3600  # en grados

    new_alt_r = degree_to_radian(alt)
    topo_Refrac = spherical_to_rectangular(new_alt_r, az, r)
    coord_rect = horizontal_to_equatorial(jd, degree_to_radian(lon), degree_to_radian(lat), topo_Refrac)

    dec, ar, r = rectangular_to_spherical (coord_rect)
    coordRef = { 'x': coord_rect[0], 'y': coord_rect[1], 'z': coord_rect[2], 'ar': scale_angle(ar), 'dec': scale_angle(dec), 'R': R, 'alt': alt }
    return(coordRef)


def calculate(star, date, jdate, lon_dms, lat_dms, temp, press):
    result = {}
    ###  CATALOG ###################################
    dataSimbad = getSimbad_mod(star)
    result['simbad'] = dataSimbad

    ###  PROPER MOTION ###################################
    coordPM = properMotion(date, dataSimbad)
    result ['proper motion']= coordPM

    ###  PRECESSION ###################################
    coordPrec = precession(jdate, coordPM['ar'], coordPM['dec'])
    result ['precession']= coordPrec

    ###  NUTATION ###################################
    coordNut = nutation(jdate, coordPrec)
    result ['nutation']= coordNut

    ###  ABERRATION ###################################
    coordAberr = aberration(coordNut, jdate) 
    result ['aberration']= coordAberr

    ####  REFRACCIÓN ATMOSFÉRICA ######################
    coordRefrac = refraction(date, lon_dms, lat_dms, temp, press, coordAberr)
    result ['refraction']= coordRefrac

    return result

