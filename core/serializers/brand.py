""" Decleare serializer class for restAPI base on Brand models"""

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from core.models import Brand, Category
from core.serializers import CategorySerializer, LocationSerializer


class BrandSerializer(ModelSerializer):
    """ Brand seriazlier class """
    chefs = PrimaryKeyRelatedField(read_only=True, many=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        """ Meta subclass """
        model = Brand
        fields = '__all__'
        read_only_fields = ['id']


class DetailBrandSerializer(BrandSerializer):
    """ Brand seriazlier class """

    class Meta:
        """ Meta subclass """
        model = Brand
        fields = '__all__'
        read_only_fields = ['id']

    def to_representation(self, instance):
        result = super().to_representation(instance)

        active_category_ids = instance.menu_items.values_list(
            'category', flat=True)
        active_categories = Category.objects.filter(pk__in=active_category_ids)

        result['categories'] = CategorySerializer(
            active_categories, many=True).data

        return result
