""" initadmin command """
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from user_management.constants.groups import CUSTOMER


class Command(BaseCommand):
    """ Custome command to create default admin"""

    def handle(self, *args, **options):
        user_model = get_user_model()

        # Finding existing user
        username = settings.DEMO_USER['username'].replace(' ', '')
        phone_number = settings.DEMO_USER['phone_number']
        last_name = settings.DEMO_USER['last_name']
        first_name = settings.DEMO_USER['first_name']

        existing_user = user_model.objects.filter(
            phone_number=phone_number).first()
        if existing_user is not None:
            return

        print('Creating account for %s' % (username))
        demo_user = user_model.objects.create_superuser(
            username=username, phone_number=phone_number,
            last_name=last_name, first_name=first_name)

        demo_user.is_active = True
        demo_user.is_staff = False
        demo_user.is_admin = False
        demo_user.is_superuser = False
        demo_user.save()

        # Add user to group
        group = group, _created = Group.objects.get_or_create(name=CUSTOMER)
        demo_user.groups.add(group)
