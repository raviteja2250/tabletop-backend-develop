""" Declear class-based view for exposing ChefMedia model """
from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from utils.views import ViewHandlerModeMixin, LikeHandlerModeMixin

from community.models import ChefMedia
from community.serializers import ChefMediaSerializer


class ChefMediaViewSet(ViewHandlerModeMixin,
                       LikeHandlerModeMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """ Chef viewset """
    filterset_fields = ['chef', ]

    queryset = ChefMedia.objects.all()
    serializer_class = ChefMediaSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('chef')
        queryset = queryset.prefetch_related('tags',)
        return queryset
