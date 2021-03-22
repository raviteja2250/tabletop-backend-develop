"""
    Purpose: Declare schema for Chef model.
"""
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

from utils.models import TimeStampMixin, MediaMixin
from utils.common import create_media_path
from utils.validators.file_validator import FileTypeValidator

from core.models import Brand


def generate_media_path(instance, filename):
    """ Generate the media path for brand model """
    return create_media_path('chef')(instance, filename)


class Chef(TimeStampMixin, models.Model):
    """ ORM class that present the Chef table """

    # PK
    id = models.AutoField(primary_key=True)

    # Fk
    brands = models.ManyToManyField(Brand, related_name='chefs', blank=True)

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': "A chef with that username already exists.",
        },
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)

    # Profile
    image = models.ImageField(
        upload_to=generate_media_path, null=True, blank=True)
    instagram_account = models.URLField(null=True, blank=True)
    facebook_account = models.URLField(null=True, blank=True)
    twitter_account = models.URLField(null=True, blank=True)
    tiktok_account = models.URLField(null=True, blank=True)

    def __str__(self):
        return 'Chef: ' + self.username + ' (' + str(self.id) + ')'

    def is_followed_by_user(self, user):
        """ Function to check if a user is following the chef"""
        if not hasattr(self, 'followers'):
            return False

        filtered_follower = self.followers.filter(user=user)
        if len(filtered_follower) > 0:
            return True

        return False


class ChefProfileMedia(MediaMixin, models.Model):
    """ ORM class that present the ChefProfileMedia table """
    class Meta:
        verbose_name_plural = "Video/Media"

    # Fk
    chef = models.ForeignKey(
        Chef, related_name='profile_media', on_delete=models.CASCADE, blank=True)

    media = models.FileField(
        upload_to=generate_media_path,
        validators=[FileTypeValidator(
            allowed_types=['image/*', 'video/*'],
        )], null=True, blank=True)
