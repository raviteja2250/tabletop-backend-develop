"""
    Purpose: Declare schema for brand model.
"""
from django.db import models

from colorfield.fields import ColorField

from utils.common import create_media_path
from utils.models import TimeStampMixin, MediaMixin
from utils.validators.file_validator import FileTypeValidator

from core.models import Tag, Location
from core.constants.time_slot import COOKING_TIME_AS_MINUTES, DELIVERY_TIME_AS_MINUTES


def generate_media_path(instance, filename):
    """ Generate the media path for brand model """
    return create_media_path('brand')(instance, filename)


class Brand(TimeStampMixin, MediaMixin, models.Model):
    """ ORM class that present the Brand table """

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    tags = models.ManyToManyField(
        Tag, related_name="brands", blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, related_name='brand', blank=True, null=True)

    name = models.CharField(max_length=200)
    description = models.TextField(
        max_length=1000, blank=True, null=True)
    abbreviation = models.CharField(
        max_length=5, default='', blank=True, null=True)

    secondary_colour = ColorField(
        default='#FFFFFF', blank=True, null=True)
    background_colour = ColorField(default='#FFFFFF', blank=True, null=True)
    foreground_colour = ColorField(default='#000000', blank=True, null=True)

    logo = models.ImageField(
        upload_to=generate_media_path, null=True, blank=True)
    menu_item_placeholder = models.ImageField(
        upload_to=generate_media_path, null=True, blank=True)
    media = models.FileField(
        upload_to=generate_media_path,
        validators=[FileTypeValidator(
            allowed_types=['image/*', 'video/*'],
        )], null=True, blank=True)
    delivery = models.BooleanField(default=True)
    dine_in = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    delivery_time = models.PositiveIntegerField(
        default=DELIVERY_TIME_AS_MINUTES, help_text='As minutes')
    cooking_time = models.PositiveIntegerField(
        default=COOKING_TIME_AS_MINUTES, help_text='As minutes')

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'
