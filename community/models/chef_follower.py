"""
    Purpose: Declare schema for ChefFollower model.
"""
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import TimeStampMixin

from community.models import Chef


class ChefFollower(TimeStampMixin, models.Model):
    """ ORM class that present the ChefFollower table """
    # Fk
    chef = models.ForeignKey(
        Chef, related_name='followers', on_delete=models.CASCADE, blank=True)

    user = models.ForeignKey(get_user_model(),
                             related_name='followed_chefs',
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = (('chef', 'user'),)
        indexes = [
            models.Index(fields=['user', 'chef', ]),
            models.Index(fields=['user', ]),
        ]
