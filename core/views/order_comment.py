""" Declear class-based view for exposing OrderComment model """
from rest_framework import mixins, viewsets

from core.models import OrderComment
from core.serializers import OrderCommentSerializer


class OrderCommentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """ OrderComment viewset """

    queryset = OrderComment.objects.all()
    serializer_class = OrderCommentSerializer
    filterset_fields = ['order', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('type')
