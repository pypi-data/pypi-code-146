from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from kfsdutils.apps.docs.views.apibrowser import APIBrowserView

urlpatterns = (
    [
        path('schema/', SpectacularAPIView.as_view(), name='schema-api'),
        path("", APIBrowserView.as_view(), name="schema-browser"),
    ]
)
