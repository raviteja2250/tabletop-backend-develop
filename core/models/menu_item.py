"""
    Purpose: Declare schema for menu's item model.
"""
from django.db import models
from django.core.validators import MinValueValidator

from utils.models import TimeStampMixin
from utils.common import create_media_path

from core.models import Brand, Category, Tag


def generate_media_path(instance, filename):
    """ Generate the media path for menuitem model """
    return create_media_path('menu_item')(instance, filename)


class MenuItem(TimeStampMixin, models.Model):
    """ ORM class that present the MenuItem table """

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="menu_items")
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="menu_items")
    tags = models.ManyToManyField(
        Tag, related_name="menu_items", blank=True)

    name = models.CharField(max_length=200)
    description = models.TextField(
        max_length=1000, blank=True, null=True)
    image = models.ImageField(
        upload_to=generate_media_path, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to=generate_media_path, null=True, blank=True)
    price = models.FloatField(default=0, validators=[
                              MinValueValidator(0.01)])
    signature_dish = models.BooleanField(default=False)
    promotion = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    no_discount = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'
