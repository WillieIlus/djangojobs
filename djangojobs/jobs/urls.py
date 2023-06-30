from django.urls import path

from .views import JobListCreateView, JobDetailUpdateView, ImpressionCreateView, ClickCreateView

app_name = 'jobs'

urlpatterns = [
    path('<slug:slug>/', JobDetailUpdateView.as_view(), name='job-detail-update'),
    path('<int:job_id>/impressions/', ImpressionCreateView.as_view(), name='job-impression-create'),
    path('<int:job_id>/clicks/', ClickCreateView.as_view(), name='job-click-create'),
    path('', JobListCreateView.as_view(), name='job-list-create'),

]
