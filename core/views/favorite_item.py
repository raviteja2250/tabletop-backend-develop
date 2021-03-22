""" Declear class-based view for exposing FavoriteItem model """
from rest_framework import mixins, viewsets

from core.models import FavoriteItem
from core.serializers import FavoriteItemSerializer


class FavoriteItemViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
):

    """ FavoriteItem viewset """

    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        queryset = queryset.select_related('menu_item')
        queryset = queryset.select_related('user')

        return queryset
