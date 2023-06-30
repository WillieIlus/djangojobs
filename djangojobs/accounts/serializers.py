from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('photo', 'address', 'location', 'bio', 'date_of_birth', 'nickname', 'title')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('email', 'last_login', 'phone_number', 'gender', 'profile' 'username', 'first_name', 'last_name',
                  'email', 'photo', 'date_of_birth')
