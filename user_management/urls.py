""" urls.py """

from django.urls import re_path

from user_management.views import (
    UserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView,
    RequestOTPView, ConfirmOTPView
)


urlpatterns = [
    re_path(r'^token', CustomTokenObtainPairView.as_view(),
            name='token_obtain_pair'),
    re_path(r'^refresh-token', CustomTokenRefreshView.as_view(),
            name='refresh_token'),
    re_path(r'^phone', RequestOTPView.as_view(),
            name='request_otp'),
    re_path(r'^otp', ConfirmOTPView.as_view(),
            name='confirm_otp'),
    re_path(r'^users', UserViewSet.as_view(),
            name='update_user'),
]
