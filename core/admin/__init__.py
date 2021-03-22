""" admin.py: Using for model that don't need too much custom in admin panel """

from django.contrib import admin


from core.models import (
    Category, Location,
    MenuItem, OrderItem,
    OrderComment, CookingItem,
    GiftSet, GiftSetCategory, TimeRange,
    Discount, Tag, Fee,
    FavoriteItem, AdyenResponse,
)

from .brand import BrandAdmin
from .order import OrderAdmin

admin.site.register(Tag)
admin.site.register(Category)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """ Override the MenuItem admin page """
    filter_horizontal = ('tags',)


@admin.register(GiftSetCategory)
class GiftSetCategoryAdmin(admin.ModelAdmin):
    """ Override the GiftSetCategory admin page """
    filter_horizontal = ('menu_items',)


@admin.register(GiftSet)
class GiftSetAdmin(admin.ModelAdmin):
    """ Override the GiftSet admin page """
    filter_horizontal = ('gift_set_categories',)


@admin.register(CookingItem)
class CookingItemAdmin(admin.ModelAdmin):
    """ Override the CookingItem admin page """
    readonly_fields = ('order', 'menu_item',)

    def has_add_permission(self, request):
        # This model is used internally
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('menu_item')
        queryset = queryset.select_related('order')
        return queryset


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """ Override the OrderItem admin page """

    readonly_fields = ('price',)

    def has_add_permission(self, request):
        # This model is used internally
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('menu_item')
        queryset = queryset.select_related('order')
        return queryset


class LocationInline(admin.TabularInline):
    """ Class to present the location as inline """
    model = Location
    extra = 1


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """ Override the Location admin page """
    readonly_fields = ('user', 'country_code',)


@admin.register(FavoriteItem)
class FavoriteItemAdmin(admin.ModelAdmin):
    """ Override the FavoriteItem admin page """

    def has_add_permission(self, request):
        # This model should be added by user
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('menu_item')
        queryset = queryset.select_related('user')
        return queryset


@admin.register(TimeRange)
class TimeRangeAdmin(admin.ModelAdmin):
    """ Override the TimeRange admin page """

    def has_module_permission(self, request):
        return False


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    """ Override the Fee admin page """

    def has_module_permission(self, request):
        return False


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """ Override the Discount admin page """

    def has_module_permission(self, request):
        return False


@admin.register(AdyenResponse)
class AdyenResponseAdmin(admin.ModelAdmin):
    """ Override the AdyenResponse admin page """
    list_display = ('order',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(OrderComment)
class OrderCommentAdmin(admin.ModelAdmin):
    """ Override the OrderComment admin page """
    readonly_fields = ('user', 'order',)

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('order')
        return queryset
