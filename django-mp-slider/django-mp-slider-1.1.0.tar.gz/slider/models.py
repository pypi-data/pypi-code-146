
from django.db import models
from django.utils.translation import gettext_lazy as _

from ordered_model.models import OrderedModel


class SliderImage(OrderedModel):

    title = models.CharField(_('Title'), blank=True, max_length=255)

    file = models.ImageField(
        _("File"), upload_to='slider_images', max_length=255)

    url = models.URLField(_('Url'), max_length=255, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order', 'id', )
        verbose_name = _('Slider image')
        verbose_name_plural = _('Slider images')
