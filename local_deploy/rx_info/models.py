from django.db import models
from django_pandas.managers import DataFrameManager
import numpy as np


class RxClaim(models.Model):
    '''Model for individual rx_claims--used in views.py to search local
    pharmacies and PBMs and to create SQLite db
    '''
    PharmacyID = models.ForeignKey(PharmacyInfo)
    UnitCost = models.FloatField()
    DrugLabelName = models.CharField(max_length=200)
    PBMVendor = models.CharField(max_length=200)

    # Allows SQLite query sets to be transformed to pandas objects
    objects = DataFrameManager()


class PharmacyInfo(models.Model):
    '''Model containing complete pharmacy information
    '''
    PharmacyID = models.CharField(max_length=200, primary_key=True)
    PharmacyName = models.CharField(max_length=200)
    PharmacyStreetAddress1 = models.CharField(max_length=200)
    PharmacyCity = models.CharField(max_length=200)
    PharmacyZip = models.ForeignKey(ZipCodeInfo)

    # Allows SQLite query sets to be transformed to pandas objects
    objects = DataFrameManager()


class BrandToGeneric(models.Model):
    '''Model for individual rx_claims--used in views.py to search medications
    by PBM and to create SQLite db
    '''
    Brand = models.CharField(max_length=200, primary_key=True)
    Generic = models.CharField(max_length=200)


class ZipCodeInfo(models.Model):
    '''Model containing zip code information for lookup when local pharmacy
    search returns no results.
    '''
    zipcode = models.CharField(max_length=5, primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # Allows SQLite query sets to be transformed to pandas objects
    objects = DataFrameManager()
