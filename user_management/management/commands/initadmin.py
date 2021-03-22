""" initadmin command """
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """ Custome command to create default admin"""

    def handle(self, *args, **options):
        user_model = get_user_model()
        if user_model.objects.count() == 0:
            for user in settings.ADMIN_USERS:
                username = user['username'].replace(' ', '')
                email = user['email'].replace(' ', '')
                password = user['password']
                print('Creating account for %s (%s)' % (username, email))
                admin = user_model.objects.create_superuser(
                    email=email, username=username, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            pass
