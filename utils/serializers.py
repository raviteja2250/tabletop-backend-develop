"""
    Define abstract classes that are used for drf-serializers
"""
from django.core.exceptions import ValidationError

from rest_framework.serializers import ModelSerializer, ListSerializer


class LikeAndUnLikeSerializer(ModelSerializer):
    """ Class to handle model have `number_of_like` and `is_liked_by_user` props """
    class Meta:
        abstract = True

    def like(self):
        """ Like the obj """
        return

    def unlike(self):
        """ Unlike the obj """
        return

    def to_representation(self, instance):
        result = super().to_representation(instance)

        # Check the post is liked by the user?
        request = self.context.get("request", None)
        if request:
            user = request.user
            result['is_liked'] = instance.is_liked_by_user(user=user)

        return result


class BulkCreateListSerializer(ListSerializer):
    """ Class to create many object with `bulk_create()` """

    def create(self, validated_data):
        # Create muplti-objects,
        # the `.create() of child serializer should return instance without saving
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except Exception as err:
            raise ValidationError(err) from Exception

        return result


class BulkCreateModelSerializer(ModelSerializer):
    """ Model class to create many object with `bulk_create()` """
    class Meta:
        list_serializer_class = BulkCreateListSerializer

    def create(self, validated_data):
        if isinstance(getattr(self, '_kwargs', {}).get("data", None), dict):
            return super().create(validated_data)

        return self.Meta.model(**validated_data)  # pylint: disable=no-member
