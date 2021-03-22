""" Declear class-based view for exposing Tag model """
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.models import Tag
from core.serializers import TagSerializer


class TagViewSet(ListModelMixin,
                 GenericViewSet):
    """ Tag viewset """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
