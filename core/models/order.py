"""
    Purpose: Declare schema for order model.
"""
from datetime import timedelta, datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from utils.models import TimeStampMixin

from core.models import Location, GiftSet, Brand
from core.constants.order_status import (
    RECEIVED, REJECTED, ACCEPTED, CHECKED_OUT,
    COOKING, COOKED, READY_TO_SEND, FAILED,
    PENDING_REJECTION, ON_THE_WAY, COMPLETED
)
from core.constants.order_type import (
    DINE_IN, DELIVERY, TAKE_AWAY
)
from core.constants.monetary import (
    PERCENT, FLAT
)


class Order(TimeStampMixin, models.Model):
    """ ORM class that present the Order table """

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="orders",
        blank=True,
        null=True
    )  # Set null if user is deleted to preserve sale data.
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, related_name='orders', blank=True, null=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, related_name='orders', null=True)
    gift_sets = models.ManyToManyField(
        GiftSet, related_name='orders', blank=True)

    table_no = models.PositiveIntegerField(blank=True, null=True)
    completed_time = models.DateTimeField(blank=True, null=True)
    received_time = models.DateTimeField(blank=True, null=True)
    due_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=(
        (CHECKED_OUT, 'Checked out'),
        (FAILED, 'Failed'),
        (RECEIVED, 'Received'),
        (REJECTED, 'Rejected'),
        (PENDING_REJECTION, 'Pending Rejection'),
        (ACCEPTED, 'Accepted'),
        (COOKING, 'Cooking'),
        (COOKED, 'Cooked'),
        (READY_TO_SEND, 'Ready to send'),
        (ON_THE_WAY, 'On the way'),
        (COMPLETED, 'Completed'),
    ), default=CHECKED_OUT)
    type = models.CharField(max_length=15, choices=(
        (DINE_IN, 'Dine In'),
        (DELIVERY, 'Delivery'),
        (TAKE_AWAY, 'Take away'),
    ), default=DINE_IN)

    # Attribute for payment
    payment_link = models.URLField(blank=True, null=True)
    payment_psp_reference = models.CharField(
        max_length=50, blank=True, null=True)
    refund_psp_reference = models.CharField(
        max_length=50, blank=True, null=True)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def clean(self):
        if self.type == DINE_IN and self.table_no is None:
            raise ValidationError("Dine in order should have the table No.")

    @property
    def base_price(self):
        """ Return the base price of an order """
        result = 0
        for order_item in self.order_items.all():
            result += order_item.price * order_item.quantity

        return result

    @property
    def total_price(self):
        """ Return the total price of an order """
        result = self.base_price

        # Apply the percent discount on order_item.
        discount = getattr(self, 'discount', None)
        if discount and discount.type == PERCENT:
            for order_item in self.order_items.all():
                if not order_item.no_discount:
                    result -= discount.get_value(order_item.price) * \
                        order_item.quantity

        # Apply the flat discount on whole basket.
        if discount and discount.type == FLAT:
            result -= discount.get_value(result)

        result = result if result > 1.0 else 1.0

        fees = self.fees.all()  # Query one time, then loop to find the gst to prevent hitting db

        result_after_discount = result
        gst_fee = None
        for fee in fees:
            if fee.is_gst:
                gst_fee = fee
                continue

            result += fee.get_value(result_after_discount)

        result_after_fee = result
        if gst_fee:
            result += gst_fee.get_value(result_after_fee)

        return round(result, 2) if result >= 0 else 0

    def save(self, *args, **kwargs):
        if self.status == READY_TO_SEND and not self.completed_time:
            self.completed_time = datetime.now()

        if self.status == RECEIVED and not self.received_time:
            self.received_time = datetime.now()

        used_time_slot = getattr(self, 'used_time_slot', None)
        if self.type != DINE_IN and not self.due_time and used_time_slot:
            self.due_time = datetime(
                year=used_time_slot.date.year,
                month=used_time_slot.date.month,
                day=used_time_slot.date.day,
                hour=used_time_slot.time_slot.time_range.start.hour,
                minute=used_time_slot.time_slot.time_range.start.minute,
            )

            if self.type == DELIVERY:
                self.due_time = self.due_time - timedelta(
                    minutes=used_time_slot.time_slot.brand_time_slot.brand.cooking_time
                )

        super().save(*args, **kwargs)
