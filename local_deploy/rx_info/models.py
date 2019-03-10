from django.db import models
import numpy as np


class ZipCodeInfo(models.Model):
    '''Model containing zip code information for lookup when local pharmacy
    search returns no results.
    '''
    zipcode = models.CharField(max_length=5, primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # Allows SQLite query sets to be transformed to pandas objects
    objects = DataFrameManager()

    def __str__(self):
        return self.zipcode


class PharmacyInfo(models.Model):
    '''Model containing complete pharmacy information
    '''
    PharmacyID = models.CharField(max_length=200, primary_key=True)
    PharmacyNumber = models.CharField(max_length=15)
    PharmacyNPI = models.CharField(max_length=15)
    PharmacyTaxId = models.CharField(max_length=15)
    PharmacyName = models.CharField(max_length=200)
    PharmacyStreetAddress1 = models.CharField(max_length=200)
    PharmacyCity = models.CharField(max_length=200)
    PharmacyZip = models.ForeignKey(ZipCodeInfo, on_delete='set null')

    def __str__(self):
        return (self.PharmacyName + ' at ' + self.PharmacyStreetAddress1 +
                ', ' + self.PharmacyCity)


class RxClaim(models.Model):
    '''Model for individual rx_claims--used in views.py to search local
    pharmacies and PBMs and to create SQLite db
    '''
    PharmacyID = models.ForeignKey(PharmacyInfo, on_delete='set null')
    UnitCost = models.FloatField()
    DrugLabelName = models.CharField(max_length=200)
    PBMVendor = models.CharField(max_length=200)

    def __str__(self):
        return '<PharmacyID: {}, DrugLabelName: {}'.format(self.PharmacyID,
                                                           self.DrugLabelName)


class BrandToGeneric(models.Model):
    '''Model for individual rx_claims--used in views.py to search medications
    by PBM and to create SQLite db
    '''
    Brand = models.CharField(max_length=600)
    Generic = models.CharField(max_length=600)

    def __str__(self):
        return '<{} is a brandname for {}'.format(self.Brand, self.Generic)
