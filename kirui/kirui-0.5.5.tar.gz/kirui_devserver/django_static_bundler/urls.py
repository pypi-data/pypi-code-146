from django.urls import path

from . import views

urlpatterns = [
    path('<path:path>', views.bundle_static_file, name='bundle-static-file'),
]

app_name = 'django_static_bundler'
