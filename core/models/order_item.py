"""
    Purpose: Declare schema for order's item model.
"""
from django.db import models
from django.core.validators import MinValueValidator

from utils.models import TimeStampMixin

from core.models import Order, MenuItem


class OrderItemManager(models.Manager):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        for obj in objs:
            obj.price = obj.menu_item.price
            obj.discounted_price = obj.menu_item.price
            obj.no_discount = obj.menu_item.no_discount

        return super().bulk_create(objs, batch_size, ignore_conflicts)


class OrderItem(TimeStampMixin, models.Model):
    """ ORM class that present the OrderItem table """
    objects = OrderItemManager()

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    menu_item = models.ForeignKey(  # Set null if menu_item is deleted to preserve sale data.
        MenuItem, on_delete=models.CASCADE,
        related_name="order_items", blank=True, null=True)
    no_discount = models.BooleanField(default=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items")

    # Used in case we have the promotion, fee, ...
    price = models.FloatField(default=0, validators=[
                              MinValueValidator(0)])
    discounted_price = models.FloatField(default=0, validators=[
        MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.menu_item.name + ' (' + str(self.id) + ') - Order: ' + str(self.order.id)

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price
        self.discounted_price = self.menu_item.price
        self.no_discount = self.menu_item.no_discount
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return round(self.discounted_price * self.quantity, 2)

    def calculate_discounted_price(self, discounts):
        for discount in discounts:
            self.discounted_price = round(
                self.discounted_price - discount.get_value(self.price), 2)
