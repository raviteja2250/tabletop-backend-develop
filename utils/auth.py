""" Create the custom auth backend for some special cases """

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings

from utils.exceptions import HasNotFinishedOnboarding


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(
                _('Token contained no recognizable user identification')) from KeyError

        user_model = get_user_model()
        try:
            user = user_model.objects.get(
                **{api_settings.USER_ID_FIELD: user_id})
        except user_model.DoesNotExist:
            raise AuthenticationFailed(
                _('User not found'), code='user_not_found') from user_model.DoesNotExist

        if not user.is_active:
            raise AuthenticationFailed(
                _('User is inactive'), code='user_inactive')

        if not user.has_finished_onboarding and not user.is_admin:
            raise HasNotFinishedOnboarding(detail={
                'detail': 'User hasn\'t finished the onboarding',
                'onboarding_session': user.onboarding_session
            })

        return user
