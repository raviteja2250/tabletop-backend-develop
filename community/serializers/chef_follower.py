
""" Decleare serializer class for restAPI base on ChefFollower models"""
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from community.models import ChefFollower
from community.serializers import BaseChefSerializer


class ChefFollowerSerializer(ModelSerializer):
    """ Chef seriazlier class """

    class Meta:
        """ Meta subclass """
        model = ChefFollower
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        follower = ChefFollower.objects.create(
            user=user, **validated_data)

        return follower

    def validate(self, attrs):
        # Validate user
        request = self.context.get("request")
        if request.user.is_anonymous:
            raise AuthenticationFailed()

        # Validate duplicate item
        chef = attrs.get('chef', None)
        try:
            ChefFollower.objects.get(user=request.user, chef=chef)
            raise ValidationError(
                "User followed this chef") from ObjectDoesNotExist
        except ObjectDoesNotExist:
            pass

        return attrs

    def to_representation(self, instance):
        result = super().to_representation(instance)

        result['chef'] = BaseChefSerializer(instance.chef).data

        return result
