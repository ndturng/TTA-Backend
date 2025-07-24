from rest_framework import serializers

from .models import (
    ApartmentDetails,
    DevelopmentProject,
    LandLotDetails,
    ProductMedia,
    RealEstateProduct,
    TownhouseDetails,
    VillaDetails,
)


class DevelopmentProjectSerializer(serializers.ModelSerializer):
    area_size_formatted = serializers.SerializerMethodField()

    class Meta:
        model = DevelopmentProject
        fields = [
            'id', 'name', 'location', 'developer', 'general_contractor',
            'project_type', 'delivery_time', 'completion_standard',
            'management_unit', 'distributor', 'area_size', 'area_size_formatted',
            'quantity', 'policy'
        ]

    def get_area_size_formatted(self, obj):
        """Format area size in hectares (Ha)."""
        if obj.area_size is not None:
            # Format the decimal to remove unnecessary zeros
            formatted_area = f"{obj.area_size:g}"
            return f"{formatted_area} Ha"
        return None


class ProductMediaSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductMedia
        fields = ['id', 'media_type', 'file',
                  'file_url', 'uploaded_at', 'order']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class TownhouseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TownhouseDetails
        fields = ['floors', 'bedrooms', 'bathrooms', 'living_room',
                  'garage', 'policy', 'structure', 'interior']


class VillaDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillaDetails
        fields = ['floors', 'bedrooms', 'bathrooms',
                  'living_room', 'garden', 'swimming_pool', 'garage']


class ApartmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentDetails
        fields = ['floor_number', 'bedrooms', 'bathrooms', 'balcony']


class LandLotDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLotDetails
        fields = ['land_type', 'road_frontage']


class RealEstateProductSerializer(serializers.ModelSerializer):
    project = DevelopmentProjectSerializer(read_only=True)
    media = ProductMediaSerializer(many=True, read_only=True)

    # Details based on product type
    townhouse_details = TownhouseDetailsSerializer(read_only=True)
    villa_details = VillaDetailsSerializer(read_only=True)
    apartment_details = ApartmentDetailsSerializer(read_only=True)
    land_details = LandLotDetailsSerializer(read_only=True)

    # Computed fields
    price_formatted = serializers.SerializerMethodField()
    area_formatted = serializers.SerializerMethodField()
    type_display = serializers.CharField(
        source='get_type_display', read_only=True)
    for_sale_display = serializers.SerializerMethodField()

    class Meta:
        model = RealEstateProduct
        fields = [
            'id', 'title', 'description', 'area', 'area_formatted', 'location',
            'price', 'price_formatted', 'for_sale', 'for_sale_display', 'type',
            'type_display', 'created_at', 'project', 'media',
            'townhouse_details', 'villa_details', 'apartment_details', 'land_details'
        ]

    def get_price_formatted(self, obj):
        """Format price in Vietnamese billions (Tỷ)."""
        billions = obj.price / 1_000_000_000
        if billions >= 1:
            return f"{billions:,.1f} Tỷ"
        millions = obj.price / 1_000_000
        return f"{millions:,.0f} Triệu"

    def get_area_formatted(self, obj):
        """Format area with unit."""
        return f"{obj.area:.0f} m²"

    def get_for_sale_display(self, obj):
        """Human readable for_sale field."""
        return "For Sale" if obj.for_sale else "For Rent"


class RealEstateProductListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views."""
    project_name = serializers.CharField(source='project.name', read_only=True)
    price_formatted = serializers.SerializerMethodField()
    area_formatted = serializers.SerializerMethodField()
    type_display = serializers.CharField(
        source='get_type_display', read_only=True)
    for_sale_display = serializers.SerializerMethodField()
    main_images = serializers.SerializerMethodField()

    class Meta:
        model = RealEstateProduct
        fields = [
            'id', 'title', 'area', 'area_formatted', 'location',
            'price', 'price_formatted', 'for_sale', 'for_sale_display',
            'type', 'type_display', 'created_at', 'project_name', 'main_images'
        ]

    def get_price_formatted(self, obj):
        """Format price in Vietnamese billions (Tỷ)."""
        billions = obj.price / 1_000_000_000
        if billions >= 1:
            return f"{billions:,.1f} Tỷ"
        millions = obj.price / 1_000_000
        return f"{millions:,.0f} Triệu"

    def get_area_formatted(self, obj):
        return f"{obj.area:.0f} m²"

    def get_for_sale_display(self, obj):
        return "For Sale" if obj.for_sale else "For Rent"

    def get_main_images(self, obj):
        """Get up to 3 main images for the product."""
        main_media = obj.media.filter(
            media_type=ProductMedia.IMAGE).order_by('order')[:3]
        images = []
        request = self.context.get('request')

        for media in main_media:
            if media.file:
                if request:
                    images.append(request.build_absolute_uri(media.file.url))
                else:
                    images.append(media.file.url)

        # Pad with None if we have fewer than 3 images
        while len(images) < 3:
            images.append(None)

        return images


class TownhouseListSerializer(RealEstateProductListSerializer):
    """Enhanced serializer for townhouse list views with additional details."""
    bedrooms = serializers.SerializerMethodField()
    bathrooms = serializers.SerializerMethodField()
    garage = serializers.SerializerMethodField()

    class Meta(RealEstateProductListSerializer.Meta):
        fields = RealEstateProductListSerializer.Meta.fields + \
            ['bedrooms', 'bathrooms', 'garage']

    def get_bedrooms(self, obj):
        return obj.townhouse_details.bedrooms if hasattr(obj, 'townhouse_details') else None

    def get_bathrooms(self, obj):
        return obj.townhouse_details.bathrooms if hasattr(obj, 'townhouse_details') else None

    def get_garage(self, obj):
        return obj.townhouse_details.garage if hasattr(obj, 'townhouse_details') else None


class VillaListSerializer(RealEstateProductListSerializer):
    """Enhanced serializer for villa list views with additional details."""
    bedrooms = serializers.SerializerMethodField()
    bathrooms = serializers.SerializerMethodField()
    garage = serializers.SerializerMethodField()

    class Meta(RealEstateProductListSerializer.Meta):
        fields = RealEstateProductListSerializer.Meta.fields + \
            ['bedrooms', 'bathrooms', 'garage']

    def get_bedrooms(self, obj):
        return obj.villa_details.bedrooms if hasattr(obj, 'villa_details') else None

    def get_bathrooms(self, obj):
        return obj.villa_details.bathrooms if hasattr(obj, 'villa_details') else None

    def get_garage(self, obj):
        return obj.villa_details.garage if hasattr(obj, 'villa_details') else None


# Specific serializers for each product type
class ApartmentSerializer(RealEstateProductSerializer):
    """Serializer specifically for apartments."""
    class Meta(RealEstateProductSerializer.Meta):
        pass

    def to_representation(self, instance):
        """Ensure we only return apartment-specific details."""
        data = super().to_representation(instance)
        # Remove non-apartment details
        data.pop('townhouse_details', None)
        data.pop('villa_details', None)
        data.pop('land_details', None)
        return data


class TownhouseSerializer(RealEstateProductSerializer):
    """Serializer specifically for townhouses."""
    class Meta(RealEstateProductSerializer.Meta):
        pass

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('apartment_details', None)
        data.pop('villa_details', None)
        data.pop('land_details', None)
        return data


class VillaSerializer(RealEstateProductSerializer):
    """Serializer specifically for villas."""
    class Meta(RealEstateProductSerializer.Meta):
        pass

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('apartment_details', None)
        data.pop('townhouse_details', None)
        data.pop('land_details', None)
        return data


class LandSerializer(RealEstateProductSerializer):
    """Serializer specifically for land lots."""
    class Meta(RealEstateProductSerializer.Meta):
        pass

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('apartment_details', None)
        data.pop('townhouse_details', None)
        data.pop('villa_details', None)
        return data
