from .models import RxClaim, PharmacyInfo, BrandToGeneric, ZipCodeInfo
import pandas as pd
from django_pandas.io import read_frame


def search_by_pharm(drug, zipcode):
    drug = generic(drug)
    try:
        qs = RxClaim.objects.filter(pharmacyid__PharmacyZip__in=[zipcode,
                                                                 'XXXXX'],
                                    DrugLabelName__contains=drug)
        df = qs.to_pivot_table(rows=['PharmacyID'], values='UnitCost',
                               aggfunc='np.mean')
        return df.sort_values(by='UnitCost')
    except DoesNotExist:
        try:
            zipcodes = get_nearby(zipcode)
            qs = RxClaim.objects.filter(pharmacyid__PharmacyZip__in=[zipcodes],
                                        DrugLabelName__contains=drug)
            df = qs.to_pivot_table(rows=['PharmacyID'], values='UnitCost',
                                   aggfunc='np.mean')
            return df.sort_values(by='DrugLabelName')[:5]
        except:
            raise


def get_pharm_info(pharmID):
    return read_frame(PharmacyInfo.objects.filter(pk__in=[pharmID]),
                      index_col='PharmacyID')


def search_by_pbm(self, drug):
    drug = generic(drug)
    try:
        qs = RxClaim.objects.filter(DrugLabelName__contains=drug)
        df = qs.to_pivot_table(rows=['PBMVendor'],
                               values='UnitCost', aggfunc='np.mean')
        return df.sort_values(by='UnitCost')[:5]
    except DoesNotExist:
        raise


def generic(drug):
    try:
        med = BrandToGeneric.objects.get(Brand__contains=drug)
        generic = med.values('Generic')
    except DoesNotExist:
        try:
            med = BrandToGeneric.objects.get(Generic__contains=drug)
            generic = med.values('Generic')
        except DoesNotExist:
            raise
    finally:
        return generic


def get_nearby(zipcode):
    try:
        zc = ZipCodeInfo.objects.get(pk=zipcode)
        lat_ = zc.value('latitude')
        long_ = zc.value('longitude')
        qs = ZipCodeInfo.objects.filter(latitude__range=((lat_ - 0.03),
                                                         (lat_ + 0.03)),
                                        longitude__range=((long_ - 0.03),
                                                          (long_ + 0.03)))
        zipcodes = qs.values_list('zipcode', flat=True)
        return zipcodes
    except DoesNotExist:
        raise
