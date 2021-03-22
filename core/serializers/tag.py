""" Decleare serializer class for restAPI base on Tag models"""

from rest_framework.serializers import ModelSerializer

from core.models import Tag


class TagSerializer(ModelSerializer):
    """ Tag seriazlier class """

    class Meta:
        """ Meta subclass """
        model = Tag
        fields = '__all__'

    def to_representation(self, instance):
        return instance.name
