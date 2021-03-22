""" Decleare serializer class for restAPI base on ChefPost models"""
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from rest_framework.serializers import ModelSerializer

from utils.serializers import LikeAndUnLikeSerializer

from community.models import ChefPost, LikedChefPost


class ChefPostSerializer(LikeAndUnLikeSerializer, ModelSerializer):
    """ Chef seriazlier class """

    class Meta:
        """ Meta subclass """
        model = ChefPost
        fields = (tuple((f.name for f in ChefPost._meta.fields)) +
                  ('number_of_like', 'media_type'))
        read_only_fields = ['id', 'number_of_like', 'number_of_view', ]

    @transaction.atomic
    def like(self):
        """ Like the post """
        request = self.context.get("request", None)
        if request.user.is_anonymous:
            return

        _, created = LikedChefPost.objects.get_or_create(
            post=self.instance, user=request.user)

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
            LikedChefPost.objects.get(
                post=self.instance, user=request.user).delete()
        except ObjectDoesNotExist as err:
            raise ValidationError('User hasn\'t liked this object') from err
