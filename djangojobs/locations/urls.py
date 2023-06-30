from django.urls import path

from .views import (
    CountryListCreateAPIView,
    CountryRetrieveUpdateDestroyAPIView,
    LocationListCreateAPIView,
    LocationRetrieveUpdateDestroyAPIView,
)

app_name = 'locations'

urlpatterns = [
    path('countries/', CountryListCreateAPIView.as_view(), name='country-list-create'),
    path('countries/<int:pk>/', CountryRetrieveUpdateDestroyAPIView.as_view(), name='country-retrieve-update-destroy'),
    path('', LocationListCreateAPIView.as_view(), name='location-list-create'),
    path('<slug:slug>/', LocationRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
]
