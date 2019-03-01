import numpy as np


def get_unit_cost(row):
    '''This function calculates a the unit cost by first calculating the
    total cost out of the available columns relating to cost. There are
    two unique measurements to get the total cost, and completeness of
    the necessary fields varies widely across files.

    The function then divides the total cost by the Quantity.
    '''
    if row['IngredientCost'] and row['DispensingFee']:
        cost1 = float(row['IngredientCost']) + float(row['DispensingFee'])
    elif row['IngredientCost']:
        cost1 = float(row['IngredientCost'])
    else:
        cost1 = 0

    cost2 = float(row['OutOfPocket']) + float(row['PaidAmount'])
    
    if float(row['Quantity']) > 0:
        return max(cost1, cost2)/float(row['Quantity'])
    else:
        return max(cost1, cost2)


def standard_zip(value):
    '''A safety for if the zipcodes were read in as ints and thus leading
    zeroes were dropped.
    '''
    if isinstance(value, str):
        value_len = len(value)
        if value_len > 5:
            return value[:5]
        elif value_len == 5:
            return value
        else:
            while len(value) < 5:
                value = '0' + value
    return value


def standardize_address(address):
    '''Standardize addresses so the same address matches even if originally
    entered using different abbreviations.
    '''
    if isinstance(address, str):
        abbreviations = [['BRDWAY', 'BROADWAY'], ['BWAY', 'BROADWAY'],
                         ['AVENUE', 'AVE'], ['BOULEVARD', 'BLVD'], ['ROAD', 'RD'],
                         ['TRAC', 'TRACE'], ['HIGHWAY', 'HWY'], ['STREET', 'ST'],
                         ['PARKWAY', 'PKWY'], ['PLZ', 'PLAZA'], ['TRL', 'TRAIL'],
                         ['SQUARE', 'SQ'], ['RTE', 'RT'], ['ROUTE', 'RT'],
                         ['DRIVE', 'DR'], ['EAST', 'E'], ['WEST', 'W'],
                         ['NORTH', 'N'], ['SOUTH', 'S'], ['/', ' '],
                         ['FREDRICK', 'FREDERICK'], [' CALEF', ' CALIFORNIA'],
                         ['CIRCLE', 'CIR'], ['STE', 'SUITE']]
        address = re.sub(r'[#\.,\-/\']', '', address)
        for abbreviation in abbreviations:
            if isinstance(address, str):
                address = address.replace(abbreviation[0], abbreviation[1])
        if address == '' or address == r'[\s*]':
            address = np.nan
        else:
            addresss = ' '.join(address.split())
    return address


def fix_pharm_name(name):
    '''Standardize Pharmacy Names'''
    if isinstance(name, str):
        if ('ORCHARD PHARMACEUTICALS' in name) or ('ORCHARD SPECIALTY' in name):
            return 'ENVISIONRX.COM'
        if 'ENVISION' in name:
            return 'ENVISIONRX.COM'
        if ('CURASCRIPT' in name) or ('ACCREDO' in name):
            return 'ACCREDO.COM'
        if ('CVS' in name) or ('TARGET' in name) or ('CAREMARK' in name):
            return 'CVS PHARMACY'
        if name.startswith('A '):
            name = name[2:]
        if ('FRONSKE' in name) or ('NAU CAMPUS' in name):
            return 'NORTH AZ UNIV FRONSKE HEALTH SERVICES'
        if 'WEGMANS' in name:
            return 'WEGMANS PHARMACY'
        name = re.sub(r'[\.,\-/\'#]', '', name)
        name = re.sub(r'[0-9]+', '', name)
        concatd = [[' COMP', ' CO'], ['SOLUTIO', 'SOLUTIONS'],
                   ['EMPLOYE', 'EMPLOYEE'], [' SUB', ' SUBWAY'],
                   [' SP', '']]
        for cutoff in concatd:
            if name.endswith(cutoff[0]):
                name = name[:-len(cutoff[0])] + cutoff[1]
        pairs = [['TARGET', 'CVS'], ['WAL-MART', 'WALMART'], ['INC', ''],
                 ['HEALTHGROUP', 'HEALTH GROUP'], ['GRP', 'GROUP'],
                 ['PHARMACIES', 'PHARMACY'], ['SERVICES', ''],
                 ['SERVICE', ''], ['SPECIALTY', ''],
                 ['PHCY', 'PHARMACY'], ['&', 'AND'], ['COMPANY', 'CO'],
                 ['LLC', ''], [' LL', ''], ['PHARMACY', ' PHARMACY '],
                 ['DRUGS', ' DRUGS '], ['K MART', 'KMART'],
                 ['UNIV', 'UNIVERSITY'], ['HLTH', 'HEALTH'],
                 ['SRVCES', 'SERVICES'], ['HELTH', 'HEALTH'],
                 ['SVCS', 'SERVICES'], [' OF ', '']]
        for pair in pairs:
            name = name.replace(pair[0], pair[1])
        tag = ' PHARMACY'
        for i in range(1, len(tag)):
            if name.endswith(tag[:i]):
                name += tag[i:]
        if 'PHARMACY' not in name:
            name += tag
        name = ' '.join(name.split())
        if name == '':
            return np.nan

    return name


def fill_pharm_info(df):
    '''Use information from all known pharmacies to fill in possible
    missing information, standardize information, and identify pharmacies
    under disparate names.
    '''
    df.PharmacyName = df.PharmacyName.apply(lambda x: _fix_pharm_name(x))

    # TODO
    return df
