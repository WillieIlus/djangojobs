from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer

User = get_user_model()


class CustomUserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
