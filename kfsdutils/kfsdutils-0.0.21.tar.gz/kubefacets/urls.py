from django.urls import path, include

urlpatterns = [
    path('docs/', include('kubefacets.apps.docs.urls')),
]
