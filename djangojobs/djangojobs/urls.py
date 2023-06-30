from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('companies/', include('companies.urls', namespace='companies')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('locations/', include('locations.urls', namespace='locations')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('plans/', include('plans.urls', namespace='plans')),
]
