"""
    Purpose: Declare schema for ChefPost model.
"""
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import TimeStampMixin, LikeMixin, MediaMixin
from utils.common import create_media_path
from utils.validators.file_validator import FileTypeValidator

from community.models import Chef, ChefTag


def generate_media_path(instance, filename):
    """ Generate the media path for chef-post model """
    return create_media_path('chef-post')(instance, filename)


class ChefPost(TimeStampMixin, LikeMixin, MediaMixin, models.Model):
    """ ORM class that present the ChefPost table """

    # PK
    id = models.AutoField(primary_key=True)

    # Fk
    chef = models.ForeignKey(Chef, related_name='posts',
                             on_delete=models.CASCADE)
    tags = models.ManyToManyField(ChefTag, related_name='posts', blank=True)

    title = models.CharField(max_length=200)
    content = models.TextField()
    media = models.FileField(
        upload_to=generate_media_path,
        validators=[FileTypeValidator(
            allowed_types=['image/*', 'video/*'],
        )]
    )
    number_of_view = models.PositiveIntegerField(default=0)


class LikedChefPost(TimeStampMixin, models.Model):
    """ ORM class that present the LikedChefPost table """

    # Fk
    post = models.ForeignKey(ChefPost, related_name='likes',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),
                             related_name='liked_post',
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = (('post', 'user',),)
        indexes = [
            models.Index(fields=['post', 'user', ]),
            models.Index(fields=['post', ]),
        ]
