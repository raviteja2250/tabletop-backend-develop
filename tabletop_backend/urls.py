"""tabletop_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings

import debug_toolbar

from rest_framework import routers
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from tabletop_backend.views import health_check_view
from core.urls import router as core_router
from community.urls import router as community_router
from content_management.urls import router as content_management_router

router = routers.DefaultRouter()
router.registry.extend(core_router.registry)
router.registry.extend(community_router.registry)


if settings.DEBUG:

    urlpatterns = [
        path('', health_check_view),
        path('admin/', admin.site.urls),
        url(r'', include('core.urls')),  # For normal api
        url(r'auth/', include('user_management.urls')),
        url(r'app-config/', include('app_config.urls')),
        path('api/', include(router.urls)),
        path('content-management/', include(content_management_router.urls)),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
else:
    urlpatterns = [
        path('', health_check_view),
        path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
        path('aaaa-dddd-mmmm-iiii-nnnn/', admin.site.urls),
        url(r'', include('core.urls')),  # For normal api
        url(r'auth/', include('user_management.urls')),
        url(r'app-config/', include('app_config.urls')),
        path('api/', include(router.urls)),
        path('content-management/', include(content_management_router.urls)),
    ]


# Config for swagger
if settings.DEBUG or settings.ENV == 'dev':
    # Config for swagger
    SchemaView = get_schema_view(
        openapi.Info(
            title="TableTop's APIs",
            default_version='v1',
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        url(r'^swagger/$', SchemaView.with_ui('swagger',
                                              cache_timeout=0), name='schema-swagger-ui'),
        url(r'^swagger(?P<format>\.json|\.yaml)$',
            SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    ]
