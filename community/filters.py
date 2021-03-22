
from django_filters import rest_framework as django_filters

from community.models import Chef


class ChefMediaTagFilter(django_filters.FilterSet):
    """ Customize the filter for Order view """

    chef = django_filters.ModelChoiceFilter(
        queryset=Chef.objects.all(), label='chef', method='handle_chef_filter')

    def handle_chef_filter(self, queryset, value, *args, **kwargs):
        return queryset.filter(media__chef=args[0])


class ChefPostTagFilter(django_filters.FilterSet):
    """ Customize the filter for Order view """

    chef = django_filters.ModelChoiceFilter(
        queryset=Chef.objects.all(), label='chef', method='handle_chef_filter')

    def handle_chef_filter(self, queryset, value, *args, **kwargs):
        return queryset.filter(posts__chef=args[0])
