""" Declear class-based view for exposing Category model """
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.models import Fee
from core.serializers import FeeSerializer, FeeWithBrandIDSerializer


class FeeViewSet(ReadOnlyModelViewSet):
    """ Category viewset """

    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    filterset_fields = ('brand', )
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list' and self.request.query_params.get('brand', None):
            return FeeSerializer  # we don't need return brand if query by brand
        return FeeWithBrandIDSerializer
