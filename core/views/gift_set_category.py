""" Declear class-based view for exposing GiftSetCategory model """
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.models import GiftSetCategory
from core.serializers import GiftSetCategorySerializer


class GiftSetCategoryViewSet(ReadOnlyModelViewSet):
    """ GiftSetCategory viewset """

    queryset = GiftSetCategory.objects.all()
    serializer_class = GiftSetCategorySerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
