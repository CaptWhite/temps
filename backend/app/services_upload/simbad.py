import pandas as pd
from astroquery.simbad import Simbad

## Obtener con Simbad el nombre y parámetros de las estrellas
def get_simbad_df(df):
  if 'ref_id' in df.columns:
    df['ref_id'] = 'Gaia DR2 ' + df['ref_id'].astype(str)

  # Recorrer fila por fila usando iloc
  list_star = []
  for i in range(len(df)):
    if True:
      row = df.iloc[i]
      query = f"SELECT TOP 1 '{int(row.field_id)}' as id, main_id, ra, dec, pmra, pmdec, plx_value, rvz_radvel, DISTANCE(POINT('ICRS', ra, dec), POINT('ICRS', {row.field_ra}, {row.field_dec})) AS dist FROM basic WHERE CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', {row.field_ra}, {row.field_dec}, 0.01)) = 1 ORDER BY dist ASC"
      result = Simbad.query_tap(query)
      df_simbad = result.to_pandas()
      if not df_simbad.empty:
        star = df_simbad.to_numpy().tolist()[0]
        star = list(map(lambda field: 0 if pd.isnull(field) else field, star))
        list_star.append(star)

  columns = ['id', 'main_id', 'ra', 'dec', 'pmra_x', 'pmdec_x', 'plx_value', 'rvz_radvel', 'dist']  
  df_simbad = pd.DataFrame(list_star, columns = columns)
  df_simbad['id'] = df_simbad['id'].astype(int)


  # Realizar un LEFT JOIN en el campo 'id'
  stars = pd.merge(df_simbad, df, left_on='id', right_on='field_id', how='left')
  stars.columns

  #### Borrar columna de la fusion de los dos dataframes
  if 'ref_id' not in stars.columns:
    items = [ 'index_x',	'index_y',	'index_ra',	'index_dec', 'match_weight', 'MAG_BT', 'MAG_VT', 'MAG_HP', 'MAG', 'FLUX', 'BACKGROUND']
  else:
    items = ['index_x',	'index_y',	'index_ra',	'index_dec', 'match_weight',	'ra_ref',	'dec_ref',	'mag',	'ref_cat', 'pmra',	'pmdec',	'parallax',	'ra_ivar',	'dec_ivar',	'pmra_ivar',	'pmdec_ivar', 'parallax_ivar',	'phot_bp_mean_mag',	'phot_rp_mean_mag',	'FLUX',	'BACKGROUND', 'ref_id']
  
  for item in items:
    stars = stars.drop(item, axis=1) 

  # stars.to_csv('stars.csv', index=False) 
  return stars

def get_simbad_star(star):

  # Recorrer fila por fila usando iloc
  list_star = []

  query = f"""SELECT b.main_id, b.ra, b.dec, b.pmra, b.pmdec, b.plx_value, b.rvz_radvel FROM basic AS b JOIN ident AS i ON b.oid = i.oidref WHERE i.id = '{star}'"""

  result = Simbad.query_tap(query)
  print('A')
  df_simbad = result.to_pandas()
  print('B')
  return df_simbad