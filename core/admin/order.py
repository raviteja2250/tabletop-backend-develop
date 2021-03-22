"""
    Customize the Admin panel for Order
"""
from django.contrib import admin

from core.models import (
    Order, OrderItem,
)


class OrderItemInline(admin.StackedInline):
    """ Class to present the order item as inline in the Order's page """
    model = OrderItem
    extra = 0
    readonly_fields = ('menu_item', 'price', 'quantity',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Override the Order admin page """
    filter_horizontal = ('gift_sets',)
    readonly_fields = ('user', 'paid', 'refunded',
                       'refund_psp_reference', 'payment_psp_reference', 'payment_link',
                       'due_time', 'completed_time', 'received_time',)
    inlines = [
        OrderItemInline
    ]
    list_display = ('id', 'brand', 'type', 'status',)
    list_filter = ('type', 'brand', 'status',)

    def has_add_permission(self, request):
        # This model is used internally
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('brand',)
        return queryset
