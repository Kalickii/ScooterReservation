from rest_framework import serializers

from users.models import CustomUser, UserProfile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user']
