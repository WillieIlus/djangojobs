from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Plan
from .serializers import PlanSerializer


class PlanListCreateView(ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PlanRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
