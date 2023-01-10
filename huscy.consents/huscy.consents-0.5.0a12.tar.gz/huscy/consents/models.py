from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Consent(models.Model):
    name = models.CharField(max_length=128)
    text_fragments = models.JSONField()

    def __str__(self):
        return self.name


class ConsentFile(models.Model):
    consent = models.ForeignKey(Consent, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    filehandle = models.FileField()


class ConsentCategory(models.Model):
    name = models.CharField(max_length=128)


class BaseTextFragment(models.Model):
    element_contenttype = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    element_id = models.PositiveIntegerField()
    properties = GenericForeignKey('element_contenttype', 'element_id')

    order = models.PositiveIntegerField()

    class Meta:
        abstract = True


class TemplateTextFragment(BaseTextFragment):
    category = models.ForeignKey(ConsentCategory, on_delete=models.CASCADE,
                                 related_name='template_text_fragments')

    class Meta:
        ordering = 'order',


class Paragraph(models.Model):
    template_name = 'consents/text_fragments/paragraph.html'

    text = models.TextField()
    boldface = models.BooleanField(default=False)


class Header(models.Model):
    template_name = 'consents/text_fragments/header.html'

    class SIZE(models.IntegerChoices):
        H2 = 2, 'h2'
        H3 = 3, 'h3'
        H4 = 4, 'h4'
        H5 = 5, 'h5'

    text = models.CharField(max_length=255)
    size = models.IntegerField(choices=SIZE.choices, default=SIZE.H2)


class Checkbox(models.Model):
    template_name = 'consents/text_fragments/checkbox.html'

    text = models.TextField()
    required = models.BooleanField(default=False)
