from django.http import HttpResponse
from django.shortcuts import render
from .models import PWASettings
from . import app_settings
from django.contrib.sites.models import Site
from django.conf import settings

def service_worker(request):
    response = HttpResponse(open(app_settings.PWA_SERVICE_WORKER_PATH).read(), content_type='application/javascript')
    return response


def manifest(request):
    pwa_settings = PWASettings.objects().first()
    site = Site.objects.first()
    context = {"settings": pwa_settings, "base_url": settings.BASE_URL}
    # {
    #     setting_name: getattr(app_settings, setting_name)
    #     for setting_name in dir(app_settings)
    #     if setting_name.startswith('PWA_')
    # }
    return render(request, 'manifest.json', context, content_type='application/json')


def offline(request):
    return render(request, "offline.html")
