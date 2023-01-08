from django_kirui.context_processors import DjangoSamonBinding
from django_static_bundler.templatetags.bundled_static import bundled_static


class KiruiBinding(DjangoSamonBinding):
    def bundled_static(self, path):
        return bundled_static(path)
