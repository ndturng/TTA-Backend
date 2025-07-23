import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver

from listings.utils import generate_product_id, product_media_path


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
    # ID format: {type_prefix}-{sequential_number}, e.g., T-001, V-001, A-001, L-001
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    title = models.CharField(max_length=120)
    description = models.TextField()
    area = models.DecimalField(max_digits=8, decimal_places=2)  # m²
    location = models.CharField(max_length=200)  # Vị trí
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
    )  # Dự án liên kết
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_id(self):
        """Generate a custom ID based on product type."""
        return generate_product_id(self)

    def save(self, *args, **kwargs):
        # Generate ID if this is a new product
        if not self.id:
            self.id = self.generate_id()
        super().save(*args, **kwargs)

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
    garage = models.PositiveSmallIntegerField(default=0)


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


# --- media tables ---------------------------------------------------------
class ProductMedia(models.Model):
    IMAGE = "image"
    VIDEO = "video"

    MEDIA_TYPE_CHOICES = [
        (IMAGE, "Image"),
        (VIDEO, "Video"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        RealEstateProduct,
        on_delete=models.CASCADE,
        related_name="media",
    )
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to=product_media_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveSmallIntegerField(
        default=0)  # optional, for slideshow order

    class Meta:
        ordering = ["order", "uploaded_at"]

    def clean(self):
        """Enforce max‑images / max‑videos rule."""
        if not hasattr(self, 'product') or not self.product or not self.product.id:
            return  # Skip validation if product is not set or not saved yet

        imgs = ProductMedia.objects.filter(
            product=self.product, media_type=self.IMAGE
        ).exclude(pk=self.pk)
        vids = ProductMedia.objects.filter(
            product=self.product, media_type=self.VIDEO
        ).exclude(pk=self.pk)

        if self.media_type == self.IMAGE and imgs.count() >= 10:
            raise ValidationError("A product can have at most 10 images.")
        if self.media_type == self.VIDEO and vids.count() >= 3:
            raise ValidationError("A product can have at most 3 videos.")

    def save(self, *args, **kwargs):
        self.full_clean()      # triggers clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.media_type.capitalize()} ({self.order}) for {self.product}"


@receiver(models.signals.post_delete, sender=ProductMedia)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete file from filesystem when corresponding `ProductMedia` object is deleted."""
    if instance.file and instance.file.storage.exists(instance.file.name):
        instance.file.delete(save=False)
