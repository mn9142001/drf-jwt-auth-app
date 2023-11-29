from rest_framework import serializers
from .user import UserLoggedInSerializer
from ..tokens import PasswordResetToken, CustomTokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from ..models import OTP
from django.contrib.auth.models import update_last_login
from django.db import IntegrityError

User = get_user_model()

class JWTLoginSerializer(CustomTokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        update_last_login(None, self.user)
        data['user'] = UserLoggedInSerializer(self.user).data
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['hello'] = "world"

        return token

class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True, source="password", style={'input_type' : 'password'})
    password2 = serializers.CharField(write_only = True, style={'input_type' : 'password'})

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['password2']:
            raise ValidationError("password do not match each other")
        attrs.pop('password2')
        validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        try:
            return User.objects.create_user(**validated_data)
        except IntegrityError as e:
            raise ValidationError("username already exists", code="username")


    def to_representation(self, instance):
        data = super().to_representation(instance)
        refresh_token = CustomTokenObtainPairSerializer.get_token(user=instance)
        data["refresh_token"] = str(refresh_token)
        data["access_token"] = str(refresh_token.access_token)
        return data

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name' : {'required' : True},
            'email' : {'required' : True},
        }

class PasswordSendResetSerializer(serializers.ModelSerializer):
    """send reset otp serializer"""
    email = serializers.SlugRelatedField(slug_field="email", queryset=User.objects.all())

    class Meta:
        model = OTP
        fields = ('email',)

class PasswordResetVerifySerializer(serializers.ModelSerializer):
    otp = serializers.SlugRelatedField(slug_field="otp", queryset=OTP.objects.all())

    class Meta:
        model = OTP
        fields = ('otp',)

    def create(self, validated_data):
        return validated_data['otp'].user

    def to_representation(self, instance):
        data = {}
        token = PasswordResetToken.get_token(self.instance)
        data['access'] = str(token.access_token)
        return data

class BasePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, style={'input_type' : "password"})

    def validate_old_password(self, value):
        self.instance = self.context['request'].user
        if not self.instance.check_password(value):
            raise ValidationError("old passwords doesn't match your password")
        return value


class PasswordChangeSerializer(BasePasswordSerializer):
    new_password = serializers.CharField(required=True,  style={'input_type' : "password"})

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        if not instance.is_active:
            instance.is_active = True
        self.instance = instance.save()
        return instance
    
    def to_representation(self, instance):
        data = {}
        token = CustomTokenObtainPairSerializer.get_token(instance)
        data['refresh'] = str(token)
        data['access'] = str(token.access_token)
        return data

class PasswordResetChangeSerializer(PasswordChangeSerializer):
    old_password = None

    def validate_old_password(self, value):
        return value
    
    def validate(self, attrs):
        OTP.objects.filter(user=self.instance).delete()
        return super().validate(attrs)
