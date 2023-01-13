from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerFileField
from django.db import models

class PDFEmbedModel(CMSPlugin):
    height = models.CharField(max_length=10, default='500px')
    width = models.CharField(max_length=10, default='100%')
    pdf = FilerFileField(
        verbose_name='PDF',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    @property
    def pdf_src(self):
        # picture can be empty, for example when the image is removed from filer
        # in this case we want to return an empty string to avoid #69
        if not self.pdf:
            return ''
        # return the original, unmodified picture
        else:
            return self.pdf.url