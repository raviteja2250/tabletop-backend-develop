""" Declear class-based view for exposing MenuItem model """
from django.db.models import Prefetch

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.models import MenuItem
from core.serializers import MenuItemSerializer


class MenuItemViewSet(ReadOnlyModelViewSet):
    """ MenuItem viewset """

    queryset = MenuItem.objects.filter(active=True).order_by(
        'category__brand_category_orders__order',
    ).distinct().order_by(
        'brand_menuitem_orders__order',
    ).distinct()
    serializer_class = MenuItemSerializer
    filterset_fields = ('brand', 'category', 'tags')
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('tags')
        queryset = queryset.select_related('category')
        queryset = queryset.select_related('brand')
        queryset = queryset.prefetch_related(
            Prefetch('brand__tags'),
            Prefetch('brand__chefs'),
        )
        return queryset
