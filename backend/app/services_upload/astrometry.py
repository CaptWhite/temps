import time
import requests
import json
import os
from dotenv import load_dotenv

from app.services_upload.fits_to_df import convert_to_df

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')

uploaded = { 'albireo.jpg' : 10943014,
             'TX-Cyg.png'  : 11099168,
             'ngc253.png'  : 11099256,
             'NGC 7331.jpg': 11109177,
             'T-CrB.jpg'   : 11109188,
             'Ursa Minor.png': 11127659,
             'foto_jose.jpg': 11259582,
             'ngc6888.png': 11281048,
             'pleyades.jpg': 11370410,
             'casiopea.jpg': 11370440,
             'TSE2024-stack_HDR_4376_81_div_gauss_final_sig4-v2-no-moon-l-8june2024.jpg': 12555297,
             'LIGHT_2025-02-26_20-10-15_L_1x1_-10.00_3.00s_0000.png':  12554910             
}

def login():
    url = API_URL + 'login'
    data = {'request-json': json.dumps({'apikey': API_KEY})}
    response = requests.post(url, data=data)
    result = response.json()
    if result['status'] == 'success':
        return result['session']
    else:
        raise Exception('Error al hacer login: ' + result.get('errormessage', ''))

def upload_image(session, filename, image):   
    #filename = os.path.basename(image)
    if filename in uploaded:
        return uploaded[filename]

    url = API_URL + 'upload'
    files = {'file': image}
    data = {'request-json': json.dumps({'session': session})}
    response = requests.post(url, files=files, data=data)
    result = response.json()
    if result['status'] == 'success':
        return result['subid']
    else:
        raise Exception('Error al subir la imagen: ' + result.get('errormessage', ''))

def solve_astrometry(subid):
    url = API_URL + f'submissions/{subid}'
    count = 0

    while True: 
        if (count > 200):
            raise Exception('Error al enviar el trabajo: ' + result.get('errormessage', ''))
        response = requests.get(url)
        result = response.json()
        count += 1
        if (len(result['jobs'])) < 1:
            print (f'Job has not started - {time.ctime()}')
            time.sleep(10)
        elif (len(result['job_calibrations']) < 1):
            print ('Job has not finished')
            time.sleep(5)
        else:
            return result['jobs'][0]

def check_job_status(jobid):
    url = API_URL + 'jobs/' + str(jobid)
    response = requests.get(url)
    result = response.json()
    status = result['status']
    if (status != 'success'):
        raise Exception('Error al procesar el trabajo: ' + result.get('errormessage', ''))
    return result['status']

def download_corr(jobid): # , filename):
    headers = { 'Content-Type': 'application/json' }
    params = { "apikey": API_KEY }
    cwd = os.getcwd()
    # outfile = cwd + filename[1:]
    url = f'https://nova.astrometry.net/corr_file/{jobid}'
    try:
        respuesta = requests.get(url, params=params, headers=headers, stream=True)
        if respuesta.status_code == 200:  # Verifica que la solicitud sea exitosa
          # Guarda el contenido de la imagen en una variable
          return respuesta.content
        else:
            print(f"Error al obtener la imagen. Código de estado: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
      raise SystemExit(f"Error al descargar el fichero 'corr': {e}")

def director(filename, filebytes):
    try:
      # Paso 0: Login
      session = login()
      print ({'session': session})

      # Paso 1: Subir la imagen
      subid = upload_image(session, filename, filebytes)
      print ({'subid': subid})

    # Paso 2: Enviar el trabajo de astrometría
      jobid = solve_astrometry(subid)
      print ({'jobid': jobid})

      # Paso 3: Verificar el estado del trabajo
      status = check_job_status(jobid)
      print ({'status': status})

      # Paso 4: Obtener fichero CORR
      fits_content = download_corr(jobid)
      df = convert_to_df(fits_content)

      return df  

    except Exception as e:
      print(f"Ocurrió un error en Astrometry: {e}")
########################################################################
########################################################################

def main():
    image = 'ngc253.png'
    image_name, image_extension = os.path.splitext(image)
    image_path = f'.\\auxiliar\\{image}'  # Reemplaza con la ruta a tu imagen
    fileCorr =   f'.\\auxiliar\\{image_name}.corr.fits'
    files = {'file': open(image_path, 'rb')}

    try:
        # Paso 0: Login
        session = login()
        print ({'session': session})

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == '__main__':
    main()
