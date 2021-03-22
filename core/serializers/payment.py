""" Decleare serializer class for restAPI base on Tag models"""
import logging

from rest_framework.serializers import ModelSerializer

from core.models import Order, AdyenResponse
from core.constants import order_status

logger = logging.getLogger(__name__)


class OrderPaymentSeriazlier(ModelSerializer):
    """ Payment seriazlier class """

    class Meta:
        """ Meta subclass """
        model = Order

    def complete_payment(self, psp_reference, raw_data=None):
        """ Handle logic when a payment of order is completed """
        if self.instance.paid:
            return

        # Update order's state
        self.instance.status = order_status.RECEIVED
        self.instance.payment_psp_reference = psp_reference
        self.instance.paid = True
        self.instance.save()

        # Store the response from Adyen
        new_adyen_response = AdyenResponse(
            order=self.instance, content=raw_data)
        new_adyen_response.save()

        logger.info('Order %s is paid', str(self.instance.id))

    def refund_payment(self):
        """ Handle logic when a payment of order is completed """
        # Update order's state
        self.instance.refunded = True
        self.instance.save()

        logger.info('Order %s is refunded', str(self.instance.id))
