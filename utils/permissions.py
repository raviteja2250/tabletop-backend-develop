""" permission.py """
import copy

from rest_framework.permissions import DjangoModelPermissions


class DjangoModelPermissionWithAllMethod(DjangoModelPermissions):
    """ Class extend from FullMethod to check the permission on get method too """

    def __init__(self):
        self.perms_map = copy.deepcopy(
            self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
