from django.urls import path

from .views import (
    PlanListCreateView,
    PlanRetrieveUpdateDestroyView,
)

app_name = 'plans'

urlpatterns = [
    path('subscription-plans/', PlanListCreateView.as_view(), name='subscription-plan-list'),
    path('subscription-plans/<int:pk>/', PlanRetrieveUpdateDestroyView.as_view(),
         name='subscription-plan-detail'),
]
