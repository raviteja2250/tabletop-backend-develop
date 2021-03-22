"""
    Purpose: Declare schema for ChefTag model.
"""
from django.db import models


class ChefTag(models.Model):
    """ ORM class that present the ChefTag table """

    # PK
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)
