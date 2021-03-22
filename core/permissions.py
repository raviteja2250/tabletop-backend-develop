""" Customize the permission for whole app """
from django.conf import settings

from rest_framework.permissions import BasePermission


class IsAdyenUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.username == settings.ADYEN_USER['username'])
