import uuid
from django.db import models


class DevelopmentProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=200)
    developer = models.CharField(max_length=120)
    general_contractor = models.CharField(max_length=120)
    project_type = models.CharField(
        max_length=20,
        choices=[
            ("apartment", "Apartment"),
            ("townhouse", "Townhouse"),
            ("villa", "Villa"),
            ("mixed", "Mixed"),
        ],
    )
    delivery_time = models.DateField()
    completion_standard = models.CharField(max_length=100)
    management_unit = models.CharField(max_length=120)
    distributor = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class RealEstateProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120)
    description = models.TextField()
    area = models.DecimalField(max_digits=8, decimal_places=2)  # m²
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    for_sale = models.BooleanField(help_text="True = sale, False = rent")
    type = models.CharField(
        max_length=15,
        choices=[
            ("land", "Land"),
            ("townhouse", "Townhouse"),
            ("villa", "Villa"),
            ("apartment", "Apartment"),
        ],
    )
    project = models.ForeignKey(
        DevelopmentProject, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# --- detail tables ---------------------------------------------------------
class TownhouseDetails(models.Model):
    product = models.OneToOneField(
        RealEstateProduct, on_delete=models.CASCADE, related_name="townhouse_details"
    )
    floors = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    living_room = models.BooleanField()


class VillaDetails(models.Model):
    product = models.OneToOneField(
        RealEstateProduct, on_delete=models.CASCADE, related_name="villa_details"
    )
    floors = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    living_room = models.BooleanField()
    garden = models.BooleanField()
    swimming_pool = models.BooleanField()


class ApartmentDetails(models.Model):
    product = models.OneToOneField(
        RealEstateProduct, on_delete=models.CASCADE, related_name="apartment_details"
    )
    floor_number = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    balcony = models.BooleanField()


class LandLotDetails(models.Model):
    product = models.OneToOneField(
        RealEstateProduct, on_delete=models.CASCADE, related_name="land_details"
    )
    land_type = models.CharField(
        max_length=20,
        choices=[("residential", "Residential"), ("commercial", "Commercial")],
    )
    road_frontage = models.DecimalField(max_digits=6, decimal_places=2)  # mét
