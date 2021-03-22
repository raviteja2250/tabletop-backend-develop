"""
    Purpose: Declare schema for ChefRecipe model.
"""
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import TimeStampMixin, LikeMixin, MediaMixin
from utils.common import create_media_path
from utils.validators.file_validator import FileTypeValidator

from community.models import Chef


def generate_media_path(instance, filename):
    """ Generate the media path for chefrecipe model """
    return create_media_path('chef-recipe')(instance, filename)


class ChefRecipe(TimeStampMixin, LikeMixin, MediaMixin, models.Model):
    """ ORM class that present the ChefRecipe table """

    # PK
    id = models.AutoField(primary_key=True)

    # Fk
    chef = models.ForeignKey(Chef, related_name='recipes',
                             on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    media = models.FileField(
        upload_to=generate_media_path,
        validators=[FileTypeValidator(
            allowed_types=['image/*', 'video/*'],
        )]
    )
    number_of_view = models.PositiveIntegerField(default=0)
    cooking_item = models.PositiveIntegerField()
    serving = models.PositiveIntegerField()


class ChefRecipeIngredient(models.Model):
    """ ORM class that present the ChefRecipeIngredient table """

    # PK
    id = models.AutoField(primary_key=True)
    ingredient = models.CharField(max_length=500)

    # FK
    recipe = models.ForeignKey(ChefRecipe, related_name='ingredients',
                               on_delete=models.CASCADE)


class ChefRecipeDirection(models.Model):
    """ ORM class that present the ChefRecipeDirection table """

    # PK
    id = models.AutoField(primary_key=True)
    step = models.TextField()

    # FK
    recipe = models.ForeignKey(ChefRecipe, related_name='directions',
                               on_delete=models.CASCADE)


class LikedChefRecipe(TimeStampMixin):
    """ ORM class that present the LikedChefRecipe table """

    # Fk
    recipe = models.ForeignKey(ChefRecipe, related_name='likes',
                               on_delete=models.CASCADE)
    user = models.OneToOneField(get_user_model(),
                                related_name='liked_recipes',
                                on_delete=models.CASCADE)

    class Meta:
        unique_together = (('recipe', 'user',),)
        indexes = [
            models.Index(fields=['recipe', 'user', ]),
            models.Index(fields=['recipe', ]),
        ]
