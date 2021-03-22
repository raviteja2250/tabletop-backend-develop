""" Decleare serializer class for restAPI base on GiftSet models"""

from rest_framework.serializers import ModelSerializer

from core.models import GiftSet


class GiftSetSerializer(ModelSerializer):
    """ GiftSet seriazlier class """

    class Meta:
        """ Meta subclass """
        model = GiftSet
        fields = '__all__'
        read_only_fields = ['id']
