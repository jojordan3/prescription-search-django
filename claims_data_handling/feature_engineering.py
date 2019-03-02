import numpy as np


def get_unit_cost(row):
    '''This function calculates a the unit cost by first calculating the total
    cost out of the available columns relating to cost. There are two unique
    measurements to get the total cost, and completeness of the necessary
    fields varies widely across files.

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
    '''Reduces 9 digit zip codes to standard 5 digit zip codes. Also validates
    that zip codes are read in as strings and thus retain leading zeroes.
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
        abbreviations = [
            ['BRDWAY', 'BROADWAY'], ['BWAY', 'BROADWAY'], ['AVENUE', 'AVE'],
            ['BOULEVARD', 'BLVD'], ['ROAD', 'RD'], ['TRAC', 'TRACE'],
            ['HIGHWAY', 'HWY'], ['STREET', 'ST'], ['PARKWAY', 'PKWY'],
            ['PLZ', 'PLAZA'], ['SOUTH', 'S'], ['SQUARE', 'SQ'], ['/', ' '],
            [' RTE', ' RT'], ['ROUTE', 'RT'], ['DRIVE', 'DR'], ['EAST', 'E'],
            ['WEST', 'W'], ['NORTH', 'N'], ['SOUTH', 'S'], ['CIRCLE', 'CIR'],
            ['FREDRICK', 'FREDERICK'], [' STE ', ' SUITE '], ['SECOND', '2ND'],
            [' CALEF', ' CALIFORNIA'], [' SO ', ' S '], ['FIRST', '1ST'],
            [' MOUNT ', ' MT '], ['CTR', 'CENTER'], ['CNTR', 'CENTER']
            ]
        address = re.sub(r'[#\.,\-/\']', '', address)
        for abbreviation in abbreviations:
            if isinstance(address, str):
                address = address.replace(abbreviation[0], abbreviation[1])
        if (address == '') or (address == r'[\s*]'):
            address = np.nan
        else:
            addresss = ' '.join(address.split())
    return address


def fix_pharm_name(name):
    '''Standardize pharmacy name'''
    if isinstance(name, str):
        name_dict = {
            'ENVISIONRX.COM': [
                'ORCHARD PHARMACEUTICALS', 'ORCHARD SPECIALTY', 'ENVISION'],
            'ACCREDO.COM': ['CURASCRIPT', 'ACCREDO'],
            'CVS PHARMACY': ['CVS', 'TARGET', 'CAREMARK'],
            'NAU FRONSKE HEALTH SERVICES': ['FRONSKE', 'NAU CAMPUS'],
            'WEGMANS PHARMACY': ['WEGMANS'],
            'WALGREENS PHARMACY': ['WALGREENS'],
            'ALBERTSONS PHARMACY': ['ALBERTSONS', 'SAVON'],
            'WALMART PHARMACY': ['WALMART', 'WAL-MART'],
            'KMART PHARMACY': ['K MART', 'KMART'],
            }

        for updated_name, markers in name_dict.items():
            if any(marker in name for marker in markers):
                return updated_name
        name = re.sub(r'[\.,\-/\'#]', '', name)
        name = re.sub(r'[0-9]+', '', name)
        concatd = [[' COMP', ' CO'], ['SOLUTIO', 'SOLUTIONS'],
                   ['EMPLOYE', 'EMPLOYEE'], [' SUB', ' SUBWAY'],
                   [' SP', ''], [' WY', ' WAY']]
        for cutoff in concatd:
            if name.endswith(cutoff[0]):
                name = name[:-len(cutoff[0])] + cutoff[1]
        pairs = [['INC', ''], ['HEALTHGROUP', 'HEALTH GROUP'], ['LLC', ''],
                 ['GRP', 'GROUP'], ['PHARMACIES', 'PHARMACY'], [' LL', ''],
                 ['SERVICES', ''], ['SERVICE', ''], ['SPECIALTY', ''],
                 ['PHCY', 'PHARMACY'], ['HLTH', 'HEALTH'], ['COMPANY', 'CO'],
                 ['PHARMACY', ' PHARMACY '], ['UNIV', 'UNIVERSITY'],
                 ['DRUGS', ' DRUGS '],  ['&', 'AND'], ['SRVCES', ''],
                 ['HELTH', 'HEALTH'], ['SVCS', ''], [' OF ', '']]
        for pair in pairs:
            name = name.replace(pair[0], pair[1])
        name = ' '.join(name.split())
        if name == '':
            return np.nan
        tag = ' PHARMACY'
        for i in range(2, len(tag)):
            if name.endswith(tag[:i]):
                name += tag[i:]
        if 'PHARMACY' not in name:
            name += tag

    return name


def fill_pharm_info(df):
    '''Use information from all known pharmacies to fill in possible
    missing information, standardize information, and identify pharmacies
    under disparate names.
    '''
    df.PharmacyName = df.PharmacyName.apply(lambda x: _fix_pharm_name(x))

    # TODO
    return df
