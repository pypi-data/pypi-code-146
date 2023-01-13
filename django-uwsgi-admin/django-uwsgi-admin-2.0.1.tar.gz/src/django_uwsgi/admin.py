import admin_utils
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext as _

from . import views

admin_utils.make_admin_class(
    app_label='django_uwsgi',
    verbose_name_plural=_('Actions'),
    model_name='actions',
    urls=[
        path('', admin.site.admin_view(views.UwsgiActions.as_view()), name='django_uwsgi_actions_changelist'),
        path('reload', admin.site.admin_view(views.UwsgiReload.as_view()), name='django_uwsgi_reload'),
        path('cache_clear', admin.site.admin_view(views.UwsgiCacheClear.as_view()), name='django_uwsgi_cache_clear'),
        path('log', admin.site.admin_view(views.UwsgiLog.as_view()), name='django_uwsgi_log'),
        path('signal', admin.site.admin_view(views.UwsgiSignal.as_view()), name='django_uwsgi_signal'),
    ],
)


def register_view(view, name):
    admin_utils.register_view(app_label='django_uwsgi', verbose_name_plural=name, model_name=name.lower().replace(' ', '_'))(view)


register_view(views.UwsgiStatus.as_view(), _('Status'))
register_view(views.UwsgiOptions.as_view(), _('Options'))
register_view(views.UwsgiMagicTable.as_view(), _('Magic Table'))
register_view(views.UwsgiWorkers.as_view(), _('Workers'))
register_view(views.UwsgiApplications.as_view(), _('Applications'))
register_view(views.UwsgiJobs.as_view(), _('Jobs'))
