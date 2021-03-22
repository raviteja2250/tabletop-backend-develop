""" urls.py """

from django.urls import re_path

from app_config.views import AppConfigView


urlpatterns = [
    re_path(r'', AppConfigView.as_view(),
            name='app_config'),
]
