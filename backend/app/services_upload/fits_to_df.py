from astropy.io import fits
from astropy.table import Table
import io


def convert_to_df(fits_content): 
  HDUList = fits.open(io.BytesIO(fits_content))
  astropy_table = Table(HDUList[1].data)
  df = astropy_table.to_pandas()
  return df