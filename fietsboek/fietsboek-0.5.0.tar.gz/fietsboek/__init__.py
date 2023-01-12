"""Fietsboek is a web application to track and share GPX tours.

This is the documentation for the Python package, useful for developers that
wish to work on fietsboek.

For more information, you can check out the following resources:

* The `Fietsboek repository`_.
* The documentation index: :doc:`../../../index`

.. _Fietsboek repository: https://gitlab.com/dunj3/fietsboek

Content
-------
"""
from pathlib import Path

import importlib_metadata
import redis
from pyramid.config import Configurator
from pyramid.csrf import CookieCSRFStoragePolicy
from pyramid.i18n import default_locale_negotiator
from pyramid.session import SignedCookieSessionFactory

from . import config as mod_config
from . import jinja2 as mod_jinja2
from .data import DataManager
from .pages import Pages
from .security import SecurityPolicy

__VERSION__ = importlib_metadata.version("fietsboek")


def locale_negotiator(request):
    """Negotiates the right locale to use.

    This tries the following:

    1. It runs the default negotiator. This allows the locale to be overriden
       by using the ``_LOCALE_`` query parameter.
    2. It uses the `Accept-Language`_ header.

    .. _Accept-Language: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language

    :param request: The request for which to get the language.
    :type request: pyramid.request.Request
    :return: The determined locale, or ``None`` if the default should be used.
    :rtype: str
    """
    locale = default_locale_negotiator(request)
    if locale:
        return locale

    installed_locales = request.config.available_locales
    sentinel = object()
    negotiated = request.accept_language.lookup(installed_locales, default=sentinel)
    if negotiated is sentinel:
        return None
    return negotiated


def main(_global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    parsed_config = mod_config.parse(settings)

    def data_manager(request):
        return DataManager(Path(request.config.data_dir))

    def redis_(request):
        return redis.from_url(request.config.redis_url)

    def config_(_request):
        return parsed_config

    # Load the pages
    page_manager = Pages()
    for path in parsed_config.pages:
        path = Path(path)
        if path.is_dir():
            page_manager.load_directory(path)
        elif path.is_file():
            page_manager.load_file(path)

    def pages(_request):
        return page_manager

    my_session_factory = SignedCookieSessionFactory(parsed_config.derive_secret("sessions"))
    cookie_secret = parsed_config.derive_secret("auth-cookie")
    with Configurator(settings=settings) as config:
        config.include("pyramid_jinja2")
        config.include(".routes")
        config.include(".models")
        config.scan()
        config.add_translation_dirs("fietsboek:locale/")
        for pack in parsed_config.language_packs:
            config.add_translation_dirs(f"{pack}:locale/")
        config.set_session_factory(my_session_factory)
        config.set_security_policy(SecurityPolicy(cookie_secret))
        config.set_csrf_storage_policy(CookieCSRFStoragePolicy())
        config.set_default_csrf_options(require_csrf=True)
        config.set_locale_negotiator(locale_negotiator)
        config.add_request_method(data_manager, reify=True)
        config.add_request_method(pages, reify=True)
        config.add_request_method(redis_, name="redis", reify=True)
        config.add_request_method(config_, name="config", reify=True)

    jinja2_env = config.get_jinja2_environment()
    jinja2_env.filters["format_decimal"] = mod_jinja2.filter_format_decimal
    jinja2_env.filters["format_datetime"] = mod_jinja2.filter_format_datetime
    jinja2_env.filters["local_datetime"] = mod_jinja2.filter_local_datetime
    jinja2_env.globals["embed_tile_layers"] = mod_jinja2.global_embed_tile_layers

    return config.make_wsgi_app()
