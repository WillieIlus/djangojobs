from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Company
        fields = ['id', 'user', 'name', 'slug', 'url', 'image', 'description', 'logo', 'email', 'website', 'category',
                  'address', 'location', 'created_at', 'modified_at']
