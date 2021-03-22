""" confirm_otp.py """
import logging

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


from user_management.serializers import ConfirmOTPSerializer, RequestOTPSerializer

logger = logging.getLogger(__name__)


class RequestOTPView(GenericAPIView):
    """ Class to interact with external authentication endpoint """
    authentication_classes = []
    permission_classes = []
    serializer_class = RequestOTPSerializer

    def post(self, request):
        """ function for post request """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.request_otp()
        return Response(serializer.data, status=HTTP_200_OK)


class ConfirmOTPView(GenericAPIView):
    """ Class to interact with external authentication endpoint """
    authentication_classes = []
    permission_classes = []
    serializer_class = ConfirmOTPSerializer

    def __init__(self, *args, **kwargs):
        self._validated_data = {}
        super().__init__(*args, **kwargs)

    def post(self, request):
        """ Handle post request """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.confirm_otp()
        return Response(serializer.data, status=HTTP_200_OK)
