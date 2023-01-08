# -*- coding: utf-8 -*-
# :Project:   SoL -- i18n utilities
# :Created:   mer 10 apr 2013 09:24:33 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2013, 2014, 2018, 2020 Lele Gaifax
#

from pyramid.i18n import TranslationStringFactory


DOMAIN = 'sol-server'
"The translation domain of the server side"

translatable_string = TranslationStringFactory(DOMAIN)
"A function to make a translatable string."


available_languages = []


def locale_negotiator(request, _available_languages=available_languages):
    """Recognize the user preferred language.

    :param request: the Pyramid request
    :param _available_languages: the list of available languages (this is used
                                 as a cache, computed at the first call to this
                                 function)

    Honor the user preferred language, stored in the ``ui_language`` slot of the request's
    ``session`` at login time by :func:`sol.views.auth.auth_user`, falling back to the
    language accepted by the user's browser.
    """

    if not _available_languages:
        from pyramid.threadlocal import get_current_registry
        settings = get_current_registry().settings
        codes = settings.get('available_languages', 'en-GB')
        _available_languages.extend((c.replace('_', '-') for c in codes.split()))

    ui_language = request.session.get('ui_language')
    if ui_language and ui_language.replace('_', '-') in _available_languages:
        return ui_language

    accepted = request.accept_language
    if not accepted:
        return

    return accepted.lookup(_available_languages, default='en-GB').replace('-', '_')


def translator(request):
    """Return a function that translates a given string in the specified request

    :param request: either None or a Pyramid request instance

    This is an helper function that handle the case when the request
    does not exist, for example while testing::

      >>> t = translator(None)
      >>> t('$first $last', mapping=dict(first='Foo', last='Bar'))
      'Foo Bar'
    """

    if request is not None:
        def wrapper(*args, **kw):
            if 'domain' not in kw:
                kw['domain'] = DOMAIN
            return request.localizer.translate(*args, **kw)
        return wrapper
    else:
        from string import Template
        return lambda s, **kw: Template(s).substitute(**kw.get('mapping', {}))


def gettext(s, **kw):
    """Immediately translate the given string with current request locale

    :param s: either a string or a TranslationString instance
    :keyword just_subst: by default False, True to disable the actual translation
                         and perform only mapping substitution
    """

    from string import Template
    from pyramid.threadlocal import get_current_request

    if 'domain' not in kw:
        kw['domain'] = DOMAIN

    text = None
    if not kw.pop('just_subst', False):
        request = get_current_request()
        if request is not None:
            text = request.localizer.translate(s, **kw)

    return text or Template(s).substitute(**kw.get('mapping', {}))


def ngettext(s, p, n, **kw):
    """Immediately translate the singular or plural form with current request locale

    :param s: either a string or a TranslationString instance with the
              singular form
    :param p: either a string or a TranslationString instance with the
              plural form
    :param n: an integer
    """

    from string import Template
    from pyramid.threadlocal import get_current_request

    if 'domain' not in kw:
        kw['domain'] = DOMAIN

    request = get_current_request()
    if request is not None:
        return request.localizer.pluralize(s, p, n, **kw)
    else:
        return Template(s if n == 1 else p).substitute(**kw.get('mapping', {}))


def _country_name(gettext, hastext, country):
    # Some countries, CZE for example, have no translation for their name,
    # so take the official_name translation, if present
    name = gettext(country.name)
    if ((hasattr(country, 'official_name')
         and not hastext(country.name)
         and hastext(country.official_name))):
        name = gettext(country.official_name)
    return name


def country_name(code, request=None):
    "Translate the given ISO 3166 country `code` name."

    from gettext import translation
    from pycountry import LOCALES_DIR, countries
    from pyramid.threadlocal import get_current_request

    if request is None:
        request = get_current_request()

    lname = getattr(request, 'locale_name', 'en')
    try:
        t = translation('iso3166', LOCALES_DIR, languages=[lname])
        gettext = t.gettext
        hastext = t._catalog.__contains__
    except IOError:
        gettext = lambda x: x        # noqa
        hastext = lambda x: True     # noqa

    _ = translatable_string

    if code:
        if code == 'eur':
            result = translator(request)(_('Europe'))
        elif code == 'wrl':
            result = translator(request)(_('World'))
        else:
            result = _country_name(gettext, hastext, countries.get(alpha_3=code))
    else:
        result = translator(request)(_('Unspecified country'))

    return result


def countries_names(request=None):
    "Build a list of dictionaries ``(code, translated-name)`` of all known countries."

    from gettext import translation
    from pycountry import LOCALES_DIR, countries
    from pyramid.threadlocal import get_current_request

    if request is None:  # pragma: nocover
        request = get_current_request()

    lname = getattr(request, 'locale_name', 'en')
    try:
        t = translation('iso3166', LOCALES_DIR, languages=[lname])
        gettext = t.gettext
        hastext = t._catalog.__contains__
    except IOError:
        gettext = lambda x: x        # noqa
        hastext = lambda x: True     # noqa

    result = [dict(code=c.alpha_3, name=_country_name(gettext, hastext, c)) for c in countries]

    # Add "eur" for Europe and "wrl" for World, lowercase code to avoid future conflict with
    # official ISO code...
    t = translator(request)
    _ = translatable_string
    result.append(dict(code="eur", name=t(_('Europe'))))
    result.append(dict(code="wrl", name=t(_('World'))))
    return result


def language_name(code, request=None):
    "Translate the given ISO 639-3 language `code`."

    if code:
        from gettext import translation
        from pycountry import LOCALES_DIR, countries, languages
        from pyramid.threadlocal import get_current_request

        if request is None:
            request = get_current_request()

        lname = getattr(request, 'locale_name', 'en')
        try:
            lt = translation('iso639-3', LOCALES_DIR, languages=[lname]).gettext
        except IOError:
            lt = lambda x: x  # noqa

        if '_' in code:
            lcode, ccode = code.split('_')
            try:
                ct = translation('iso3166', LOCALES_DIR, languages=[lname]).gettext
            except IOError:
                ct = lambda x: x  # noqa
            return '%s (%s)' % (lt(languages.get(alpha_2=lcode).name),
                                ct(countries.get(alpha_2=ccode).name))
        else:
            return lt(languages.get(alpha_2=code).name)


def languages_names(request=None):
    "Build a list of dictionaries ``(code, translated-name)`` of all available languages."

    from gettext import translation
    from pycountry import LOCALES_DIR, countries, languages
    from pyramid.threadlocal import get_current_request

    if request is None:  # pragma: nocover
        request = get_current_request()

    lname = getattr(request, 'locale_name', 'en')
    available_languages = request.registry.settings.get('available_languages', 'en')
    try:
        lt = translation('iso639-3', LOCALES_DIR, languages=[lname]).gettext
    except IOError:
        lt = lambda x: x  # noqa
    try:
        ct = translation('iso3166', LOCALES_DIR, languages=[lname]).gettext
    except IOError:
        ct = lambda x: x  # noqa

    result = []
    for code in available_languages.split():
        if len(code) == 2:
            result.append(dict(code=code, name=lt(languages.get(alpha_2=code).name)))
        else:
            lcode, ccode = code.split('_')
            result.append(dict(code=code,
                               name='%s (%s)' % (lt(languages.get(alpha_2=lcode).name),
                                                 ct(countries.get(alpha_2=ccode).name))))
    return result
