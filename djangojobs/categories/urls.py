app_name = 'category'

from django.urls import path

from categories.views import CategoryList, CategoryDetail

urlpatterns = [
    path('', CategoryList.as_view(), name='list'),
    path('<slug:slug>/', CategoryDetail.as_view(), name='detail'),
]
