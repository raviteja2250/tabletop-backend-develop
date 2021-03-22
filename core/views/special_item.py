""" Declear class-based view for exposing MenuItem model """
from core.models import MenuItem
from core.views import MenuItemViewSet


class SpecialItemViewSet(MenuItemViewSet):
    """ Viewset that represent the MenuItem with signature_dish flag """

    # Special items is for delivery type.
    queryset = MenuItem.objects.filter(
        signature_dish=True,
        active=True,
        brand__delivery=True
    ).order_by(
        'category__brand_category_orders__order',
    ).distinct().order_by(
        'brand_menuitem_orders__order',
    ).distinct()
