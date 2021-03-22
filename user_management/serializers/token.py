""" Decleare serializer class for Token"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import update_last_login

from rest_framework_simplejwt.utils import datetime_to_epoch
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from user_management.serializers import UserSerializer


class GetLifeTime():
    """ Class to support token views """
    @staticmethod
    def get_lifetime(user):
        """
            Get token's lifetime based on user's role
        """
        # Give the expiry time by base-role
        if user.is_customer:
            return settings.CUSTOMER_TOKEN_LIFETIME

        return settings.STAFF_TOKEN_LIFETIME


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, GetLifeTime):
    """ Class to handle the token """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = kwargs.get('data', {}).get('user', None)
        if user and isinstance(user, get_user_model()):
            self.user = user

            # Delete old fields because we have the user, we don't need to validate
            del self.fields[self.username_field]
            del self.fields['password']

    def validate(self, attrs):
        try:
            if self.user:
                if api_settings.UPDATE_LAST_LOGIN:
                    update_last_login(None, self.user)
        except AttributeError:
            super().validate(attrs)

        refresh_token = self.get_token(self.user)
        access_token = refresh_token.access_token

        # Give the expiry time by base-role
        token_lifetime = self.get_lifetime(self.user)

        access_token.set_exp(from_time=refresh_token.current_time,
                             lifetime=token_lifetime)
        access_token.payload['exp'] = datetime_to_epoch(
            access_token.current_time + token_lifetime)

        return {
            'refresh': str(refresh_token),
            'access': str(access_token),
            'access_token_expiry': int(token_lifetime.total_seconds()),
            'user_data': UserSerializer(self.user).data
        }

    def to_representation(self, instance):
        return instance


class CustomTokenRefreshSerializer(TokenRefreshSerializer, GetLifeTime):
    """ Class to handle the token """

    def validate(self, attrs):
        data = super().validate(attrs)

        # Generate the new access token
        refresh_token = RefreshToken(attrs['refresh'])
        access_token = refresh_token.access_token

        user_id = access_token[api_settings.USER_ID_CLAIM]
        user = get_user_model().objects.filter(pk=user_id).first()

        if not user:
            raise ValidationError({'user': 'User not found'})

        # Give the expiry time by base-role
        token_lifetime = self.get_lifetime(user)

        access_token.set_exp(from_time=refresh_token.current_time,
                             lifetime=token_lifetime)
        access_token.payload['exp'] = datetime_to_epoch(
            access_token.current_time + token_lifetime)

        return {
            **data,
            'access': str(access_token),
            'access_token_expiry': int(token_lifetime.total_seconds())
        }
