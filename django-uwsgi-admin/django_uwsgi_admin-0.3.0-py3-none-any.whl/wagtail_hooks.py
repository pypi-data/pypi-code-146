from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.site_summary import SummaryItem

try:
    import uwsgi
except ImportError:
    pass


class UwsgiSummaryItem(SummaryItem):
    order = 800
    template_name = 'uwsgi/wagtail_dashboard_item.html'

    def get_context_data(self, parent_context):
        workers = int(uwsgi.numproc) if uwsgi else 0
        return {'workers': workers}


@hooks.register('construct_homepage_summary_items')
def add_uwsgi_summary_item(request, items):
    items.append(UwsgiSummaryItem(request))


class UwsgiMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.is_staff or request.user.is_superuser


@hooks.register('register_settings_menu_item')
def register_uwsgi_menu_item():
    return UwsgiMenuItem(_('uWSGI Status'), reverse_lazy('admin:django_uwsgi_status_changelist'), classnames='icon icon-cogs', order=800)
