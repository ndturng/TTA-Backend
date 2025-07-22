from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    ApartmentDetails,
    DevelopmentProject,
    LandLotDetails,
    RealEstateProduct,
    TownhouseDetails,
    VillaDetails,
)
from .serializers import (
    ApartmentSerializer,
    DevelopmentProjectSerializer,
    LandSerializer,
    RealEstateProductListSerializer,
    RealEstateProductSerializer,
    TownhouseSerializer,
    VillaSerializer,
)


# Development Projects API Views
class DevelopmentProjectListView(generics.ListAPIView):
    """List all development projects."""
    queryset = DevelopmentProject.objects.all()
    serializer_class = DevelopmentProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location', 'developer']
    ordering_fields = ['name', 'delivery_time']
    ordering = ['-delivery_time']


class DevelopmentProjectDetailView(generics.RetrieveAPIView):
    """Get a specific development project."""
    queryset = DevelopmentProject.objects.all()
    serializer_class = DevelopmentProjectSerializer


# Real Estate Products API Views
class RealEstateProductListView(generics.ListAPIView):
    """List all real estate products with filtering and search."""
    queryset = RealEstateProduct.objects.select_related(
        'project').prefetch_related('media')
    serializer_class = RealEstateProductListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'for_sale', 'project']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price', 'area', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Custom filtering
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        min_area = self.request.query_params.get('min_area')
        max_area = self.request.query_params.get('max_area')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_area:
            queryset = queryset.filter(area__gte=min_area)
        if max_area:
            queryset = queryset.filter(area__lte=max_area)

        return queryset


class RealEstateProductDetailView(generics.RetrieveAPIView):
    """Get a specific real estate product with full details."""
    queryset = RealEstateProduct.objects.select_related(
        'project',
        'townhouse_details',
        'villa_details',
        'apartment_details',
        'land_details'
    ).prefetch_related('media')
    serializer_class = RealEstateProductSerializer


# Type-specific API Views
class ApartmentListView(generics.ListAPIView):
    """List all apartments."""
    serializer_class = RealEstateProductListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['for_sale', 'project']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price', 'area', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = RealEstateProduct.objects.filter(
            type='apartment').select_related('project').prefetch_related('media')

        # Custom filtering for apartments
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        min_area = self.request.query_params.get('min_area')
        max_area = self.request.query_params.get('max_area')
        bedrooms = self.request.query_params.get('bedrooms')
        bathrooms = self.request.query_params.get('bathrooms')
        has_balcony = self.request.query_params.get('has_balcony')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if min_area:
            queryset = queryset.filter(area__gte=min_area)
        if max_area:
            queryset = queryset.filter(area__lte=max_area)
        if bedrooms:
            queryset = queryset.filter(apartment_details__bedrooms=bedrooms)
        if bathrooms:
            queryset = queryset.filter(apartment_details__bathrooms=bathrooms)
        if has_balcony is not None:
            queryset = queryset.filter(
                apartment_details__balcony=has_balcony.lower() == 'true')

        return queryset


class ApartmentDetailView(generics.RetrieveAPIView):
    """Get a specific apartment with full details."""
    serializer_class = ApartmentSerializer

    def get_queryset(self):
        return RealEstateProduct.objects.filter(type='apartment').select_related(
            'project', 'apartment_details'
        ).prefetch_related('media')


class TownhouseListView(generics.ListAPIView):
    """List all townhouses."""
    serializer_class = RealEstateProductListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['for_sale', 'project']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price', 'area', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return RealEstateProduct.objects.filter(type='townhouse').select_related('project').prefetch_related('media')


class TownhouseDetailView(generics.RetrieveAPIView):
    """Get a specific townhouse with full details."""
    serializer_class = TownhouseSerializer

    def get_queryset(self):
        return RealEstateProduct.objects.filter(type='townhouse').select_related(
            'project', 'townhouse_details'
        ).prefetch_related('media')


class VillaListView(generics.ListAPIView):
    """List all villas."""
    serializer_class = RealEstateProductListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['for_sale', 'project']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price', 'area', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return RealEstateProduct.objects.filter(type='villa').select_related('project').prefetch_related('media')


class VillaDetailView(generics.RetrieveAPIView):
    """Get a specific villa with full details."""
    serializer_class = VillaSerializer

    def get_queryset(self):
        return RealEstateProduct.objects.filter(type='villa').select_related(
            'project', 'villa_details'
        ).prefetch_related('media')


class LandListView(generics.ListAPIView):
    """List all land lots."""
    serializer_class = RealEstateProductListSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['for_sale', 'project']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price', 'area', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return RealEstateProduct.objects.filter(type='land').select_related('project').prefetch_related('media')


class LandDetailView(generics.RetrieveAPIView):
    """Get a specific land lot with full details."""
    serializer_class = LandSerializer

    def get_queryset(self):
        return RealEstateProduct.objects.filter(type='land').select_related(
            'project', 'land_details'
        ).prefetch_related('media')


# Utility API Views
@api_view(['GET'])
def property_types_view(request):
    """Get all available property types."""
    types = [
        {'value': choice[0], 'label': choice[1]}
        for choice in RealEstateProduct._meta.get_field('type').choices
    ]
    return Response({'property_types': types})


@api_view(['GET'])
def search_properties_view(request):
    """Advanced search endpoint for properties."""
    query = request.query_params.get('q', '')
    property_type = request.query_params.get('type')
    for_sale = request.query_params.get('for_sale')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    queryset = RealEstateProduct.objects.select_related(
        'project').prefetch_related('media')

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(project__name__icontains=query)
        )

    if property_type:
        queryset = queryset.filter(type=property_type)

    if for_sale is not None:
        queryset = queryset.filter(for_sale=for_sale.lower() == 'true')

    if min_price:
        queryset = queryset.filter(price__gte=min_price)

    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    serializer = RealEstateProductListSerializer(
        queryset[:20], many=True, context={'request': request}
    )

    return Response({
        'results': serializer.data,
        'count': queryset.count()
    })


@api_view(['GET'])
def similar_products(request, product_id):
    """Get similar products based on price, type, and area."""
    from decimal import Decimal
    
    try:
        product = RealEstateProduct.objects.get(id=product_id)
    except RealEstateProduct.DoesNotExist:
        return Response(
            {'detail': 'Product not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Define similarity criteria - convert to Decimal for proper arithmetic
    price_range = Decimal('0.3')  # 30% price variance
    area_range = Decimal('0.2')   # 20% area variance
    
    min_price = product.price * (Decimal('1') - price_range)
    max_price = product.price * (Decimal('1') + price_range)
    min_area = product.area * (Decimal('1') - area_range)
    max_area = product.area * (Decimal('1') + area_range)
    
    # Find similar products
    similar_queryset = RealEstateProduct.objects.filter(
        type=product.type,  # Same type (apartment, townhouse, etc.)
        price__gte=min_price,
        price__lte=max_price,
        area__gte=min_area,
        area__lte=max_area,
        for_sale=product.for_sale  # Same transaction type (sale/rent)
    ).exclude(
        id=product_id  # Exclude the current product
    ).order_by('?')[:5]  # Random order, limit to 5
    
    # Return only product IDs
    similar_ids = list(similar_queryset.values_list('id', flat=True))
    
    return Response({
        'product_id': product_id,
        'similar_products': similar_ids,
        'criteria': {
            'type': product.type,
            'price_range': f"{min_price:,.0f} - {max_price:,.0f} VND",
            'area_range': f"{min_area:.1f} - {max_area:.1f} m²",
            'for_sale': product.for_sale
        }
    })
