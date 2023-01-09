import json
import re
from typing import List, Tuple, Union

import jinja2
import jinja2.ext
from django.conf import settings
from django.contrib.messages import get_messages
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import date, linebreaks_filter, linebreaksbr, time
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.safestring import SafeText, mark_safe
from markupsafe import Markup
from wagtail.models import Page, Site
from webpack_loader.templatetags.webpack_loader import render_bundle


def add_form_class(bound_field, new_classes):
    """Add a class to a django form field widget"""
    attrs = bound_field.field.widget.attrs
    classes = sorted(set(attrs.get('class', '').split() + new_classes.split()))
    attrs['class'] = ' '.join(classes)
    return bound_field


def add_form_attributes(bound_field, attributes={}):
    """Add 1 or more attributes to a django form field widget"""
    bound_field.field.widget.attrs.update(attributes)
    return bound_field


def include_static(path):
    """
    Include the contents of a file that has been compiled into the static directory
    """
    fullpath = finders.find(path)
    if fullpath is None:
        raise ValueError("Could not find file %s" % path)

    with open(fullpath, "r") as f:
        return f.read()


def debug_variable(variable):
    """Print all the fields available on a variable"""
    return format_html('<pre>{}</pre>', dir(variable))


def url(name, *args, **kwargs):
    """Reverse a URL name. Alias of ``django.core.urlresolvers.reverse``"""
    return reverse(name, args=args or None, kwargs=kwargs or None)


@jinja2.pass_context
def site_root(context):
    """Get the root page for the site"""
    # This lookup will be cached on the intermediary objects, so this will only
    # hit the DB once per request
    request = context['request']
    return Site.find_for_request(request).root_page.specific


def svg_inline(name):
    """
    Inline an SVG image. SVG images are expected to be a template, not kept in
    the static files
    """
    return mark_safe(render_to_string('svgs/%s.svg' % name))


@jinja2.pass_context
def breadcrumbs(context, page=None):
    """Print the top navigation menu for this site"""
    request = context.get('request')
    root = site_root(context)
    if page is None:
        page = context.get('page')
    ancestors = page.get_ancestors().filter(depth__gte=root.depth)

    return Markup(render_to_string('tags/breadcrumbs.html', {
        'page': page,
        'ancestors': ancestors,
        'request': request,
    }))


def model_classname(model_or_instance):
    """
    Generate a CSS class name from a Page model

    Usage::

        <html class="{{ self|model_classname }}">
    """
    if isinstance(model_or_instance, Page):
        model_or_instance = model_or_instance.content_type.model_class()

    try:
        meta = model_or_instance._meta
        return 'page-{0}-{1}'.format(meta.app_label, meta.model_name)
    except AttributeError:
        return ''


@jinja2.pass_context
def messages(context):
    """Get any messages from django.contrib.messages framework"""
    return get_messages(context.get('request'))


def json_dumps(value):
    """
    Dump the value to a JSON string. Useful when sending values to JavaScript
    """
    return Markup(json.dumps(value, cls=DjangoJSONEncoder))


@jinja2.pass_context
def qs(context, get=None, **kwargs):
    """
    Update a querydict with new values, and return it as a URL encoded string.
    Pass in the current ``request.GET``, and any items to set as keyword
    arguments. If a key has a value of ``None``, that key is removed from the
    querydict.

    The querydict is grabbed from ``request`.GET` in the context by default,
    but an alternative can be provided as the first positional argument.

    >>> request.GET.urlencode()
    "page=1&foo=bar"
    >>> qs(request.GET, page=2, baz="quux", foo=None)
    "page=2&baz=quux"
    """
    if get is None:
        get = context['request'].GET

    get = get.copy()
    for key, value in kwargs.items():
        if value is None:
            # Delete keys if value is None
            get.pop(key, None)
        else:
            get[key] = value
    return get.urlencode()


not_digit_re = re.compile(r'[^0-9+]+')


def tel(value):
    return 'tel:{}'.format(not_digit_re.sub('-', value).strip('-'))


def source_tag(image, media, normal_spec, retina_spec):
    return format_html(
        '<source media="{media}" srcset="{normal_image_url}, {retina_image_url} 2x">',
        media=media,
        normal_image_url=image.get_rendition(normal_spec).url,
        retina_image_url=image.get_rendition(retina_spec).url,
    )


