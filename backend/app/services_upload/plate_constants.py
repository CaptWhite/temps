import numpy as np
import pandas as pd

def calculate(ar, dec, x, y):
  X2 = x*x
  XY = x*y
  Y2 = y*y
  X = x
  Y = y
  ind = np.ones(x.size) 
 
  # Creamos la matriz de diseño X
  MX = np.column_stack((X2, Y2, XY, X, Y, ind))

  # Calculamos los coeficientes usando la fórmula de mínimos cuadrados
  a_est_AR = np.linalg.inv(MX.T @ MX) @ MX.T @ ar
  a_est_DEC = np.linalg.inv(MX.T @ MX) @ MX.T @ dec

  return [a_est_AR, a_est_DEC] 


def calculate_plate(df):
  # Obtener un array de una columna
  arr_ar = df['ar_app'].to_numpy()
  arr_dec = df['dec_app'].to_numpy()
  arr_x = df['field_x'].to_numpy()
  arr_y = df['field_y'].to_numpy()
  [pc_ar, pc_dec] = calculate(arr_ar, arr_dec, arr_x, arr_y)
  coefs_name = ['X²', 'Y²', 'XY', 'X', 'Y', 'ind'] 
  coefs = pd.DataFrame({
    'Coef': coefs_name,
    'AR': pc_ar,
    'DEC': pc_dec
})
  
  def calculate_residues(ra, dec, x, y, pc_ar, pc_dec):
    ar_res = ra - ((pc_ar[0] * x * x) + (pc_ar[1] * y * y) + (pc_ar[2] * x * y  ) + (pc_ar[3] * x) + (pc_ar[4] * y) + pc_ar[5]) 
    dec_res = dec - ((pc_dec[0] * x * x) + (pc_dec[1] * y * y) + (pc_dec[2] * x * y  ) + (pc_dec[3] * x) + (pc_dec[4] * y) + pc_dec[5])

    return [ar_res, dec_res] 
    


  df[['ra_resid', 'dec_resid']] = df.apply(lambda row: calculate_residues(row['ar_app'], row['dec_app'], row['field_x'], row['field_y'], pc_ar, pc_dec), axis=1, result_type='expand')

  return df, coefs
  # Opción recomendada
# También puedes usar:
# array_columna1 = df['columna1'].values

''' 
MY_AR = np.array([
3.30579905,3.30464277,3.30201750,3.30130482,3.30191569,3.30132664,3.30098485,3.30102121,3.30049761,3.29994492,3.29894863,3.29870138,3.29478893,3.29390172,3.29295633,3.29284725,3.29377809,3.29241092,3.29065832,3.29051287
])
MY_DEC = np.array([0.22112497,0.22660676,0.23162846,0.23156495,0.22200685,0.22528710,0.22591009,0.22269529,0.22410464,0.22733253,0.23007221,0.22139211,0.22582718,0.22322519,0.22762875,0.22626691,0.21745590,0.21895010,0.22962909,0.21965066
])
x = np.array([-1211,-1139,-835,-722,-631,-604,-564,-505,-453,-430,-331,-124,393,579,640,683,712,897,956,1177])
y = np.array([-543,343,1186,1190,-332,197,302,-207,26,544,999,-367,405,12,727,515,-899,-631,1089,-488])

[a_est_AR, a_est_DEC] = calculate(MY_AR, MY_DEC, x, y)

print("Coeficientes estimados AR :", a_est_AR)
print("Coeficientes estimados DEC :", a_est_DEC)
'''