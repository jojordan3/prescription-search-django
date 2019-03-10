# Register your models here.
from django.contrib import admin
from .models import ZipCodeInfo, PharmacyInfo, RxClaim, BrandToGeneric


@admin.register(ZipCodeInfo, PharmacyInfo, RxClaim, BrandToGeneric)
class PersonAdmin(admin.ModelAdmin):
    pass
