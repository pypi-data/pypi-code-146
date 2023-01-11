import logging
from django.db import models
from django.conf import settings
from urllib.parse import quote
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from functools import partial
from django.core.exceptions import ImproperlyConfigured

try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

from embedly import Embedly
from csembedlyparser.utils.datetime_utils import get_datetime_now_utc
from csembedlyparser.utils.chars import check_uppercase, get_longest_string

import re

EMBEDLY_KEY = getattr(settings, 'CSEMBEDLYPARSER_EMBEDLY_KEY', None)
OEMBED_SIZES = getattr(settings,
                       'CSEMBEDLYPARSER_OEMBED_SIZES',
                       (('big', (420, 420)),
                        )
                       )

EXPIRATION = getattr(settings, 'CSEMBEDLYPARSER_EXPIRATION', 3600 * 24 * 365 * 10)
STOPWORDS_IMAGES = getattr(settings, 'CSEMBEDLYPARSER_STOPWORDS_IMAGES', ('banner', 'ad', 'promo', 'promos', 'logo', 'icono', 'publi', 'ads', 'banners', 'iconos', 'logos', 'berriafb', 'default',))
TITLE_CLEANER = getattr(settings, 'CSEMBEDLYPARSER_TITLE_CLEANER', (r'\\', '-', '_', r'\|', '~', '/','::', ':', '<', '>','/','~'))

CTE_MIN_WIDTH_OR_HEIGHT = 200
CTE_MIN_WIDTH_OR_HEIGHT_2 = 100


def is_photo_clean(photo_url, photo_width, photo_height):
    if not photo_url:
        return False
    if photo_width < CTE_MIN_WIDTH_OR_HEIGHT and photo_height < CTE_MIN_WIDTH_OR_HEIGHT:
        return False

    if photo_width < CTE_MIN_WIDTH_OR_HEIGHT_2 or photo_height < CTE_MIN_WIDTH_OR_HEIGHT_2:
        return False

    words = re.split('[^a-zA-Z0-9]+', photo_url.lower())
    fids = set(words)
    inter = fids.intersection(STOPWORDS_IMAGES)
    if len(inter):
        return False
    return True


def get_embedly_client():
    if not EMBEDLY_KEY:
        raise ImproperlyConfigured('Embedly key needed')
    client = Embedly(key=EMBEDLY_KEY)
    return client


def get_or_create_embedlyparsed(url):
    embedly = EmbedlyParsed.objects.filter(original_url=url)
    if embedly.exists():
        return (embedly[0], False)
    else:
        obj = EmbedlyParsed(original_url=url)
        obj.save()
        obj.parse()
        return (obj, True)


