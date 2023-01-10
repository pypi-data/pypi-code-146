import admin_utils
from django.contrib import admin
from django.urls import path

from . import views

admin_utils.make_admin_class(
    app_label='django_uwsgi',
    verbose_name_plural='uWSGI Status',
    model_name='status',
    urls=[
        path('', admin.site.admin_view(views.UwsgiStatus.as_view()), name='django_uwsgi_status_changelist'),
        path('reload', admin.site.admin_view(views.UwsgiReload.as_view()), name='django_uwsgi_reload'),
        path('cache_clear', admin.site.admin_view(views.UwsgiCacheClear.as_view()), name='django_uwsgi_cache_clear'),
        path('log', admin.site.admin_view(views.UwsgiLog.as_view()), name='django_uwsgi_log'),
        path('signal', admin.site.admin_view(views.UwsgiSignal.as_view()), name='django_uwsgi_signal'),
    ],
)
