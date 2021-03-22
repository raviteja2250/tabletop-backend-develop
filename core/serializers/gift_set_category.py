""" Decleare serializer class for restAPI base on GiftSetCategory models"""

from rest_framework.serializers import ModelSerializer

from core.models import GiftSetCategory


class GiftSetCategorySerializer(ModelSerializer):
    """ GiftSetCategory seriazlier class """

    class Meta:
        """ Meta subclass """
        model = GiftSetCategory
        fields = '__all__'
        read_only_fields = ['id']
