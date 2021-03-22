
"""
    Customize the Admin panel for Brand
"""
from django.contrib import admin

from nested_admin.nested import NestedModelAdmin, NestedTabularInline

from core.forms import (
    FeeFormSet, GSTFeeForm, GSTFeeFormSet
)
from core.models import (
    Brand,
    MenuItem,
    TimeSlot,
    Discount,
    Fee,
    GSTFee,
    BrandTimeSlot
)


class MenuItemInline(NestedTabularInline):
    """ Class to present the menu item as inline in the Brand's page """
    model = MenuItem
    extra = 1

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('tags')
        return queryset


class TimeSlotInline(NestedTabularInline):
    """ Class to present the timeslot as inline in the Brand's page """
    model = TimeSlot
    extra = 1
    fields = (
        'time_range', 'capacity'
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('time_range')
        return queryset


class BrandTimeSlotInline(NestedTabularInline):
    """ Class to present the brand timeslot as inline in the Brand's page """
    model = BrandTimeSlot
    extra = 1
    inlines = [
        TimeSlotInline
    ]


class FeeInline(NestedTabularInline):
    """ Class to present the fee as inline in the Brand's page """
    model = Fee
    formset = FeeFormSet
    extra = 0
    exclude = ('is_gst',)


class GSTInline(NestedTabularInline):
    """ Class to present the fee as inline in the Order's page """
    model = GSTFee
    form = GSTFeeForm
    formset = GSTFeeFormSet
    extra = 1
    max_num = 1
    can_delete = False
    verbose_name_plural = "GST"


class DiscountInline(NestedTabularInline):
    """ Class to present the discount as inline in the Brand's page """
    model = Discount
    extra = 0


@admin.register(Brand)
class BrandAdmin(NestedModelAdmin):
    """ Override the Brand admin page """
    fields = (
        'is_active', 'name', 'description', 'location', 'cooking_time',
        'delivery_time', 'logo', 'menu_item_placeholder', 'media', 'media_type',
        'abbreviation', 'foreground_colour', 'background_colour', 'secondary_colour',
        'delivery', 'dine_in',
        'tags',
    )
    readonly_fields = ('media_type',)
    filter_horizontal = ('tags',)
    inlines = [
        DiscountInline,
        FeeInline,
        GSTInline,
        MenuItemInline,
        BrandTimeSlotInline
    ]
