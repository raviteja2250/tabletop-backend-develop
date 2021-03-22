""" Declear class-based view for exposing Order model """
from django.db.models import Prefetch

from rest_framework import mixins, viewsets

from core.models import Order
from core.serializers import UpdateOrderSerializer, CreateOrderSerializer
from core.filters import OrderFilter


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """ Order viewset """

    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = CreateOrderSerializer
    filterset_class = OrderFilter

    def get_queryset(self):
        if self.request.user.is_customer:
            queryset = super().get_queryset().filter(user=self.request.user)
        else:
            queryset = super().get_queryset()

        queryset = queryset.prefetch_related(
            'fees', 'order_items', 'cooking_items', 'gift_sets', 'comments',)
        queryset = queryset.select_related(
            'location', 'used_time_slot', 'user', 'brand', 'discount',)
        queryset = queryset.prefetch_related(
            Prefetch('brand__tags'),
            Prefetch('brand__chefs'),
            Prefetch('order_items__menu_item'),
            Prefetch('order_items__menu_item__tags')
        )

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = UpdateOrderSerializer
        return serializer_class
