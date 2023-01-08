from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.utils.module_loading import import_string

from kirui_devserver.backend.forms import SampleForm
from kirui_devserver.backend.models import Activity


class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.test.client import RequestFactory
        rf = RequestFactory()
        post_request = rf.post('/backend/form/', {'foo': 'bar'})
        form = SampleForm(post_request, instance=Activity.objects.first())
        klass = getattr(settings, 'DJANGO_SAMON_BINDING_CLASS', 'django_kirui.context_processors.DjangoSamonBinding')
        klass = import_string(klass)

        data = get_template('xml/form.html').render(context={'form': form, 'djsamon': klass(post_request)}, request=None, to='psx')
        print(data)
