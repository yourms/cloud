from rest_framework import serializers

from android_rest.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'phone', 'address', 'gno']
