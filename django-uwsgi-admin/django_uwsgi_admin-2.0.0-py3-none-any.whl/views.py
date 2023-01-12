import os
import time
from datetime import datetime

from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic import View

try:
    import uwsgi
except ImportError:
    uwsgi = None


class BaseUwsgiPage(TemplateView):
    """
    uWSGI Status View
    """

    title = 'uWSGI'

    def get_template_names(self):
        if uwsgi:
            return self.template_name
        else:
            return 'uwsgi/unavailable.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied

        opts = {
            'app_label': 'django_uwsgi',
            'app_config': {'verbose_name': 'uWSGI'},
            'verbose_name_plural': self.title,
        }

        kwargs.update(
            **admin.site.each_context(self.request),
            **opts,
            opts=opts,
            cl={'opts': opts},
        )
        if uwsgi:
            context = self.get_context_data(**kwargs)
        else:
            context = kwargs

        return self.render_to_response(context)


class UwsgiStatus(BaseUwsgiPage):
    template_name = 'uwsgi/status.html'
    title = _('Status')

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            stats=[
                ('loop', uwsgi.loop),
                ('masterpid', str(uwsgi.masterpid())),
                ('started_on', datetime.fromtimestamp(uwsgi.started_on)),
                ('now', datetime.now()),
                ('buffer_size', uwsgi.buffer_size),
                ('total_requests', uwsgi.total_requests()),
                ('numproc', uwsgi.numproc),
                ('cores', uwsgi.cores),
                ('cwd', os.getcwd()),
                ('logsize', uwsgi.logsize()),
                ('spooler_pid', uwsgi.spooler_pid() if uwsgi.opt.get('spooler') else _('disabled')),
                ('threads', _('enabled') if uwsgi.has_threads else _('disabled')),
            ],
            **kwargs,
        )


class UwsgiOptions(BaseUwsgiPage):
    template_name = 'uwsgi/options.html'
    title = _('Options')

    def get_context_data(self, **kwargs):
        return super().get_context_data(options={key: repr(value).lstrip('b') for key, value in uwsgi.opt.items()}, **kwargs)


class UwsgiMagicTable(BaseUwsgiPage):
    template_name = 'uwsgi/magic_table.html'
    title = _('Magic Table')

    def get_context_data(self, **kwargs):
        return super().get_context_data(magic_table=uwsgi.magic_table, **kwargs)


class UwsgiWorkers(BaseUwsgiPage):
    template_name = 'uwsgi/workers.html'
    title = _('Workers')

    def get_context_data(self, **kwargs):
        workers = uwsgi.workers()
        total_load = time.time() - uwsgi.started_on
        for w in workers:
            w['running_time'] = w['running_time'] / 1000
            w['avg_rt'] = w['avg_rt'] / 1000
            w['load'] = w['running_time'] / total_load / 10 / len(workers)
            w['last_spawn'] = datetime.fromtimestamp(w['last_spawn'])

        return super().get_context_data(workers=workers, **kwargs)


class UwsgiApplications(UwsgiWorkers):
    template_name = 'uwsgi/applications.html'
    title = _('Applications')


class UwsgiJobs(BaseUwsgiPage):
    template_name = 'uwsgi/jobs.html'
    title = _('Jobs')

    def get_context_data(self, **kwargs):
        return super().get_context_data(options=uwsgi.opt, **kwargs)


class UwsgiActions(BaseUwsgiPage):
    template_name = 'uwsgi/actions.html'
    title = _('Actions')


class RedirectURLMixin:
    redirect_field_name = 'next'

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name, self.request.GET.get(self.redirect_field_name))
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts={
                self.request.get_host(),
            },
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""


class UwsgiCacheClear(RedirectURLMixin, View):
    """
    Clear uWSGI Cache View
    """

    def post(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        if uwsgi is not None and uwsgi.masterpid() > 0:
            uwsgi.cache_clear()
            messages.add_message(request, messages.SUCCESS, _('uWSGI Cache cleared!'), fail_silently=True)
        else:
            messages.add_message(request, messages.ERROR, _('The uWSGI master process is not active'), fail_silently=True)
        return HttpResponseRedirect(self.get_redirect_url() or reverse_lazy('admin:django_uwsgi_actions_changelist'))


class UwsgiReload(RedirectURLMixin, View):
    """
    Reload uWSGI View
    """

    def get(self, request):
        # This method exists in case the reload breaks the connection. If you get an empty response just retry the requests as GET to get
        # the redirect.
        return HttpResponseRedirect(self.get_redirect_url() or reverse_lazy('admin:django_uwsgi_actions_changelist'))

    def post(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        if uwsgi is not None and uwsgi.masterpid() > 0:
            messages.add_message(request, messages.SUCCESS, _('uWSGI reloaded!'), fail_silently=True)
            uwsgi.reload()
        else:
            messages.add_message(request, messages.ERROR, _('The uWSGI master process is not active'), fail_silently=True)
        return HttpResponseRedirect(self.get_redirect_url() or reverse_lazy('admin:django_uwsgi_actions_changelist'))


class UwsgiLog(View):
    """
    uWSGI Log View
    """

    def post(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        if uwsgi is not None:
            uwsgi.log(request.POST.get('log_message'))
            messages.add_message(request, messages.SUCCESS, _('uWSGI Log message has been sent!'), fail_silently=True)
        else:
            messages.add_message(request, messages.ERROR, _('uWSGI is not available!'), fail_silently=True)
        return HttpResponseRedirect(reverse_lazy('admin:django_uwsgi_actions_changelist'))


class UwsgiSignal(View):
    """
    uWSGI Signal View
    """

    def post(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        if uwsgi is not None:
            uwsgi.signal(int(request.POST.get('signal_number')))
            messages.add_message(request, messages.SUCCESS, _('uWSGI signal has been sent!'), fail_silently=True)
        else:
            messages.add_message(request, messages.ERROR, _('uWSGI is not available!'), fail_silently=True)
        return HttpResponseRedirect(reverse_lazy('admin:django_uwsgi_actions_changelist'))
