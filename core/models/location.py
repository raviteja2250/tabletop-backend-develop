"""
    Purpose: Declare schema for location model.
"""
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import TimeStampMixin
from utils.common import create_media_path
from utils.validators.file_validator import FileTypeValidator


def generate_media_path(instance, filename):
    """ Generate the media path for brand model """
    return create_media_path('location')(instance, filename)


class Location(TimeStampMixin, models.Model):
    """ ORM class that present the Location table """

    # PK
    id = models.AutoField(primary_key=True)

    # FK
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name="locations", blank=True, null=True
    )

    name = models.CharField(max_length=200)
    block_or_street = models.CharField(max_length=300)
    postcode = models.CharField(max_length=50, blank=True, null=True)
    unit_or_building = models.CharField(max_length=300, blank=True, null=True)
    country_code = models.CharField(max_length=3, default="SG")
    is_default = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=generate_media_path,
        validators=[FileTypeValidator(
            allowed_types=['image/*'],
        )], null=True, blank=True
    )

    def __str__(self):
        result = self.name + '( ' + str(self.id) + ' '

        if self.block_or_street:
            result += self.block_or_street

        if self.unit_or_building:
            result += ' - ' + self.unit_or_building

        return result + ' )'
