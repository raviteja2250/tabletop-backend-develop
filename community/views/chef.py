""" Declear class-based view for exposing Chef model """
from django.db.models import Prefetch

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from community.models import Chef
from community.serializers import ChefSerializer, BaseChefSerializer


class ChefViewSet(ReadOnlyModelViewSet):
    """ Chef viewset """
    filterset_fields = ['brands', ]

    queryset = Chef.objects.all()
    serializer_class = ChefSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('brands', 'profile_media',)
        queryset = queryset.prefetch_related(
            Prefetch('brands__tags'),
            Prefetch('brands__chefs'),
        )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return BaseChefSerializer
        return super().get_serializer_class()
