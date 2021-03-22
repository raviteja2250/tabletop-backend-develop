
""" Decleare serializer class for restAPI base on ChefTag models"""
from rest_framework.serializers import ModelSerializer

from community.models import ChefTag


class ChefTagSerializer(ModelSerializer):
    """ Chef seriazlier class """

    class Meta:
        """ Meta subclass """
        model = ChefTag
        fields = '__all__'

    def to_representation(self, instance):
        return instance.name
