""" Decleare serializer class for restAPI base on MenuItem models"""

from rest_framework.serializers import ModelSerializer, ListSerializer, CharField

from core.models import MenuItem
from core.serializers import BrandSerializer, CategorySerializer


class MenuItemListSerializer(ListSerializer):
    """ Class to list menu item with special structure """

    def to_representation(self, data):
        data = super().to_representation(data)

        result = dict()
        for item in data:
            # Get the category data and delete redundant data
            category = item['category']
            category_id = item['category']['id']
            del item['category']

            try:
                result[category_id]['items'].append(item)
            except KeyError:
                # If categories' items is not listed in the dict => create new.
                result[category_id] = {
                    "category": category,
                    "items": [item]
                }

        return list(result.values())


class BaseMenuItemSerializer(ModelSerializer):
    """ MenuItem seriazlier class with base setting """
    price = CharField()

    class Meta:
        """ Meta subclass """
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['id']


class MenuItemSerializer(BaseMenuItemSerializer):
    """ MenuItem seriazlier class """
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        """ Meta subclass """
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['id']
        list_serializer_class = MenuItemListSerializer
