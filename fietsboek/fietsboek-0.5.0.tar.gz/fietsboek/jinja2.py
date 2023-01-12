"""Custom filters for Jinja2."""
import datetime
import json

import jinja2
from babel.dates import format_datetime
from babel.numbers import format_decimal
from markupsafe import Markup


@jinja2.pass_context
def filter_format_decimal(ctx, value):
    """Format a decimal number according to the locale.

    This uses the right thousands grouping and the right decimal separator.

    :param ctx: The jinja context, passed automatically.
    :type ctx: jinja2.runtime.Context
    :param value: The value to format.
    :type value: float
    :return: The formatted decimal.
    :rtype: str
    """
    request = ctx.get("request")
    locale = request.localizer.locale_name
    return format_decimal(value, locale=locale)


@jinja2.pass_context
def filter_format_datetime(ctx, value):
    """Format a datetime according to the locale.

    :param ctx: The jinja context, passed automatically.
    :type ctx: jinja2.runtime.Context
    :param value: The value to format.
    :type value: datetime.datetime
    :return: The formatted date.
    :rtype: str
    """
    request = ctx.get("request")
    locale = request.localizer.locale_name
    return format_datetime(value, locale=locale)


@jinja2.pass_context
def filter_local_datetime(ctx, value):
    """Format a UTC datetime to show in the user's local timezone.

    This is done by embedding the UTC timestamp in the page, such that we can
    do some client-side magic and replace it with the time in the user's local
    timezone. As a fallback value, we do apply the locale's standard
    formatting, in case JavaScript is disabled - however, that will not
    represent the time in the user's timezone, but in UTC.

    :param ctx: The jinja context, passed automatically.
    :type ctx: jinja2.runtime.Context
    :param value: The value to format.
    :type value: datetime.datetime
    :return: The formatted date.
    :rtype: Markup
    """
    # If we get a naive object in, we assume that we got it from the database
    # and we have to treat it like a UTC-aware object. This happens when we
    # access object's DateTime columns directly, as SQLAlchemy only returns
    # naive datetimes.
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.timezone.utc)
    else:
        value = value.astimezone(datetime.timezone.utc)

    request = ctx.get("request")
    locale = request.localizer.locale_name
    fallback = Markup.escape(format_datetime(value, locale=locale))

    # Forget about the fractional seconds
    timestamp = int(value.timestamp())
    return Markup(
        f'<span class="fietsboek-local-datetime" data-utc-timestamp="{timestamp}">{fallback}</span>'
    )


def global_embed_tile_layers(request):
    """Renders the available tile servers for the current user, as a JSON object.

    The returned value is wrapped as a :class:`~markupsafe.Markup` so that it
    won't get escaped by jinja.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The available tile servers.
    :rtype: markupsafe.Markup
    """
    # pylint: disable=import-outside-toplevel,cyclic-import
    from .views import tileproxy

    tile_sources = tileproxy.sources_for(request)

    if request.config.disable_tile_proxy:

        def _url(source):
            return source.url

    else:

        def _url(source):
            return (
                request.route_url("tile-proxy", provider=source.layer_id, x="{x}", y="{y}", z="{z}")
                .replace("%7Bx%7D", "{x}")
                .replace("%7By%7D", "{y}")
                .replace("%7Bz%7D", "{z}")
            )

    return Markup(
        json.dumps(
            [
                {
                    "name": source.name,
                    "url": _url(source),
                    "attribution": source.attribution,
                    "type": source.layer_type.value,
                    "zoom": source.zoom,
                }
                for source in tile_sources
            ]
        )
    )
