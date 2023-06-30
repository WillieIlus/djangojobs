from rest_framework import serializers

from .models import Job, Click, Impression


class JobSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    user_mail = serializers.ReadOnlyField(source='user.email')
    company_name = serializers.ReadOnlyField(source='company.name')
    category = serializers.ReadOnlyField(source='category.name')
    location = serializers.ReadOnlyField(source='location.name')
    plan_title = serializers.ReadOnlyField(source='plan.title')

    expired = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    views_count = serializers.IntegerField(read_only=True)
    click_count = serializers.IntegerField(read_only=True)
    days_left = serializers.IntegerField(read_only=True)
    expires_soon = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'user', 'user_username', 'company', 'company_name', 'active', 'category', 'category_id', 'click_count',
                  'clicks', 'company', 'company_id', 'contact_email', 'user_mail', 'created_on', 'description',
                  'duration_days', 'id', 'impressions', 'location', 'location_id', 'on_site', 'openings', 'poster',
                  'requirements', 'salary', 'slug', 'plan', 'plan_id', 'plan_title', 'title', 'updated_on', 'url', 'user', 'user_id',
                  'views_count', 'work_hours', 'expired', 'price', 'days_left', 'expires_soon', 'time_since']

    def get_expired(self, obj):
        return obj.is_expired()

    def get_price(self, obj):
        return obj.get_price()

    def get_expires_soon(self, obj):
        return obj.expires_soon()

    def get_time_since(self, obj):
        return obj.time_since()


class JobImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impression
        fields = ['job', 'impression_date', 'source_ip', 'session_id']


class JobClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['job', 'click_date', 'source_ip', 'session_id']
