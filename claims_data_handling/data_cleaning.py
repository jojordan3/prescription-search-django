import pandas as pd
import numpy as np
import re
from . import feature_engineering as fe
from supplementary_data import brand_generic_mapping


def get_data(paths, sep_char='|', nan_values=None):
    '''Get data from files, using valid filepath strings. Put data into a
    pandas dataframe, eliminating unnecessary
    '''
    df_list = []
    for path in paths:
        df = pd.read_csv(path, sep=sep_char, dtype=str,
                         na_values=['nan', 'NaN', r'\s*'].extend(nan_values),
                         usecols=['PBMVendor', 'ClaimStatus', 'Quantity',
                                  'IngredientCost', 'DispensingFee', 'Copay',
                                  'CoInsurance', 'Deductible', 'OutOfPocket',
                                  'PaidAmount', 'PharmacyNumber',
                                  'PharmacyTaxId', 'PharmacyNPI',
                                  'PharmacyName', 'PharmacyStreetAddress1',
                                  'PharmacyCity', 'PharmacyState',
                                  'PharmacyZip', 'MailOrderPharmacy',
                                  'DrugLabelName'])

        df = df[df.ClaimStatus == 'P'].drop(columns=['ClaimStatus']).\
            dropna(subset=['DrugLabelName'])
        for column in df.columns:
            if column == 'DrugLabelName':
                df[column] = df[column].apply(lambda name: name.lower())
            df[column] = df[column].apply(lambda value: _rid_whitespace(value))
        df_list.append(df)
    claims = pd.concat(df_list, ignore_index=True)


def _rid_whitespace(value):
    elipsis = re.search('...', value)
    if value:
        if elipsis:
            value = value[:elipsis.start()] + value[elipsis.end():]
        return (' '.join(value.strip().split()))
    else:
        return ''


def engineer_features(df):
    df['TotalCost'] = df.apply(lambda row: fe.get_total(row), axis=1)
    df = df[df.TotalCost > 0]
    df['UnitCost'] = df.apply(lambda row: fe.get_unit_cost(row), axis=1)
    df['PharmacyZip'] = df.apply(lambda row: fe.get_zip_mail_order(row),
                                 axis=1)
    df = fe.fill_pharm_info(df)
    return df


def drop_final(df):
    df = df.drop(columns=['CoInsurance', 'Deductible', 'DispensingFee',
                          'IngredientCost', 'MailOrderPharmacy', 'OutOfPocket',
                          'PaidAmount', 'PaidOrAdjudicatedDate', 'PharmacyNPI',
                          'PharmacyNumber', 'PharmacyState', 'PharmacyTaxId',
                          'Quantity', 'TotalCost'])
