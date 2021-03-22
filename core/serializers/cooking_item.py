""" Decleare serializer class for restAPI base on CookingItem models"""
from django.core.exceptions import FieldError

from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.exceptions import ValidationError

from core.models import CookingItem
from core.utils.cooking_item_status import validate_cooking_item_status


class CookingItemSerializer(ModelSerializer):
    """ CookingItem seriazlier class """
    name = CharField(
        source="menu_item.name", read_only=True
    )

    class Meta:
        """ Meta subclass """
        model = CookingItem
        fields = '__all__'
        read_only_fields = ['id', 'menu_item', 'order']

    def validate_status(self, value):
        """ Validator for te status field """
        try:
            validate_cooking_item_status(self.instance.status, value)
        except FieldError as field_error:
            raise ValidationError('Status is invalid') from field_error

        return value