class EmbedlyParsed(models.Model):
    original_url = models.CharField(max_length=255)
    domain = models.CharField(max_length=100, null=True, blank=True)

    parsed = models.BooleanField(default=False, db_index=True)
    parsed_datetime = models.DateTimeField(null=True, blank=True)

    favicon = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

    type = models.CharField(max_length=25, null=True, blank=True)
    version = models.CharField(max_length=25, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    title_original = models.CharField(max_length=255, null=True, blank=True)
    #ALTER TABLE `csembedlyparser_embedlyparsed` ADD `title_original` VARCHAR( 255 ) NULL AFTER `title`
    description = models.TextField(null=True, blank=True)
    author_name = models.CharField(max_length=255, null=True, blank=True)
    author_url = models.CharField(max_length=255, null=True, blank=True)
    provider_name = models.CharField(max_length=255, null=True, blank=True)
    provider_url = models.CharField(max_length=255, null=True, blank=True)
    cache_age = models.PositiveIntegerField(null=True, blank=True)
    thumbnail_url = models.CharField(max_length=255, null=True, blank=True)
    #photo = models.ForeignKey(Photo, null=True, blank=True, related_name='embedly_photo')
    photo_url = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u'Embedly: %s' % self.original_url

    def __init__(self, *args, **kwargs):
        super(EmbedlyParsed, self).__init__(*args, **kwargs)
        self.add_accessor_methods()

    def clean_title(self):
        """ """
        splitter = re.compile(r'|'.join(r'\s' + word + r'\s' for word in TITLE_CLEANER))
        if check_uppercase(self.title_original):
            self.title_original = self.title_original.lower().capitalize()
        if check_uppercase(self.description):
            self.description = self.description.lower().capitalize()
        if not self.title_original:
            self.title = self.title_original
            return None
        this_title_splitted = splitter.split(self.title_original)

        if len(this_title_splitted) == 1:
            self.title = self.title_original
            return None
        #has any preview url for this domain?
        if EmbedlyParsed.objects.filter(domain=self.domain, pk__lt=self.pk, title_original__isnull=False).count():
            p_ep = EmbedlyParsed.objects.filter(domain=self.domain, pk__lt=self.pk, title_original__isnull=False).order_by('-pk')[0]
            p_ep_title_splitted = splitter.split(p_ep.title_original)
            diference = set(this_title_splitted).difference(p_ep_title_splitted)
            if len(diference) >= 1:
                self.title = get_longest_string(diference)
                return None
        #use the longest split
        self.title = get_longest_string(this_title_splitted)
        return None
        """
        import re
        >>> re.compile('\||-')
        <_sre.SRE_Pattern object at 0xa96aea8>
        >>> splitter = re.compile('\||-')
        >>> splitter.split('Kaixo | Agur')
        ['Kaixo ', ' Agur']
        >>> splitter.split('Kaixo - Agur')
        ['Kaixo ', ' Agur']
        """

    def get_original_url_toparse(self):
        """ """
        url = self.original_url
        return url
        p_http = '%s://' % urlparse(url).scheme
        return '%s%s' % (p_http, quote(url[len(p_http):]))

    """
    def has_parser_title(self):
        if not(self.title):
            return False
        t = self.title.strip()
        return len(t) > 3
    """

    def has_parser_description(self):
        d = self.parser_description.strip()
        return len(d) > 10

    def has_been_parsed(self):
        """ """
        return self.parsed

    def set_extract_data(self, obj):
        """ """
        self.favicon = obj.get('favicon_url')
        self.domain = obj.get('provider_url')
        self.title = obj.get('title')
        self.title_original = self.title
        self.description = obj.get('description')
        self.url = obj.get('url')
        self.author_name = obj.get('author_name')
        self.author_url = obj.get('author_url')
        self.provider_name = obj.get('provider_name')
        self.cache_age = obj.get('cache_age')
        self.type = obj.get('media') and obj.get('media').get('type') or obj.get('type') or ''

        if obj.get('media') and obj.get('media').get('type') == 'photo':
            self.photo_url = obj.get('media').get('url')
            if self.domain in (u'http://twitter.com',u'http://twitter.yfrog.com'):
                #find urls
                r = re.compile(r"(http://[^ ]+)")
                title = ' '.join([k for k in r.split(self.description) if len(k) > 0 and not(k.startswith('http'))])
                self.title_original = title
                self.title = title
        elif obj.get('images'):
            #news
            photo_url = obj.get('images')[0].get('url','')
            photo_width = obj.get('images')[0].get('width')
            photo_height = obj.get('images')[0].get('height')
            if not is_photo_clean(photo_url, photo_width, photo_height):
                photo_url = u''
            self.photo_url = photo_url
        else:
            self.photo_url = ''
        self.parsed = True
        self.parsed_datetime = get_datetime_now_utc()
        #Clearn our title from title_original
        self.clean_title()

        self.save()
        return True

    def _parse_oembed(self):
        """ """
        log = logging.getLogger('django')
        client = get_embedly_client()
        for size in OEMBED_SIZES:
            try:
                obj = client.extract(self.original_url, maxwidth=size[1][0], maxheight=size[1][1])
            except Exception:
                log.info('csembedly: Exception: %s' % Exception)
                return False
            if not getattr(obj, 'error', False):
                if not self.title_original or not self.parsed:
                    self.set_extract_data(obj)
                if not OembedSized.objects.filter(url=self, width=size[1][0], height=size[1][1]).exists():

                    size_things = OembedSized(url=self,
                                          width=size[1][0],
                                          height=size[1][1],
                                          thumbnail_width= obj.get('images') and obj.get('images')[0].get('width') or 0,
                                          thumbnail_height= obj.get('images') and obj.get('images')[0].get('height') or 0,
                                          width_returned= obj.get('media') and obj.get('media').get('width') or 0,
                                          height_returned= obj.get('media') and obj.get('media').get('width') or 0,
                                          html=obj.get('media').get('html') or '',
                                          data=obj.data)

                    size_things.save()
            else:
                log.info(obj.error)
        return True

    def parse(self):
        """ """
        return self._parse_oembed()

    def _get_oembed_html_SIZE(self, size):
        obj = OembedSized.objects.get(url=self, width=size[0], height=size[1])
        return obj.html

    def _get_oembed_thumbnail_width_SIZE(self, size):
        obj = OembedSized.objects.get(url=self, width=size[0], height=size[1])
        return obj.thumbnail_width

    def _get_oembed_thumbnail_height_SIZE(self, size):
        obj = OembedSized.objects.get(url=self, width=size[0], height=size[1])
        return obj.thumbnail_height

    def _get_oembed_width_SIZE(self, size):
        obj = OembedSized.objects.get(url=self, width=size[0], height=size[1])
        return obj.width

    def _get_oembed_height_SIZE(self, size):
        obj = OembedSized.objects.get(url=self, width=size[0], height=size[1])
        return obj.height

    def _get_oembed_data_SIZE(self, size):
        obj = OembedSized.objects.get(url=self, width=size[0], height=size[1])
        return obj.data

    def _html_SIZE(self, size):
        """ """
        h = {}
        h['obj'] = self
        try:
            if self.type == u'photo':
                return render_to_string("csembedlyparser/%s_oembed_photo.html" % size, h)
            elif self.type == u'video':
                return render_to_string("csembedlyparser/%s_oembed_video.html" % size, h)
            elif self.type == u'rich':
                return render_to_string("csembedlyparser/%s_oembed_rich.html" % size, h)
            elif self.type == u'link':
                return render_to_string("csembedlyparser/%s_oembed_link.html" % size, h)
        except TemplateDoesNotExist:
            return render_to_string("csembedlyparser/default.html", h)

    def add_accessor_methods(self, *args, **kwargs):
        for size in OEMBED_SIZES:
            size_name = size[0]
            size = size[1]
            setattr(self, 'get_oembed_html_%s' % size_name,
                    partial(self._get_oembed_html_SIZE, size=size))
            setattr(self, 'get_oembed_thumbnail_width_%s' % size_name,
                    partial(self._get_oembed_thumbnail_width_SIZE, size=size))
            setattr(self, 'get_oembed_thumbnail_height_%s' % size_name,
                    partial(self._get_oembed_thumbnail_height_SIZE, size=size))
            setattr(self, 'get_oembed_width_%s' % size_name,
                    partial(self._get_oembed_width_SIZE, size=size))
            setattr(self, 'get_oembed_height_%s' % size_name,
                    partial(self._get_oembed_height_SIZE, size=size))
            setattr(self, 'get_oembed_data_%s' % size_name,
                    partial(self._get_oembed_data_SIZE, size=size))
            setattr(self, 'html_%s' % size_name,
                    partial(self._html_SIZE, size=size_name))


class OembedSized(models.Model):
    url = models.ForeignKey(EmbedlyParsed, on_delete=models.PROTECT)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    thumbnail_width = models.PositiveIntegerField(null=True, blank=True)
    thumbnail_height = models.PositiveIntegerField(null=True, blank=True)
    html = models.TextField(null=True, blank=True)
    width_returned = models.PositiveIntegerField(null=True, blank=True)
    height_returned = models.PositiveIntegerField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('url', 'width', 'height')
