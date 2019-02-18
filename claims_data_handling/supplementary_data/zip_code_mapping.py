import pandas as pd
import numpy as np


datatypes = {'zip': 'str', 'lat': 'np.float64', 'long': 'np.float4',
             'city': 'str', 'county_name': 'str'}

zip_code_info = pd.read_csv('. product.txt', encoding="ISO-8859-1",
                            usecols=['zip', 'lat', 'long'],
                            dtype=datatypes)

zip_code_info.columns = ['zipcode', 'latitude', 'longitude']

if if __name__ == "__main__":
    pass