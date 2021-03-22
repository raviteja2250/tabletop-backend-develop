""" Decleare serializer class for restAPI base on Tag models"""

from django.core.exceptions import ValidationError

from utils.serializers import BulkCreateListSerializer, BulkCreateModelSerializer

from content_management.models import BrandCategoryOrder, BrandMenuItemOrder, BrandOrder


# Classes for BrandMenuItemOrder


class BrandMenuItemOrderListSerializer(BulkCreateListSerializer):
    """ Class to list menu item order """

    def create(self, validated_data):
        # Delete the old record to prevent duplication.
        brand_ids = list(set(map(lambda x: x['brand'].id, validated_data)))
        menu_item_ids = list(
            set(map(lambda x: x['menu_item'].id, validated_data)))
        BrandMenuItemOrder.objects.filter(
            brand__id__in=brand_ids, menu_item__id__in=menu_item_ids).delete()

        return super().create(validated_data)


class BrandMenuItemOrderSerializer(BulkCreateModelSerializer):
    """ BrandMenuItemOrder seriazlier class """

    class Meta:
        """ Meta subclass """
        model = BrandMenuItemOrder
        fields = '__all__'
        validators = []
        list_serializer_class = BrandMenuItemOrderListSerializer

    def validate(self, attrs):
        if attrs['menu_item'].brand != attrs['brand']:
            raise ValidationError(
                {'menu_item': 'menu_item doesn\'t belong to brand'})

        return attrs

    def create(self, validated_data):
        if isinstance(getattr(self, '_kwargs', {}).get("data", None), dict):
            BrandMenuItemOrder.objects.filter(
                brand=validated_data['brand'], menu_item=validated_data['menu_item']).delete()

        return super().create(validated_data)


# Classes for BrandCategoryOrder


class BrandCategoryOrderListSerializer(BulkCreateListSerializer):
    """ Class to list menu item order """

    def create(self, validated_data):
        # Delete the old record to prevent duplication.
        brand_ids = list(set(map(lambda x: x['brand'].id, validated_data)))
        category_ids = list(
            set(map(lambda x: x['category'].id, validated_data)))
        BrandCategoryOrder.objects.filter(
            brand__id__in=brand_ids, category__id__in=category_ids).delete()

        return super().create(validated_data)


class BrandCategoryOrderSerializer(BulkCreateModelSerializer):
    """ BrandCategoryOrder seriazlier class """

    class Meta:
        """ Meta subclass """
        model = BrandCategoryOrder
        fields = '__all__'
        validators = []
        list_serializer_class = BrandCategoryOrderListSerializer

    def validate(self, attrs):
        menu_items = attrs['category'].menu_items.all()

        is_belong = False
        for menu_item in menu_items:
            if menu_item.brand == attrs['brand']:
                is_belong = True
                break

        if not is_belong:
            raise ValidationError(
                {'category': 'category doesn\'t belong to brand'})

        return attrs

    def create(self, validated_data):
        if isinstance(getattr(self, '_kwargs', {}).get("data", None), dict):
            BrandCategoryOrder.objects.filter(
                brand=validated_data['brand'], category=validated_data['category']).delete()

        return super().create(validated_data)


# Classes for BrandCategoryOrder


class BrandOrderListSerializer(BulkCreateListSerializer):
    """ Class to list brand order """

    def create(self, validated_data):
        # Delete the old record to prevent duplication.
        brand_ids = list(set(map(lambda x: x['brand'].id, validated_data)))
        BrandOrder.objects.filter(brand__id__in=brand_ids).delete()

        return super().create(validated_data)


class BrandOrderSerializer(BulkCreateModelSerializer):
    """ BrandOrder seriazlier class """

    class Meta:
        """ Meta subclass """
        model = BrandOrder
        fields = '__all__'
        validators = []
        list_serializer_class = BrandOrderListSerializer

    def create(self, validated_data):
        if isinstance(getattr(self, '_kwargs', {}).get("data", None), dict):
            BrandOrder.objects.filter(
                brand=validated_data['brand'], category=validated_data['category']).delete()

        return super().create(validated_data)
