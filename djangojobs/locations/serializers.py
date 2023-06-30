from rest_framework import serializers

from jobs.models import Job
from jobs.serializers import JobSerializer
from .models import Location, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'id', 'slug']


class LocationSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    job_count = serializers.SerializerMethodField()
    jobs = JobSerializer(many=True, read_only=True)

    def get_job_count(self, location):
        return Job.objects.filter(location=location).count()

    class Meta:
        model = Location
        fields = ['id', 'name', 'slug', 'url', 'job_count', 'jobs']
