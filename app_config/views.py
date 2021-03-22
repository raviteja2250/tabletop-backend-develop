""" Declear class-based view for exposing Tag model """
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from app_config.models import GeneralConfig
from app_config.serializers import GeneralConfigSerializer


class AppConfigView(APIView):
    """ AppConfigView
        - The API for configuration of mobile app
        - We use the base APIView because we might have many serializers for each type of config
            and this API combines all config, not for specific model
    """

    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        """ Return all config of mobile application """
        # If config not found, maybe we can't init data
        # let create the new one with default value
        general_config_list = GeneralConfig.objects.all()

        if len(general_config_list) > 0:
            general_config = general_config_list[0]
        else:
            general_config = GeneralConfig.objects.create()

        serializer = GeneralConfigSerializer(general_config)
        return Response(serializer.data, status=HTTP_200_OK)
