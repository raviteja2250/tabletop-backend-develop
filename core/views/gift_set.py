""" Declear class-based view for exposing GiftSet model """
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.models import GiftSet
from core.serializers import GiftSetSerializer


class GiftSetViewSet(ReadOnlyModelViewSet):
    """ GiftSet viewset """

    queryset = GiftSet.objects.all()
    serializer_class = GiftSetSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
