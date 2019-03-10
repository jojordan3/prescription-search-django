import pandas as pd
import psycopg2
from private import user, password
from numpy import isnan
import re

path_to_meds = '/Users/joannejordan/Desktop/GitHub/prescription-search-django/\
claims_data_handling/supplementary_data/product.txt'


def rid_whitespace(name):
    name = name.replace('...', '')
    name = ' '.join(name.split())
    return name


def get_generic(meds_data):
    meds = []
    for med in meds_data:
        if isinstance(med[0], str):
            brand = rid_whitespace(med[0])
            if isinstance(med[1], str):
                suffix = rid_whitespace(med[1])
                brand_ = ' '.join([brand.lower(), suffix.lower()])
            else:
                brand_ = brand.lower()
        else:
            continue

        if isinstance(med[2], str):
            generic_ = med[2].lower()
        else:
            continue

        if brand_ != generic_:
            mapping = (brand_, generic_)
            if mapping not in meds:
                meds.append(mapping)
    return meds


if __name__ == "__main__":
    conn = psycopg2.connect(database='rxdatabase', user=user,
                            password=password, host='localhost')
    cur = conn.cursor()

    ndc_product = pd.read_csv(path_to_meds, sep='\t',
                              usecols=['PROPRIETARYNAME',
                                       'PROPRIETARYNAMESUFFIX',
                                       'NONPROPRIETARYNAME'])
    generic_mapping = get_generic(ndc_product.values)

    medsText = ','.join(cur.mogrify('(%s, %s)', med).decode("utf-8")
                        for med in generic_mapping)

    cur.execute(
        'INSERT INTO rx_info_brandtogeneric ("Brand", "Generic") VALUES ' +
        medsText)
    conn.commit()
    cur.close()
    conn.close()
    print('BrandToGeneric table populated successfully!')
