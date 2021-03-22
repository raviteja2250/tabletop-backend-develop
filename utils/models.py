"""
    Define abstract classes that are used for models
"""

from django.db import models

from utils.common import is_video, is_image, get_file_mine
from utils.constants.file_type import VIDEO, IMAGE

from utils.validators.file_validator import FileTypeValidator


class TimeStampMixin(models.Model):
    """ Abstract class contains the created_at and updated_at file """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ Class' meta"""
        abstract = True


class LikeMixin:
    """ Abstract class for models contain `likes` """
    @property
    def number_of_like(self):
        """ Computed property, return the number of like """
        if not hasattr(self, 'likes'):
            return 0

        return len(self.likes.all())

    def is_liked_by_user(self, user):
        """ Check if a user is liked this media """
        if not hasattr(self, 'likes'):
            return False

        for like in self.likes.all():  # Avoid hit db
            if like.user.pk == user.pk:
                return True

        return False


class MediaMixin(models.Model):
    """ Abstract class for models contain `media` """
    media = models.FileField(
        validators=[FileTypeValidator(
            allowed_types=['image/*', 'video/*'],
        )]
    )
    media_type = models.CharField(max_length=15, choices=(
        (VIDEO, 'Video'),
        (IMAGE, 'Image'),
    ), default='', blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """ Return the type of media """
        if not self.media:
            super().save(*args, **kwargs)

        mine = get_file_mine(self.media.file)

        if is_video(mine=mine):
            self.media_type = VIDEO

        if is_image(mine):
            self.media_type = IMAGE

        super().save(*args, **kwargs)
