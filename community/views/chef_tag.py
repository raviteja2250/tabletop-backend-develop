""" Declear class-based view for exposing ChefTag model """
from django.db.models import Count

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from community.models import ChefTag
from community.serializers import ChefTagSerializer
from community.filters import ChefMediaTagFilter, ChefPostTagFilter


class ChefMediaTagViewSet(ReadOnlyModelViewSet):
    """ Chef viewset """
    queryset = ChefTag.objects.annotate(
        num_media=Count('media')).filter(num_media__gt=0)
    serializer_class = ChefTagSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filterset_class = ChefMediaTagFilter


class ChefPostTagViewSet(ReadOnlyModelViewSet):
    """ Chef viewset """
    queryset = ChefTag.objects.annotate(
        num_post=Count('posts')).filter(num_post__gt=0)
    serializer_class = ChefTagSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filterset_class = ChefPostTagFilter
