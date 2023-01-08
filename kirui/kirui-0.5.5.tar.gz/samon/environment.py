from copy import copy

from .registry import registry
from .loaders import BaseLoader
from .parser import DefaultParser
from .template import Template


class Environment:
    DEFAULT_TEMPLATE_CLASS = Template

    def __init__(self, loader: BaseLoader):
        self.loader = loader
        self.registry = copy(registry)
        self.template_class = self.DEFAULT_TEMPLATE_CLASS

    def get_template(self, template_name):
        src, source_path = self.loader.get_source(template_name)
        parser = DefaultParser(environment=self)
        template = parser.parse(src, template_name=template_name)
        template.source_path = source_path

        return template
