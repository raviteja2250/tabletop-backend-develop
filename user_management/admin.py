""" admin.py """
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.admin import LocationInline

from user_management.models import ProxyUser, AuthSession
from user_management.constants import groups


@admin.register(ProxyUser)
class UserAdmin(BaseUserAdmin):
    """ Customize the User Admin to add user's info """
    readonly_fields = ('phone_number', 'has_finished_onboarding',)
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('id', 'username', 'email', 'phone_number',
                    'first_name', 'last_name', )
    inlines = [
        LocationInline
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))

        for index, fieldset in enumerate(fieldsets):
            if fieldset[0] == 'Personal info':
                fieldsets[index] = (
                    'Personal info',
                    {'fields': ('phone_number', 'first_name', 'last_name', 'email', 'has_finished_onboarding')})
                break

        return fieldsets


admin.site.unregister(Group)


@admin.register(Group)
class GroupsAdmin(admin.ModelAdmin):
    """ Customized the Group admin panel """
    default_groups = [groups.FRONT_DESK_STAFF,
                      groups.KITCHEN_STAFF, groups.CUSTOMER]
    fields = ('name', 'permissions')
    filter_horizontal = ('permissions',)

    # Make sure default groups cannot be deleted, and can be changed permissions only
    def has_delete_permission(self, request, obj=None):
        if obj is None or obj.name in self.default_groups:
            return False
        return True

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.name in self.default_groups:
            return ("name",)
        return []


@admin.register(AuthSession)
class AuthSessionAdmin(admin.ModelAdmin):
    """ Override the AuthSession admin page """
    list_display = ('phone_number', 'otp',)

    def has_module_permission(self, request):
        return settings.ENV == 'dev'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
