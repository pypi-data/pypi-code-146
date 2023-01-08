from django.urls import path, re_path, include


urlpatterns = [
    path('backend/', include('kirui_devserver.backend.urls', namespace='backend')),
    path('brython/', include('django_brython.urls', namespace='brython')),
    path('bundler/', include('django_static_bundler.urls')),
]
