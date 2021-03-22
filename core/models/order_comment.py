"""
    Purpose: Declare schema for comment of an order.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from utils.models import TimeStampMixin

from core.models import Order
from core.constants.order_comment_type import (
    KITCHEN, SERVICE
)


class OrderCommentManager(models.Manager):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        for obj in objs:
            post_save.send(OrderComment, instance=obj, created=True)

            if not obj.user or obj.type:
                continue

            if obj.user.is_kitchen_staff:
                obj.type = KITCHEN

            if obj.user.is_front_desk_staff:
                obj.type = SERVICE

        return super().bulk_create(objs, batch_size, ignore_conflicts)


class OrderComment(TimeStampMixin, models.Model):
    """ ORM class that present the OrderComment table """
    objects = OrderCommentManager()

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name="order_comments", blank=True, null=True
    )
    type = models.CharField(max_length=15, choices=(
        (KITCHEN, 'Kitchen'),
        (SERVICE, 'Service'),
    ), default=KITCHEN)

    comment = models.TextField()

    def __str__(self):
        return str(self.order.id) + ''

    def save(self, *args, **kwargs):
        if not self.user or self.type:
            super().save(*args, **kwargs)

        # pylint: disable=no-member
        if self.user.is_kitchen_staff:
            self.type = KITCHEN

        if self.user.is_front_desk_staff:
            self.type = SERVICE

        super().save(*args, **kwargs)
