"""enough URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from enough.api import views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from .views import member_index

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('delegate-test-dns/', views.delegate_test_dns, name='delegate-test-dns'),
    path('delegate-dns/', views.delegate_dns, name='delegate-dns'),
    path('ping/', views.ping, name='ping'),

    url(r'^$', TemplateView.as_view(template_name='visitor/landing-index.html'),
        name='landing_index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^member/$', member_index, name='user_home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
