from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView

from .models import Impression, Click
from .models import Job
from .serializers import JobImpressionSerializer, JobClickSerializer
from .serializers import JobSerializer


class JobListCreateView(ListCreateAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        jobs = Job.objects.all()  # # Job.get_sorted_jobs()
        query = self.request.GET.get('query', '')
        categories = self.request.GET.get('category', '')

        if query:
            jobs = jobs.filter(title__icontains=query)

        if categories:
            categories_list = categories.split(',')
            jobs = jobs.filter(category__slug__in=categories_list)

        return jobs

    def post(self, request, *args, **kwargs):
        # You can implement custom logic for POST requests here if needed
        return self.create(request, *args, **kwargs)


class JobDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = JobSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Job.objects.get_queryset()


class ImpressionCreateView(ListCreateAPIView):
    serializer_class = JobImpressionSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return Impression.objects.filter(job_id=job_id)


class ClickCreateView(ListCreateAPIView):
    serializer_class = JobClickSerializer

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        return Click.objects.filter(job_id=job_id)
