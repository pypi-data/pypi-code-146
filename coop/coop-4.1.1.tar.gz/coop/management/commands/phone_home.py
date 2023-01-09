import json

import requests
from django import __version__ as django_version
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.text import slugify
from django.utils.timezone import now
from wagtail import __version__ as wt_version
from wagtail.models import Page, Site

from coop.models import AnalyticsSettings


class Command(BaseCommand):
    help = "Sends a JSON payload to the given url"

    def add_arguments(self, parser):
        parser.add_argument(
            "url",
            type=str,
            nargs="?",
            help="url to send the payload to",)

    def handle(self, *args, **options) -> None:
        url = options['url']

        def get_site_info(site):
            info = dict()
            analytics = AnalyticsSettings.for_site(site)

            if analytics:
                info['google_analytics'] = analytics.google_analytics
                info['google_tag_manager'] = analytics.google_tag_manager
            else:
                info['google_analytics'] = False
                info['google_tag_manager'] = False

            info['url'] = site.root_url
            info['name'] = site.site_name

            info['page_count'] = Page.objects.live().count() - 1  # Don't count the root page
            info['update_time'] = now().timestamp()
            info['wt_version'] = wt_version
            info['django_version'] = django_version

            return info

        payload = dict()
        for site in Site.objects.all():
            site_info = get_site_info(site)
            key = slugify(site.site_name)
            payload.update({key: site_info})

        requests.post(url, data=json.dumps(payload, cls=DjangoJSONEncoder))
