import sqlite3
import pandas as pd
import numpy as np
import re
from . import feature_engineering as fe
from supplementary_data import brand_generic_mapping


# Columns of interest -- not all appear in every file
column_names = [
    'PBMVendor', 'ClaimStatus', 'Quantity', 'IngredientCost', 'DispensingFee',
    'CoInsurance', 'Deductible', 'OutOfPocket', 'PaidAmount', 'PharmacyName',
    'DrugLabelName', 'PharmacyNumber', 'PharmacyTaxId', 'PharmacyNPI', 'Copay',
    'PharmacyStreetAddress1', 'PharmacyCity', 'PharmacyState', 'PharmacyZip',
    'MailOrderPharmacy']


def get_data(path, sep_char='|', nan_values=None):
    '''Get data from files, using valid filepath strings. Put data into a
    pandas dataframe, eliminating unnecessary
    '''

    if path[-4:] == '.csv':
        claims = _make_df(path, sep_char='|', nan_values=None)

    else:
        df_list = []
        for filename in os.listdir(path):
            if filename[-4:] == '.csv':
                fullpath = os.path.join(path, filename)
                df = _make_df(fullpath, sep_char='|', nan_values=None)
        df_list.append(df)

        claims = pd.concat(df_list, sort=True, ignore_index=True)

    claims = claims[claims.ClaimStatus == 'P'].drop(
        columns=['ClaimStatus']).dropna(subset=['DrugLabelName'])
    for column in claims.columns:
        if column == 'DrugLabelName':
            claims[column] = claims[column].apply(lambda name: name.lower())
        claims[column] = claims[column].apply(
            lambda value: value.replace(
                '...', '').strip() if isinstance(value, str) else value)

    claims = engineer_features(claims)

    return claims


def _make_df(filepath, sep_char='|', nan_values=None):
    '''Read in the first line of the file to determine schema of this
    particular file. Then continue to build the dataframe from the csv.'''
    with open(path) as data:
        header = data.readline()
    columns = [col for col in column_names if col in header]

    df = pd.read_csv(path, sep=sep_char, usecols=columns, dtype=str,
                     na_values=['nan', 'NaN', r'\s*', ''].extend(nan_values))
    for col in list(set(column_names) - set(columns)):
        df[col] = [np.nan] * len(df)

    return df
