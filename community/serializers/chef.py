""" Decleare serializer class for restAPI base on Chef models"""
from django.db.models import Prefetch

from rest_framework.serializers import ModelSerializer

from core.models import MenuItem
from core.serializers import BrandSerializer, BaseMenuItemSerializer

from community.models import ChefProfileMedia

from community.models import Chef


class ChefProfileMediaSerializer(ModelSerializer):
    class Meta:
        """ Meta subclass """
        model = ChefProfileMedia
        fields = ('media', 'media_type')

    def to_representation(self, instance):
        url = instance.media.url
        request = self.context.get('request', None)
        result = super().to_representation(instance)

        if request is not None:
            result['media'] = request.build_absolute_uri(url)

        return result


class BaseChefSerializer(ModelSerializer):
    profile_media = ChefProfileMediaSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        """ Meta subclass """
        model = Chef
        fields = '__all__'
        read_only_fields = ['id']

    def to_representation(self, instance):
        result = super().to_representation(instance)

        # Check user is following this chef
        request = self.context.get('request', None)
        if request and not request.user.is_anonymous:
            result['is_followed'] = instance.is_followed_by_user(request.user)

        return result


class ChefSerializer(BaseChefSerializer):
    """ Chef seriazlier class """
    brands = BrandSerializer(read_only=True, many=True)
    recommended_items = BaseMenuItemSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        """ Meta subclass """
        model = Chef
        fields = '__all__'
        read_only_fields = ['id']
        list_serializer_class = BaseChefSerializer

    def to_representation(self, instance):
        result = super().to_representation(instance)

        # Set recommended_items
        recommended_items = MenuItem.objects.filter(
            brand__in=instance.brands.all()).order_by('?')[:10]
        recommended_items = recommended_items.prefetch_related('tags')
        recommended_items = recommended_items.select_related(
            'category', 'brand',)
        recommended_items = recommended_items.prefetch_related(
            Prefetch('brand__tags'),
            Prefetch('brand__chefs'),
        )

        result['recommended_items'] = BaseMenuItemSerializer(
            recommended_items, many=True).data

        return result
