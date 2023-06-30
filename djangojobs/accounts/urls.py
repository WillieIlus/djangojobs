from django.urls import path, include

from .views import CustomUserViewSet

app_name = 'user'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('custom/', CustomUserViewSet.as_view({'get': 'list'}), name='custom-list'),
    path('custom/<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve'}), name='custom-detail'),
]
