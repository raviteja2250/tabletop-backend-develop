""" Declear class-based view for exposing CookingItem model """
from rest_framework import mixins, viewsets

from core.models import CookingItem
from core.serializers import CookingItemSerializer


class CookingItemViewSet(
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet
):

    """ CookingItem viewset
        - Create/Delele API is not published, cooking item is handled internally
    """

    queryset = CookingItem.objects.all()
    serializer_class = CookingItemSerializer
    filterset_fields = ['order', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('menu_item',)
        return queryset.order_by('menu_item__name', 'created_at')
