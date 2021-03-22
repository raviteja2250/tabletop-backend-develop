"""
    Purpose: Declare schema for category model.
"""
from django.db import models

from utils.models import TimeStampMixin


class Category(TimeStampMixin, models.Model):
    """ ORM class that present the Category table """

    # PK
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'
