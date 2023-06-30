from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from .models import Location, Country
from .serializers import LocationSerializer, CountrySerializer


class CountryListCreateAPIView(ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]


class CountryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]


class LocationListCreateAPIView(ListCreateAPIView):
    lookup_field = 'slug'
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]


class LocationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]
