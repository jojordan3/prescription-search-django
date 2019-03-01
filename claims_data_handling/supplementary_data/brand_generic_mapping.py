import pandas as pd
import sqlite3


def get_generic(brand, generic):
    meds = ()
    for i in range(len(brand)):
        brand_ = brand[i].lower()
        generic_ = generic[i].lower()
        if isinstance(brand_, str) and isinstance(generic_, str):
            if brand_ != generic_:
                mapping = [brand_, generic_]
                if mapping not in meds:
                    meds.append(mapping)
    generic_df = pd.DataFrame(data=meds, columns=['Brand', 'Generic'])
    return generic_df


if __name__ == "main":
    ndc_product = pd.read_csv('product.txt', na_values='NaN', sep='\t',
                              usecols=['PROPRIETARYNAME',
                                       'NONPROPRIETARYNAME'],
                              encoding="ISO-8859-1")
    generic_meds_df = get_generic(ndc_product.PROPRIETARYNAME.values,
                                  ndc_product.NONPROPRIETARYNAME.values)