def render_honeypot_field():
    return Markup(render_to_string('honeypot/honeypot_field.html', {
        'fieldname': settings.HONEYPOT_FIELD_NAME,
        'value': ''
    }))


@jinja2.pass_context
def analytics_js(context):
    hide: bool = settings.DEBUG
    if request := context.get('request'):
        hide |= getattr(request, 'preview', False)
    if not hide:
        return mark_safe(
            '<script defer src="https://stats.neonjungle.com.au/analytics.js"></script>')
    return ''


def _gen_sources(image, sizes: List[Tuple[int, str]],
                 aspect_ratio: float) -> Union[SafeText, None]:
    def html_attrs():
        for pixel_width, media_attr in sizes:
            yield (
                media_attr,
                image.get_rendition(
                    f'fill-{pixel_width}x{int(aspect_ratio * float(pixel_width))}').url,
                image.get_rendition(
                    f'fill-{pixel_width * 2}x{int(aspect_ratio * float(pixel_width)) * 2}').url,
            )
    return format_html_join(
        '\n',
        '<source media="{}" srcset="{}, {} 2x">',
        html_attrs()
    )


def _size_refactor(size_tuple: Tuple[int, str], factor: float) -> Tuple[int, str]:
    return (int(size_tuple[0] * factor), size_tuple[1])


def aspect_picture_mobile(image, dimensions: Tuple[int, int]) -> SafeText:
    # height / width
    aspect_ratio = dimensions[1] / dimensions[0]
    # Calculate the percentage the image takes up of the 'default width'
    width_factor = dimensions[0] / 375
    sizes = [
        (375, '(max-width: 375px)'),
        (767, '(min-width: 376px) and (max-width: 767px)'),
    ]
    sizes = [_size_refactor(s, width_factor) for s in sizes]
    return _gen_sources(image, sizes, aspect_ratio) or SafeText('')


def aspect_picture_desktop(image, dimensions: Tuple[int, int]) -> SafeText:
    # height / width
    aspect_ratio = dimensions[1] / dimensions[0]
    # Calculate the percentage the image takes up of the 'default width'
    width_factor = dimensions[0] / 1920
    sizes = [
        (1023, '(min-width: 768px) and (max-width: 1023px)'),
        (1279, '(min-width: 1024px) and (max-width: 1279px)'),
        (1439, '(min-width: 1280px) and (max-width: 1439px)'),
        (1920, '(min-width: 1440px)'),
    ]
    sizes = [_size_refactor(s, width_factor) for s in sizes]
    return _gen_sources(image, sizes, aspect_ratio) or SafeText('')


def aspect_picture(image, desktop_dimensions: Tuple[int, int],
                   mobile_dimensions: Tuple[int, int], html_class: str = '') -> SafeText:
    if not image:
        return SafeText('')

    sources_markup = aspect_picture_mobile(image, mobile_dimensions) + \
        aspect_picture_desktop(image, desktop_dimensions)

    default_image = image.get_rendition(f'fill-{desktop_dimensions[0]}x{desktop_dimensions[1]}')

    if html_class:
        html_class = f' class="{html_class}"'
    return format_html("""
        <picture{2}>
            {0}
            {1}
        </picture>
    """, sources_markup, default_image.img_tag(), mark_safe(html_class))


class Extension(jinja2.ext.Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update({
            'breadcrumbs': breadcrumbs,
            'site_root': site_root,
            'static': staticfiles_storage.url,
            'include_static': include_static,
            'render_bundle': render_bundle,
            'url': url,
            'svg': svg_inline,
            'model_classname': model_classname,
            'messages': messages,
            'DEBUG': settings.DEBUG,
            'qs': qs,
            'pic_src': source_tag,
            'render_honeypot_field': render_honeypot_field,
            'analytics_js': analytics_js,
            'aspect_picture': aspect_picture,
        })

        self.environment.filters.update({
            'model_classname': model_classname,
            'add_form_class': add_form_class,
            'add_form_attributes': add_form_attributes,
            'debug_variable': debug_variable,
            'br': linebreaksbr,
            'p': linebreaks_filter,
            'json': json_dumps,
            'tel': tel,
            'time_format': time,
            'date_format': date
        })
