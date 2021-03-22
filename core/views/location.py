""" Declear class-based view for exposing Location model """
from rest_framework.viewsets import ModelViewSet

from core.models import Location
from core.serializers import LocationSerializer


class LocationViewSet(ModelViewSet):
    """ Location viewset """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            user=self.request.user).order_by('-is_default', '-updated_at')

        return queryset
