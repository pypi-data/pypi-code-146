from django.urls import path

from .views import styleguide

urlpatterns = [
    path('', styleguide, name='styleguide', kwargs={'page': 'index'}),
    path('<str:page>/', styleguide, name='styleguide'),
]
