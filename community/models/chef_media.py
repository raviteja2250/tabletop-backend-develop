"""
    Purpose: Declare schema for ChefMedia model.
"""
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import TimeStampMixin, LikeMixin, MediaMixin
from utils.common import create_media_path
from utils.validators.file_validator import FileTypeValidator

from community.models import Chef, ChefTag


def generate_media_path(instance, filename):
    """ Generate the media path for chef-media model """
    return create_media_path('chef-media')(instance, filename)


class ChefMedia(TimeStampMixin, LikeMixin, MediaMixin, models.Model):
    """ ORM class that present the ChefMedia table """

    class Meta:
        verbose_name_plural = "Chef media"

    # PK
    id = models.AutoField(primary_key=True)

    # Fk
    chef = models.ForeignKey(Chef, related_name='media',
                             on_delete=models.CASCADE)
    tags = models.ManyToManyField(ChefTag, related_name='media', blank=True)

    title = models.CharField(max_length=200)
    media = models.FileField(
        upload_to=generate_media_path,
        validators=[FileTypeValidator(
            allowed_types=['image/*', 'video/*'],
        )]
    )

    number_of_view = models.PositiveIntegerField(default=0)


class LikedChefMedia(TimeStampMixin, models.Model):
    """ ORM class that present the LikedChefMedia table """

    # Fk
    media = models.ForeignKey(ChefMedia, related_name='likes',
                              on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),
                             related_name='liked_media',
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = (('media', 'user',),)
        indexes = [
            models.Index(fields=['media', 'user', ]),
            models.Index(fields=['media', ]),
        ]
