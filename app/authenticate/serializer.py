from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8,
                                     write_only=True, trim_whitespace=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'token']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True, trim_whitespace=False)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        password = data.get('password')
        username = data.get('username')
        if not password:
            raise serializers.ValidationError('Password required')
        if not username:
            raise serializers.ValidationError('Username required')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'balance', 'first_name', 'last_name', 'email', 'last_login']
