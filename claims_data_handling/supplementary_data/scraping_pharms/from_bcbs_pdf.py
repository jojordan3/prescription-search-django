'''
Gets pharmacy information from Blue Cross Blue Shield https://www.bcbsri.com
'''
from tabula import read_pdf
import sys
import os
import pandas as pd

# Includes Washington DC, Puerto Rico, and Virgin Islands
# Orig taken from
# https://gist.github.com/bubblerun/a624de5b4fa8ff0980010054a7220977
states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
          'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
          'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
          'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN',
          'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY']

obj_length = len(states)  # For progress bar

# Link to PDF files - state abbreviation replaces @@
l = f'https://www.bcbsri.com/BCBSRIWeb/pdf/state_pharmacies/@@_PHARMACIES.pdf'

dir_path = os.path.dirname(os.path.abspath(__file__))  # Directory path to save

# For pandas df
option = {'names': ['PharmacyNumber', 'PharmacyNPI', 'PharmacyName',
                    'PharmacyStreetAddress1', 'PharmacyCity', 'PharmacyState',
                    'PharmacyZip', 'other1', 'other2'],
          'header': None, 'dtype': str, 'index_col': False}


def progressbar(i, current):
    '''Simple progress bar'''
    width = 55
    if i == 0:
        sys.stdout.write(f"Progress: [>{' ' * (width - 1)}] 0.0%")
        sys.stdout.flush()
        sys.stdout.write('\b' * 4)
    else:
        progress = int(width * i / obj_length)
        percent = i * 100 / obj_length
        if progress > current:
            sys.stdout.write('\r')
            sys.stdout.write(f"Progress: \
[{'=' * progress}>{' ' * (width - progress - 1)}] {percent:.1f}%")
            sys.stdout.flush()
        else:
            sys.stdout.write(f'{percent:.1f}%')
            sys.stdout.flush()
        sys.stdout.write('\b' * len(f'{percent:.1f}%'))
    i += 1
    progress = current
    return i, progress


def get_bcbs_info(save_to_path):
    '''Get data from all stated covered by BlueCross BlueShield'''
    pharmacies = []

    i = 0
    progress = 0
    obj_length = len(states)

    for state in states[0:1]:
        i, progress = progressbar(i, progress)
        df = read_pdf(l.replace('@@', state), pandas_options=option)
        df = df.drop(columns=['other1', 'other2'])
        pharmacies.append(df)

    bcbs_pharms = pd.concat(pharmacies, ignore_index=True)
    bcbs_pharms.to_csv(save_to_path)
    print('File saved to :' + save_to_path)


if __name__ == "__main__":
    get_bcbs_info(dir_path + '/bcbspharms.csv')
