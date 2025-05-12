from django.contrib import admin

from .models import (
    DevelopmentProject,
    RealEstateProduct,
    TownhouseDetails,
    VillaDetails,
    ApartmentDetails,
    LandLotDetails,
)

admin.site.register(DevelopmentProject)
admin.site.register(RealEstateProduct)
admin.site.register(TownhouseDetails)
admin.site.register(VillaDetails)
admin.site.register(ApartmentDetails)
admin.site.register(LandLotDetails)
