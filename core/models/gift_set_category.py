"""
    Purpose: Declare schema for gift set category model.
"""
from django.db import models

from utils.models import TimeStampMixin

from core.models import MenuItem


class GiftSetCategory(TimeStampMixin, models.Model):
    """ ORM class that present the GiftSetCategory table """

    # PK
    id = models.AutoField(primary_key=True)

    menu_items = models.ManyToManyField(
        MenuItem, related_name='gift_set_categories',  blank=True)

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'
