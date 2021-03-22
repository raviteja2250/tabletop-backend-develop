""" Decleare serializer class for restAPI base on ChefRecipe models"""
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework.serializers import ModelSerializer, SlugRelatedField

from utils.serializers import LikeAndUnLikeSerializer

from community.models import ChefRecipe, LikedChefRecipe


class ChefRecipeSerializer(LikeAndUnLikeSerializer, ModelSerializer):
    """ Chef seriazlier class """
    ingredients = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='ingredient'
    )
    directions = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='step'
    )

    class Meta:
        """ Meta subclass """
        model = ChefRecipe
        fields = (tuple((f.name for f in ChefRecipe._meta.fields)) +
                  ('number_of_like', 'directions', 'ingredients', 'media_type'))
        read_only_fields = ['id', 'number_of_like', 'number_of_view', ]

    @transaction.atomic
    def like(self):
        """ Like the post """
        request = self.context.get("request", None)
        if request.user.is_anonymous:
            return

        _, created = LikedChefRecipe.objects.get_or_create(
            recipe=self.instance, user=request.user)

        if not created:
            # if there is a record, means user liked this media
            raise ValidationError('User liked this object')

    @transaction.atomic
    def unlike(self):
        """ Unlike the post """
        request = self.context.get("request", None)
        if request.user.is_anonymous:
            return

        try:
            LikedChefRecipe.objects.get(
                recipe=self.instance, user=request.user).delete()
        except ObjectDoesNotExist as err:
            raise ValidationError('User hasn\'t liked this object') from err
