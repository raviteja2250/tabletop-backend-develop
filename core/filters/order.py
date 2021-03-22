
from django_filters import rest_framework as django_filters

from core.models import Brand, Order, Category
from core.constants.order_status import (
    RECEIVED, REJECTED, ACCEPTED, CHECKED_OUT,
    COOKING, COOKED, READY_TO_SEND,
    PENDING_REJECTION, ON_THE_WAY, COMPLETED
)


class OrderFilter(django_filters.FilterSet):
    """ Customize the filter for Order view """
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all())
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(), label='Category', method='handle_category_filter')
    status = django_filters.MultipleChoiceFilter(
        choices=(
            (CHECKED_OUT, 'Checked out'),
            (RECEIVED, 'Received'),
            (REJECTED, 'Rejected'),
            (PENDING_REJECTION, 'Pending Rejection'),
            (ACCEPTED, 'Accepted'),
            (COOKING, 'Cooking'),
            (COOKED, 'Cooked'),
            (READY_TO_SEND, 'Ready to send'),
            (ON_THE_WAY, 'On the way'),
            (COMPLETED, 'Completed'),
        ),
    )
    created_at__date__ex = django_filters.DateFilter(
        label='Created at exclude date', method='handle_created_at__exc')

    class Meta:
        model = Order
        # fields = ('brand', 'status', 'created_at',)
        fields = {
            'brand': ('exact',),
            'status': ('exact',),
            'created_at': ('date', 'date__gt', 'date__lt', 'date__lte', 'date__gte')
        }

    def handle_created_at__exc(self, queryset, value, *args, **kwargs):
        query_date = args[0]

        if query_date:

            queryset = queryset.filter().exclude(created_at__date=query_date)

        return queryset

    def handle_category_filter(self, queryset, value, *args, **kwargs):
        queried_brands = args[0]

        if queried_brands:
            queryset = queryset.filter(
                order_items__menu_item__category__in=queried_brands).distinct()

        return queryset
