""" Decleare serializer class for restAPI base on Category models"""

from rest_framework.serializers import ModelSerializer

from core.models import Category


class CategorySerializer(ModelSerializer):
    """ Category seriazlier class """

    class Meta:
        """ Meta subclass """
        model = Category
        fields = '__all__'
        read_only_fields = ['id']
