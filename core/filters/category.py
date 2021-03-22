
from django_filters import rest_framework as django_filters

from core.models import Brand


class CategoryFilter(django_filters.FilterSet):
    """ Customize the filter for Order view """
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all(), label='Brand', method='handle_brand_filter')

    def handle_brand_filter(self, queryset, value, *args, **kwargs):
        queried_brands = args[0]

        if queried_brands:
            queryset = queryset.filter(
                menu_items__brand__in=queried_brands).distinct()

        return queryset
