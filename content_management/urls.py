""" urls.py """

from rest_framework.routers import DefaultRouter

from content_management.views import (
    BrandCategoryOrderViewSet, BrandMenuItemOrderViewSet, BrandOrderViewSet
)

router = DefaultRouter()

router.register(r'brand-category-orders',
                BrandCategoryOrderViewSet, basename='brand-category-orders')
router.register(r'brand-menuitem-orders', BrandMenuItemOrderViewSet,
                basename='brand-menuitem-orders')
router.register(r'brand-orders', BrandOrderViewSet,
                basename='brand-menuitem-orders')
