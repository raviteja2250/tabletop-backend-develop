from django.contrib import admin

from community.models import (
    Chef, ChefTag, ChefPost, ChefMedia, ChefProfileMedia,
    ChefRecipe, ChefRecipeDirection, ChefRecipeIngredient
)


@admin.register(ChefTag)
class ChefTagAdmin(admin.ModelAdmin):
    """ Override the ChefTag admin page """

    def has_module_permission(self, request):
        return False


class ChefProfileMediaInline(admin.TabularInline):
    """ Class to present the ChefProfileMedia as inline """
    model = ChefProfileMedia
    readonly_fields = ('media_type',)
    extra = 0


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    """ Override the Chef admin page """
    filter_horizontal = ('brands',)
    inlines = [ChefProfileMediaInline]


@admin.register(ChefPost)
class ChefPostAdmin(admin.ModelAdmin):
    """ Override the ChefPost admin page """
    list_filter = ('chef', )
    filter_horizontal = ('tags',)
    readonly_fields = ('media_type', 'number_of_like', 'number_of_view', )
    list_display = ('id', 'title', 'chef', 'number_of_like', 'number_of_view',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('chef')
        queryset = queryset.prefetch_related('tags', 'likes',)
        return queryset


@admin.register(ChefMedia)
class ChefMediaAdmin(admin.ModelAdmin):
    """ Override the ChefPost admin page """
    list_filter = ('chef', )
    filter_horizontal = ('tags',)
    readonly_fields = ('media_type', 'number_of_view', 'number_of_like',)
    list_display = ('id', 'title', 'chef', 'number_of_view', 'number_of_like')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('chef')
        queryset = queryset.prefetch_related('tags', 'likes',)
        return queryset


class ChefRecipeIngredientInline(admin.TabularInline):
    """ Class to present the ChefRecipeIngredient as inline """
    model = ChefRecipeIngredient
    extra = 1


class ChefRecipeDirectionInline(admin.TabularInline):
    """ Class to present the ChefRecipeDirection as inline """
    model = ChefRecipeDirection
    extra = 1


@admin.register(ChefRecipe)
class ChefRecipeAdmin(admin.ModelAdmin):
    """ Override the ChefPost admin page """
    list_filter = ('chef', )
    readonly_fields = ('media_type', 'number_of_like', 'number_of_view',)
    inlines = [ChefRecipeIngredientInline, ChefRecipeDirectionInline]
    list_display = ('id', 'title', 'chef', 'number_of_like', 'number_of_view',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('chef')
        queryset = queryset.prefetch_related(
            'ingredients', 'directions', 'likes',)

        return queryset
