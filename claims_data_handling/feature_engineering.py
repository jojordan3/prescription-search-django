import numpy as np


def get_total(row):
    '''This function calculates a total cost out of the available columns
    relating to cost. There are two unique measurements to get the total cost,
    and completeness of the necessary fields varies widely across files.
    '''
    if row['IngredientCost'] and row['DispensingFee']:
        cost1 = float(row['IngredientCost']) + float(row['DispensingFee'])
    elif row['IngredientCost']:
        cost1 = float(row['IngredientCost'])
    else:
        cost1 = 0

    cost2 = float(row['OutOfPocket']) + float(row['PaidAmount'])

    return max(cost1, cost2)


def get_unit_cost(row):
    '''This function calculates the unit cost (price per pill, etc.) for the
    claim using the TotalCost and the Quantity provided.
    '''
    if float(row['Quantity']) > 0:
        return float(row['TotalCost'])/float(row['Quantity'])
    else:
        return row['TotalCost']


def standard_zip(value):
    '''A safety for if the zipcodes were read in as ints and thus leading
    zeroes were dropped.
    '''
    value = str(value)
    value_len = len(value)
    if value_len > 5:
        return value[:5]
    elif value_len == 5:
        return value
    else:
        while value_len < 5:
            value = '0' + value
        return value


def get_zip_mail_order(row):
    '''This function sets all the zipcodes for mail order pharmacies to 'XXXXX'
    to consolidate information from two fields into one.
    '''
    if row['MailOrderPharmacy'] == 'Y':
        return 'XXXXX'
    else:
        zipcode = str(row['PharmacyZip'])
        if zipcode == 'np.nan' or zipcode == 'nan':
            return np.nan
        else:
            zipcode = standard_zip(zipcode)
            return zipcode


def standardize_address(address):
    '''Standardize addresses so the same address matches even if originally
    entered using different abbreviations.
    '''
    abbreviations = [['BRDWAY', 'BROADWAY'], ['BWAY', 'BROADWAY'],
                     ['AVENUE', 'AVE'], ['BOULEVARD', 'BLVD'], ['ROAD', 'RD'],
                     ['TRAC', 'TRACE'], ['HIGHWAY', 'HWY'], ['STREET', 'ST'],
                     ['PARKWAY', 'PKWY'], ['PLZ', 'PLAZA'], ['TRL', 'TRAIL']]
    for abbreviation in abbreviations:
        address.replace(abbreviation[0], abbreviation[1], regex=True,
                        inplace=True)


def fill_pharm_info(row):
    '''Use information from all pharmacy-related features to fill in possible
    missing information, standardize information, and identify pharmacies
    under disparate names.
    '''