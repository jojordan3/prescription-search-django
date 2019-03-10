import pandas as pd
import psycopg2
from private import user, password

path_to_zips = '/Users/joannejordan/Desktop/GitHub/prescription-search-django/\
claims_data_handling/supplementary_data/uszips.csv'


def get_zipcodes():
    datatypes = {'zip': 'str', 'lat': 'float64', 'lng': 'float64'}

    zip_code_info = pd.read_csv(path_to_zips, encoding="ISO-8859-1",
                                usecols=['zip', 'lat', 'lng'],
                                dtype=datatypes)

    zip_code_info.columns = ['zipcode', 'latitude', 'longitude']
    zip_code_info = zip_code_info.dropna()
    return zip_code_info

if __name__ == "__main__":
    conn = psycopg2.connect(database='rxdatabase', user=user,
                            password=password, host='localhost')
    cur = conn.cursor()
    zips = get_zipcodes()
    zipText = ','.join(
        cur.mogrify('(%s, %s, %s)', zips.loc[i].values).decode("utf-8")
        for i in zips.index)

    cur.execute(
        """INSERT INTO rx_info_zipcodeinfo (zipcode, latitude, longitude)
        VALUES """ + zipText
        )
    conn.commit()
    cur.close()
    conn.close()
    print('ZipCodeInfo table populated successfully!')
