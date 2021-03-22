from django.contrib import admin

from app_config.models import GeneralConfig


@admin.register(GeneralConfig)
class GeneralConfigAdmin(admin.ModelAdmin):
    """
        Override the GeneralConfig admin page
        => We initialize only 1 config entry => No add/delete
     """

    def has_add_permission(self, *args, **kwargs):
        return not GeneralConfig.objects.exists()

    def has_delete_permission(self, *args, **kwargs):
        return False
