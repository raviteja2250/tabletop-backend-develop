""" urls.py """

from rest_framework.routers import DefaultRouter


from community.views import (
    ChefViewSet, ChefPostViewSet,
    ChefMediaViewSet, ChefRecipeViewSet,
    ChefMediaTagViewSet, ChefPostTagViewSet, ChefFollowerViewSet,
)

router = DefaultRouter()

router.register(r'chefs', ChefViewSet, basename='chefs')
router.register(r'chef-posts', ChefPostViewSet, basename='chef-posts')
router.register(r'chef-media', ChefMediaViewSet, basename='chef-media')
router.register(r'chef-recipes', ChefRecipeViewSet, basename='chef-recipes')
router.register(r'chef-media-tags', ChefMediaTagViewSet,
                basename='chef-media-tags')
router.register(r'chef-post-tags', ChefPostTagViewSet,
                basename='chef-post-tags')
router.register(r'chef-followers', ChefFollowerViewSet,
                basename='chef-followers')
