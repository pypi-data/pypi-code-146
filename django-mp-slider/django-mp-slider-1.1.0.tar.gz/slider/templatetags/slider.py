
from django import template
from django.conf import settings

from slider.models import SliderImage


register = template.Library()


@register.inclusion_tag('slider.html')
def render_slider():
    return {'slider_photos': SliderImage.objects.all()}


@register.inclusion_tag('slideshow.html')
def render_slideshow(images, group_name='slideshow', preview_size=None):
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'images': images,
        'preview_size': preview_size,
        'group_name': group_name
    }
