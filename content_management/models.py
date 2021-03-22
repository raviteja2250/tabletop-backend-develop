"""
    Purpose: Declare schema for brand model.
"""
from django.db import models

from core.models import Brand, MenuItem, Category


class BrandOrder(models.Model):
    """ ORM class that present the order of Brand when displaying """

    # FK
    brand = models.ForeignKey(
        Brand, related_name="brand_orders", on_delete=models.CASCADE, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('brand', 'order',),)
        indexes = [
            models.Index(fields=['brand', ]),
        ]


class BrandMenuItemOrder(models.Model):
    """ ORM class that present the order of MenuItem when displaying in a brand """

    # FK
    brand = models.ForeignKey(
        Brand, related_name="brand_menuitem_orders", on_delete=models.CASCADE, blank=True)
    menu_item = models.ForeignKey(
        MenuItem, related_name="brand_menuitem_orders", on_delete=models.CASCADE, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('menu_item', 'brand',),
                           ('menu_item', 'brand', 'order'),)
        indexes = [
            models.Index(fields=['menu_item', ]),
        ]


class BrandCategoryOrder(models.Model):
    """ ORM class that present the order of MenuItem when displaying in a brand """

    # FK
    brand = models.ForeignKey(
        Brand, related_name="brand_category_orders", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="brand_category_orders", on_delete=models.CASCADE)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('category', 'brand',),
                           ('category', 'brand', 'order'),)
        indexes = [
            models.Index(fields=['category', ]),
        ]
