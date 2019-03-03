import pandas as pd
import numpy as np
import re
from . import feature_engineering as fe
from supplementary_data import brand_generic_mapping


def engineer_features(df):
    df['UnitCost'] = df.apply(lambda row: fe.get_unit_cost(row), axis=1)
    df = df[df.UnitCost > 0]
    df.drop(columns=['IngredientCost', 'DispensingFee', 'OutOfPocket',
                     'PaidAmount', 'Quantity'])
    df['PharmacyName'] = df.PharmacyName.apply(lambda x: fe.fix_pharm_name(x))
    df['PharmacyStreetAddress1'] = df.PharmacyStreetAddress1.apply(
        lambda x: standardize_address(x))
    df['PharmacyZip'] = df.PharmacyZip.apply(lambda x: standard_zip(x))
    df = fe.fill_pharm_info(df)
    return df
