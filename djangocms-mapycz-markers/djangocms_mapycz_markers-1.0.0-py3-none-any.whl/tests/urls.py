"""Urls for tests."""

from cms import views
from cms.constants import SLUG_REGEXP
from django.urls import path, re_path

from djangocms_mapycz_markers.urls import urlpatterns as plugin_urlpatterns

urlpatterns = [
    re_path(r'^(?P<slug>%s)/$' % SLUG_REGEXP, views.details, name='pages-details-by-slug'),
    path('', views.details, {'slug': ''}, name='pages-root'),
] + plugin_urlpatterns
