from urllib.parse import urlparse

from django.http import HttpRequest
from django.conf import settings

from .menu import get_menu_items

def backoffice(request: HttpRequest) -> dict:
    """The backoffice context processor. This variables will be available in all templates.

    :param request: The request object.
    :return: The context variables.
    :rtype: dict
    """
    base_url = getattr(settings, "BASE_URL", "https://www.dnoticias.pt")
    site_domain = urlparse(base_url).netloc

    return {
        "BASE_URL": base_url,
        "SITE_DOMAIN": site_domain,
        "SITE_NAME": getattr(settings, "SITE_NAME", "Backoffice"),
        "MENU_ITEMS": get_menu_items(request),
    }
