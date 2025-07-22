from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'listings'

urlpatterns = [
    # Development Projects
    path('projects/', views.DevelopmentProjectListView.as_view(), name='project-list'),
    path('projects/<uuid:pk>/',
         views.DevelopmentProjectDetailView.as_view(), name='project-detail'),

    # All Real Estate Products
    path('properties/', views.RealEstateProductListView.as_view(),
         name='property-list'),
    path('properties/<str:pk>/',
         views.RealEstateProductDetailView.as_view(), name='property-detail'),

    # Type-specific endpoints
    path('apartments/', views.ApartmentListView.as_view(), name='apartment-list'),
    path('apartments/<str:pk>/', views.ApartmentDetailView.as_view(),
         name='apartment-detail'),

    path('townhouses/', views.TownhouseListView.as_view(), name='townhouse-list'),
    path('townhouses/<str:pk>/', views.TownhouseDetailView.as_view(),
         name='townhouse-detail'),

    path('villas/', views.VillaListView.as_view(), name='villa-list'),
    path('villas/<str:pk>/', views.VillaDetailView.as_view(), name='villa-detail'),

    path('land/', views.LandListView.as_view(), name='land-list'),
    path('land/<str:pk>/', views.LandDetailView.as_view(), name='land-detail'),

    # Utility endpoints
    path('property-types/', views.property_types_view, name='property-types'),
    path('search/', views.search_properties_view, name='search-properties'),
]
