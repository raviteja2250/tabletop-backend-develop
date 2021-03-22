from rest_framework.serializers import ModelSerializer

from app_config.models import GeneralConfig


class GeneralConfigSerializer(ModelSerializer):
    """ GeneralConfig seriazlier class """

    class Meta:
        """ Meta subclass """
        model = GeneralConfig
        fields = ('on_maintenance', 'maintenance_due_time',)
