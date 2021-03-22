""" Decleare serializer class for restAPI base on montary models"""

from rest_framework.serializers import ModelSerializer

from core.models import Discount, Fee


class DiscountSerializer(ModelSerializer):
    """ Discount seriazlier class """

    class Meta:
        """ Meta subclass """
        model = Discount
        fields = ('id', 'name', 'description', 'code', 'value',
                  'is_auto', 'type', 'order_type',)


class FeeSerializer(ModelSerializer):
    """ Fee seriazlier class for use internal in other APIs"""

    class Meta:
        """ Meta subclass """
        model = Fee
        fields = ('id', 'name', 'description', 'value', 'type', 'order_type',)


class FeeWithBrandIDSerializer(ModelSerializer):
    """ Fee seriazlier class to return in fee API"""

    class Meta:
        """ Meta subclass """
        model = Fee
        fields = ('id', 'brand', 'description', 'name',
                  'value', 'type', 'order_type',)
