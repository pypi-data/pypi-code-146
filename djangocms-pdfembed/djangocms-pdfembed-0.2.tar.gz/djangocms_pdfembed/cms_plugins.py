from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import PDFEmbedModel

@plugin_pool.register_plugin
class PDFEmbedPlugin(CMSPluginBase):
    model = PDFEmbedModel
    name = "PDF Embed"
    render_template = "djangocms_pdfembed/pdf_embed.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context