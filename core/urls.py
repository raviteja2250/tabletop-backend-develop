""" urls.py """

from django.urls import re_path

from rest_framework.routers import DefaultRouter


from core.views import (
    BrandViewSet,
    CategoryViewSet,
    LocationViewSet,
    MenuItemViewSet,
    OrderViewSet,
    OrderCommentViewSet,
    CookingItemViewSet,
    GiftSetViewSet,
    GiftSetCategoryViewSet,
    PromotionItemViewSet,
    SpecialItemViewSet,
    PaymentCallbackView,
    TimeSlotView,
    TagViewSet,
    FeeViewSet,
    FavoriteItemViewSet,
    DiscountViewSet,
)

router = DefaultRouter()

router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'menu-items', MenuItemViewSet, basename='menu-items')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-comments', OrderCommentViewSet,
                basename='order-comments')
router.register(r'cooking-items', CookingItemViewSet, basename='cooking-items')
router.register(r'gift-set-categories',
                GiftSetCategoryViewSet, basename='gift-set-categories')
router.register(r'gift-sets', GiftSetViewSet, basename='gift-sets')
router.register(r'promotions', PromotionItemViewSet, basename='promotions')
router.register(r'special-items', SpecialItemViewSet, basename='special-items')
router.register(r'tags', TagViewSet, basename='tag-view')
router.register(r'fees', FeeViewSet, basename='fee-view')
router.register(r'discounts', DiscountViewSet, basename='discounts')
router.register(r'favorite-items', FavoriteItemViewSet,
                basename='favorite-items')

urlpatterns = [
    re_path(r'^webhook/$', PaymentCallbackView.as_view()),
    re_path(r'^api/time-slots$', TimeSlotView.as_view()),
]
