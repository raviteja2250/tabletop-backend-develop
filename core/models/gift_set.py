"""
    Purpose: Declare schema for gift set model.
"""
from django.db import models

from utils.models import TimeStampMixin

from core.models import GiftSetCategory


class GiftSet(TimeStampMixin, models.Model):
    """ ORM class that present the GiftSet table """

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    gift_set_categories = models.ManyToManyField(
        GiftSetCategory, related_name='gift_sets', blank=True)

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'
