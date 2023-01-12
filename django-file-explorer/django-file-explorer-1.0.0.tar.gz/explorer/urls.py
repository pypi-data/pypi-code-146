from django.urls import path

from . import views
from .admin import explorer_admin

urlpatterns = [
    path('admin/', explorer_admin.urls),
    path('about', views.About.as_view(), name='explorer-about'),
    path('', views.Explorer.as_view(), name='explorer-main'),

]
