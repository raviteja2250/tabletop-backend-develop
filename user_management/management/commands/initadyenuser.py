""" initadmin command """
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """ Custome command to create default admin"""

    def handle(self, *args, **options):
        user_model = get_user_model()

        # Finding existing user
        existing_user = user_model.objects.filter(
            username=settings.ADYEN_USER['username']).first()
        if existing_user is not None:
            return

        username = settings.ADYEN_USER['username'].replace(' ', '')
        password = settings.ADYEN_USER['password']
        print('Creating account for %s' % (username))
        adyen_user = user_model.objects.create_superuser(
            username=username, password=password)
        adyen_user.is_active = True
        adyen_user.is_staff = False
        adyen_user.is_admin = False
        adyen_user.is_superuser = False
        adyen_user.save()
