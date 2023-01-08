from django.http import HttpRequest
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.template.context import make_context
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

from django_kirui.components import KrApp, KrForm
from django_kirui.components.forms import KrField
from samon.environment import Environment
from samon.loaders import FileSystemLoader
from samon.exceptions import TemplateNotFound, TemplateError
from samon.template import Template


class DjangoSamonTemplates(BaseEngine):
    app_dirname = 'templates'

    def __init__(self, params):
        params = params.copy()
        options = params.pop("OPTIONS", {}).copy()
        super().__init__(params)

        self.engine = Environment(loader=FileSystemLoader(search_path=self.template_dirs))
        self.engine.registry.element('kr-app', KrApp)
        self.engine.registry.element('kr-form', KrForm)
        self.engine.registry.element('kr-form-field', KrField)
        self._context_processors = options.pop('context_processors', [])

    @cached_property
    def context_processors(self):
        return tuple(import_string(path) for path in self._context_processors)

    def get_template(self, template_name):
        try:
            return Template(self.engine.get_template(template_name), backend=self)
        except TemplateNotFound as exc:
            raise TemplateDoesNotExist(exc.args, backend=self)
        except TemplateError as exc:
            raise TemplateSyntaxError(exc.args)


class Template:
    DEFAULT_OUTPUT_FORMAT = 'json'

    def __init__(self, template: Template, backend: DjangoSamonTemplates):
        self.template = template
        self.backend = backend
        # TODO: self.origin = ... # https://docs.djangoproject.com/en/3.1/ref/templates/api/#django.template.base.Origin

    def render(self, context: dict = None, request: HttpRequest = None, to: str = 'xml', **kwargs):
        context = make_context(context, request, autoescape=True)

        if request is not None:
            context['request'] = request
            context['csrf_input'] = csrf_input_lazy(request)
            context['csrf_token'] = csrf_token_lazy(request)

            """if request.content_type in ('html/text', 'text/plain', ''):
                output = 'xml'
            else:
                output = 'json'"""

            # Support for django context processors
            for processor in self.backend.context_processors:
                context.update(processor(request))

        # return json.dumps(self.template.root_element.render(context).serialize(output=output))
        return self.template.root_element.render(context).serialize(output=to, **kwargs)
