""" Declear class-based view for exposing Brand model """
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.models import Brand
from core.serializers import BrandSerializer, DetailBrandSerializer


class BrandViewSet(ReadOnlyModelViewSet):
    """ Brand viewset """

    queryset = Brand.objects.filter(is_active=True).order_by(
        'brand_orders__order').distinct()
    serializer_class = BrandSerializer
    filterset_fields = ('name', 'delivery', 'dine_in', 'tags',)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('tags', 'chefs',)
        queryset = queryset.select_related('location')
        return queryset

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()

        if self.action == 'retrieve':
            serializer_class = DetailBrandSerializer

        return serializer_class
