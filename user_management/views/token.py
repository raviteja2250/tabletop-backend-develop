""" token_obtain_pair.py """
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user_management.serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """ Class to use the custom serializer for get token """
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """ Class to use the custom serializer for refresh token """
    serializer_class = CustomTokenRefreshSerializer
