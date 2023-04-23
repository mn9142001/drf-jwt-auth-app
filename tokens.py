from rest_framework_simplejwt.authentication import JWTAuthentication, AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class PasswordResetAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        if not validated_token.get('type', False) == "reset_password":
            raise AuthenticationFailed(_('Bad Token'), code='user_inactive')
        return super().get_user(validated_token)    


class PasswordResetToken(CustomTokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['type'] = "reset_password"
        return token