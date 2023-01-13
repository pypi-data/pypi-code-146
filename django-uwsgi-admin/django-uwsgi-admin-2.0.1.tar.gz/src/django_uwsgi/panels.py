from logging import getLogger

from debug_toolbar.panels import Panel
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .views import UwsgiWorkers

try:
    import uwsgi
except ImportError:
    uwsgi = None

logger = getLogger(__name__)


class UwsgiWorkersPanel(Panel):
    nav_title = title = _('uWSGI Workers')
    template = 'uwsgi/common/workers.html'

    @property
    def nav_subtitle(self):
        if uwsgi:
            return _('Version %s, %d Workers') % (str(uwsgi.version.decode()), int(uwsgi.numproc))
        else:
            return _('uWSGI is missing 😣')

    @property
    def has_content(self):
        return uwsgi

    def generate_stats(self, request, response):
        if uwsgi:
            view = UwsgiWorkers()
            view.setup(request)
            try:
                self.record_stats(view.get_context_data())
            except Exception as exc:
                logger.exception('Failed generating UwsgiWorkersPanel stats: %s', exc)


class UwsgiActionsPanel(Panel):
    nav_title = title = _('uWSGI Actions')
    template = 'uwsgi/panels/actions.html'

    @property
    def has_content(self):
        return False

    def generate_stats(self, request, response):
        self.record_stats({'request': request})

    @property
    def nav_subtitle(self):
        if uwsgi:
            return render_to_string(self.template, **self.get_stats())
        else:
            return _('uWSGI is missing 😣')
