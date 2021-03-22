""" fee.py """
from django.db import models

from core.models import Brand, Order
from core.models.monetary import Monetary
from core.constants.monetary import PERCENT

from core.constants.order_type import (
    DINE_IN, DELIVERY, TAKE_AWAY
)


class OrderFee(Monetary):
    """ ORM class that present the copy of fee for an order """
    is_gst = models.BooleanField(default=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='fees')


class Fee(Monetary):
    """ ORM class that present the fee table """
    is_gst = models.BooleanField(default=False)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='fees')

    def clone_to_order_fee(self, order_instance):
        """ Convert an instance of Fee into OrderFee """
        new_order_fee = OrderFee(
            value=self.value,
            name=self.name,
            type=self.type,
            is_gst=self.is_gst,
            order_type=self.order_type,
            order=order_instance
        )
        return new_order_fee


class GSTFee(Fee):
    """ ORM class that present the fee table """
    class Meta:
        proxy = True

    def __str__(self):
        return ''

    def save(self, *args, **kwargs):
        """ Overrided save function for GST fee"""
        # Set value for GST fee
        self.is_gst = True
        self.type = PERCENT
        self.name = 'GST'
        self.order_type = [
            DINE_IN, DELIVERY, TAKE_AWAY
        ]

        # Validate the input of value
        self.clean()
        super().save(*args, **kwargs)
