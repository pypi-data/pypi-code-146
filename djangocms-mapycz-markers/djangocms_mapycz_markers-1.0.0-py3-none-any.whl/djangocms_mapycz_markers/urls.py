"""URLs required by plugin. Add this into the site urls.py.

urls.py:

from djangocms_mapycz_markers.urls import urlpatterns as plugin_urlpatterns

urlpatterns = [
    ...
] + plugin_urlpatterns
"""
from django.urls import re_path
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    # The language_code parameter is necessary due to the cache of some browsers that do not reload the same URL.
    re_path(r'^(?P<language_code>[a-z]{2})-jsi18n/mapycz-markers/$', JavaScriptCatalog.as_view(
            packages=['djangocms_mapycz_markers']), name='mapycz_markers_js'),
]
