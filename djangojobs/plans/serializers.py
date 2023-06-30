from rest_framework import serializers

from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'title', 'description', 'price_per_day', 'trial_duration', 'is_default',
                  'is_fallback', 'is_available', 'is_visible', 'is_trial', 'created', 'modified', 'weight')
        read_only_fields = ('created', 'modified')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price_per_day'] = str(representation['price_per_day'])  # Convert DecimalField to string
        return representation
