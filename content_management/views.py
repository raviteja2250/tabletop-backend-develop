""" Declear class-based view for exposing Tag model """
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from utils.views import BulkCreateModeMixin

from content_management.models import BrandMenuItemOrder, BrandCategoryOrder, BrandOrder
from content_management.serializers import (
    BrandCategoryOrderSerializer, BrandMenuItemOrderSerializer, BrandOrderSerializer
)


class BrandCategoryOrderViewSet(BulkCreateModeMixin,
                                GenericViewSet):
    """ BrandCategoryOrder viewset """

    queryset = BrandCategoryOrder.objects.all()
    serializer_class = BrandCategoryOrderSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class BrandMenuItemOrderViewSet(BulkCreateModeMixin,
                                GenericViewSet):
    """ BrandMenuItemOrder viewset """

    queryset = BrandMenuItemOrder.objects.all()
    serializer_class = BrandMenuItemOrderSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)


class BrandOrderViewSet(BulkCreateModeMixin,
                        GenericViewSet):
    """ BrandOrder viewset """

    queryset = BrandOrder.objects.all()
    serializer_class = BrandOrderSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
