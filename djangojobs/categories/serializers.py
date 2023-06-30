from rest_framework import serializers

from jobs.models import Job
from jobs.serializers import JobSerializer
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    job_count = serializers.SerializerMethodField()
    jobs = JobSerializer(many=True, read_only=True)

    def get_job_count(self, category):
        return Job.objects.filter(category=category).count()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'photo', 'description', 'url', 'category_order', 'job_count', 'jobs']
