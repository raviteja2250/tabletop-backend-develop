"""
    Purpose: Declare schema for discount model.
"""
from django.db import models
from django.core.exceptions import ValidationError

from multiselectfield import MultiSelectField

from utils.models import TimeStampMixin

from core.constants.monetary import (
    PERCENT, FLAT
)
from core.constants.order_type import (
    DINE_IN, DELIVERY, TAKE_AWAY
)


class Monetary(TimeStampMixin, models.Model):
    """ ORM class that present the Discount table """

    # PK
    id = models.AutoField(primary_key=True)

    value = models.FloatField()
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    type = models.CharField(max_length=10, choices=(
        (PERCENT, 'Percent'),
        (FLAT, 'Flat Value'),
    ), default=FLAT)
    order_type = MultiSelectField(choices=(
        (DINE_IN, 'Dine In'),
        (DELIVERY, 'Delivery'),
        (TAKE_AWAY, 'Take away'),
    ), blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'

    def clean(self):
        if not self.value:
            # This case will handle automatically
            return

        if self.value < 0:
            raise ValidationError("Value should be positive number")

        if self.type == PERCENT and self.value > 100:
            raise ValidationError(
                "Value as percent should not be greater than 100")

    def get_value(self, price):
        """ Get the actual value of discount """
        if self.type == PERCENT:
            return (self.value / 100) * price

        if self.type == FLAT:
            return self.value

        return 0
