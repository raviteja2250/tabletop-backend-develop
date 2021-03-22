""" payments.py """
import logging

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication

from core.models import Order
from core.permissions import IsAdyenUser
from core.serializers import OrderPaymentSeriazlier

logger = logging.getLogger(__name__)


class PaymentCallbackView(APIView):
    """ Viewset to listen the notification when the order is paid """
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [IsAdyenUser]

    def _handle_payment_complete(self, notification_item, request_data):
        if notification_item['merchantReference'] and notification_item['success']:
            # Finding existing order
            try:
                order_id = int(notification_item['merchantReference'])
                order = Order.objects.get(pk=order_id)

                serializer = OrderPaymentSeriazlier(order)
                serializer.complete_payment(
                    psp_reference=notification_item['pspReference'],
                    raw_data=request_data
                )
            except (ValueError, ObjectDoesNotExist) as ext:
                raise ext

    def _handle_refund_complete(self, notification_item):
        if notification_item['pspReference'] and notification_item['success']:
            try:
                # Finding existing order
                refund_psp_reference = notification_item['pspReference']
                order = Order.objects.get(
                    refund_psp_reference=refund_psp_reference)

                serializer = OrderPaymentSeriazlier(order)
                serializer.refund_payment()
            except (ValueError, ObjectDoesNotExist) as ext:
                raise ext

    def post(self, request):
        """ Listen the notification form adyen """
        logger.info(
            'New request to webhook endpoint with data: %s', str(request.data))

        notification_items = request.data.get('notificationItems', None)
        if not notification_items or len(notification_items) == 0:
            logger.info('Webhook - Missing notificationItems field')
            return Response("[accepted]", status=status.HTTP_400_BAD_REQUEST)

        notification_req_item = notification_items[0].get(
            'NotificationRequestItem', None)
        if not notification_req_item:
            logger.info('Webhook - Missing NotificationRequestItem field')
            return Response("[accepted]", status=status.HTTP_400_BAD_REQUEST)

        try:
            if notification_req_item['eventCode'] == 'AUTHORISATION':
                self._handle_payment_complete(
                    notification_req_item, request.data)
            if notification_req_item['eventCode'] == 'CANCEL_OR_REFUND':
                self._handle_refund_complete(notification_req_item)
        except (ValueError, KeyError, ObjectDoesNotExist) as err:
            logger.error('Webhook\'s error: %s', str(err))
            return Response("[accepted]", status=status.HTTP_400_BAD_REQUEST)

        return Response("[accepted]", status=status.HTTP_200_OK)
