""" Decleare serializer class for restAPI base on Location models"""

from rest_framework.serializers import ModelSerializer

from core.models import Location


class LocationSerializer(ModelSerializer):
    """ Location seriazlier class """

    class Meta:
        """ Meta subclass """
        model = Location
        fields = '__all__'
        read_only_fields = ['id', 'country_code']

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user") and not request.user.is_anonymous:
            user = request.user

        location = Location.objects.create(
            user=user, **validated_data)

        return location
