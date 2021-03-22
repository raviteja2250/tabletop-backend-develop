""" Decleare serializer class for restAPI base on Order Items models"""

from rest_framework.serializers import ModelSerializer, CharField

from core.models import OrderItem
from core.serializers import BaseMenuItemSerializer


class OrderItemSerializer(ModelSerializer):
    """ OrderItem seriazlier class """
    price = CharField(read_only=True, required=False)

    class Meta:
        """ Meta subclass """
        model = OrderItem
        fields = ['id', 'menu_item', 'no_discount',
                  'price', 'discounted_price', 'final_price', 'quantity']
        read_only_fields = ['id', 'price']

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['menu_item'] = BaseMenuItemSerializer(instance.menu_item).data

        return result
