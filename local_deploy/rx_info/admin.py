# Register your models here.
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import ZipCodeInfo, PharmacyInfo, RxClaim, BrandToGeneric
# admin
# labs7meddash

class PersonAdmin(ImportExportModelAdmin):
    admin.site.register(ZipCodeInfo)
    admin.site.register(PharmacyInfo)
    admin.site.register(RxClaim)
    admin.site.register(BrandToGeneric)
