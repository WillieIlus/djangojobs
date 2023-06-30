from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from companies import views

app_name = 'company'

urlpatterns = [
    path('companies/', views.CompanyList.as_view()),
    path('companies/<slug:slug>/', views.CompanyDetail.as_view(), name='detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
