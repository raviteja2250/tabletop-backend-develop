""" initadmin command """
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from user_management.constants.group_permissions import GROUPS


class Command(BaseCommand):
    """ Custome command to create default admin"""

    def handle(self, *args, **options):
        for group_name in GROUPS.keys():
            group, _created = Group.objects.get_or_create(name=group_name)

            # Set permission again in case want to update
            print(' -- Adding group {}'.format(group_name))
            group.permissions.set([])
            for model_name in GROUPS[group_name].keys():
                for action in GROUPS[group_name][model_name]:
                    codename = '{}_{}'.format(
                        action, model_name)
                    try:
                        permissions = Permission.objects.filter(
                            codename=codename)

                        for permission in permissions:
                            group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        pass

            print(' -- Added group {}'.format(group_name))
            group.save()
