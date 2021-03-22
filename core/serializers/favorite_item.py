""" Decleare serializer class for restAPI base on FavoriteItem models"""
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.serializers import ModelSerializer, ValidationError

from core.models import FavoriteItem
from core.serializers import MenuItemSerializer


class FavoriteItemSerializer(ModelSerializer):
    """ FavoriteItem seriazlier class """

    class Meta:
        """ Meta subclass """
        model = FavoriteItem
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        favorite_item = FavoriteItem.objects.create(
            user=user, **validated_data)

        return favorite_item

    def validate(self, attrs):
        # Validate user
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user") and not request.user.is_anonymous:
            user = request.user

        if not user:
            raise ValidationError("Favorite item should belong to a user")

        # Validate duplicate item
        item = attrs.get('menu_item', None)
        try:
            FavoriteItem.objects.get(user=user, menu_item=item)
            raise ValidationError(
                "Duplicated favorite item") from ObjectDoesNotExist
        except ObjectDoesNotExist:
            pass

        return attrs

    def to_representation(self, instance):
        result = super().to_representation(instance)

        result['menu_item'] = MenuItemSerializer(instance.menu_item).data

        return result
