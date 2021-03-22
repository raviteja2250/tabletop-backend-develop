""" fee.py """
from django.db import models

from core.models import Brand, Order
from core.models.monetary import Monetary


class OrderDiscount(Monetary):
    """ ORM class that present the copy of discount for an order """

    # FK
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='discount')
    code = models.CharField(max_length=30, null=True, blank=True)


class Discount(Monetary):
    """ ORM class that present the Discount table """

    # FK
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='discounts')
    code = models.CharField(max_length=30, null=True, blank=True)
    is_auto = models.BooleanField(default=False)

    def clone_to_order_discount(self, order_instance):
        """ Convert an instance of Discount into OrderDiscount """
        new_order_discount = OrderDiscount(
            value=self.value,
            name=self.name,
            type=self.type,
            order_type=self.order_type,
            code=self.code,
            order=order_instance
        )
        return new_order_discount
