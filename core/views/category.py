""" Declear class-based view for exposing Category model """
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from core.models import Category
from core.serializers import CategorySerializer
from core.filters import CategoryFilter


class CategoryViewSet(ReadOnlyModelViewSet):
    """ Category viewset """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filterset_class = CategoryFilter
