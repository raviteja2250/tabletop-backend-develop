""" Declear class-based view for exposing ChefRecipe model """
from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from utils.views import ViewHandlerModeMixin, LikeHandlerModeMixin
from community.models import ChefRecipe
from community.serializers import ChefRecipeSerializer


class ChefRecipeViewSet(ViewHandlerModeMixin,
                        LikeHandlerModeMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """ Chef viewset """
    filterset_fields = ['chef', ]

    queryset = ChefRecipe.objects.all()
    serializer_class = ChefRecipeSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('chef')
        queryset = queryset.prefetch_related('ingredients', 'directions',)
        return queryset
