from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ApartmentDetails,
    DevelopmentProject,
    LandLotDetails,
    ProductMedia,
    RealEstateProduct,
    TownhouseDetails,
    VillaDetails,
)


class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 1
    fields = ("preview", "media_type", "file", "order")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.media_type == ProductMedia.IMAGE and obj.file:
            return format_html('<img src="{}" style="height:60px;" />', obj.file.url)
        return "-"


class RealEstateProductAdmin(admin.ModelAdmin):
    inlines = [ProductMediaInline]
    list_display = ['id', 'title', 'type', 'price',
                    'location', 'for_sale', 'latitude', 'longitude']
    list_filter = ['type', 'for_sale', 'created_at']
    search_fields = ['title', 'description', 'mini_description', 'location']
    fields = [
        'title', 'description', 'mini_description', 'type', 'area', 'location', 'price', 'for_sale',
        'project', 'youtube_url', 'tiktok_url', 'latitude', 'longitude'
    ]


admin.site.register(DevelopmentProject)
admin.site.register(RealEstateProduct)
admin.site.register(TownhouseDetails)
admin.site.register(VillaDetails)
admin.site.register(ApartmentDetails)
admin.site.register(LandLotDetails)
admin.site.register(ProductMedia)

admin.site.unregister(RealEstateProduct)
admin.site.register(RealEstateProduct, RealEstateProductAdmin)
