from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8,
                                     write_only=True, trim_whitespace=False)

    def validate_password(self, data):
        if data:
            errors = dict()
            try:
                password_validation.validate_password(password=data)
            except ValidationError as e:
                errors['password'] = list(e.messages)
            if errors:
                raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'token']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True, required=True)
    password = serializers.CharField(max_length=128, write_only=True, trim_whitespace=False, required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        user = authenticate(username=data.get('password'),
                            password=data.get('username'))

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
