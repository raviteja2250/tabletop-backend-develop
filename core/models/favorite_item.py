"""
    Purpose: Declare schema for favorite's item model.
"""
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import TimeStampMixin

from core.models import MenuItem


class FavoriteItem(TimeStampMixin, models.Model):
    """ ORM class that present the FavoriteItem table """

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE, related_name="favorite_items")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name="favorite_items", blank=True, null=True
    )

    def __str__(self):
        return self.menu_item.name + ' (' + str(self.id) + ')'

    class Meta:
        unique_together = (('menu_item', 'user'),)
        indexes = [
            models.Index(fields=['user', 'menu_item', ]),
            models.Index(fields=['user', ]),
        ]
