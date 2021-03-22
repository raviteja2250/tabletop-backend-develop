"""
    Purpose: Declare schema for cooking item model.
"""
from django.db import models

from utils.models import TimeStampMixin

from core.models import Order, MenuItem
from core.constants.cooking_status import (
    COOKING, COOKED, PICKEDUP
)


class CookingItem(TimeStampMixin, models.Model):
    """ ORM class that present the CookingItem table """

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.SET_NULL, related_name="cooking_items", blank=True, null=True)  # Set null if menu_item is deleted to preserve sale data.
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="cooking_items")

    status = models.CharField(max_length=10, choices=(
        (COOKING, 'Cooking'),
        (COOKED, 'Cooked'),
        (PICKEDUP, 'Picked Up'),
    ), default=COOKING)

    def __str__(self):
        name = self.menu_item.name if self.menu_item else ''
        return name + ' (' + str(self.id) + ') - Order: ' + str(self.order.id)
