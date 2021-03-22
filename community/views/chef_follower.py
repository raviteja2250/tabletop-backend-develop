""" Declear class-based view for exposing ChefFollower model """
from rest_framework import mixins, viewsets

from community.models import ChefFollower
from community.serializers import ChefFollowerSerializer


class ChefFollowerViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
):

    """ ChefFollower viewset """

    queryset = ChefFollower.objects.all()
    serializer_class = ChefFollowerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
