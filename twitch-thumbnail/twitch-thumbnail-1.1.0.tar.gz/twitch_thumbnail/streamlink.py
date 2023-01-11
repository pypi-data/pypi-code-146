from typing import Optional

from streamlink.exceptions import PluginError
from streamlink.plugins.twitch import (
    Twitch,
    TwitchAPI,
    TwitchHLSStream,
    TwitchM3U8,
    TwitchM3U8Parser,
    UsherService,
)
from streamlink.session import Streamlink

from .exceptions import AuthError, NoStreamError


def get_stream_url(channel: str, twitch_oauth: Optional[str] = None) -> str:
    session = Streamlink()
    api = TwitchAPI(session)
    usher = UsherService(session)

    session.http.headers.update(
        {
            "referer": "https://player.twitch.tv",
            "origin": "https://player.twitch.tv",
        }
    )

    if twitch_oauth:
        session.http.headers.update({"Authorization": f"OAuth {twitch_oauth}"})

    try:
        sig, token = api.access_token(True, channel)
    except PluginError:
        raise AuthError

    url = usher.channel(channel, sig=sig, token=token, fast_bread=True)

    try:
        streams = TwitchHLSStream.parse_variant_playlist(session, url)
    except OSError:
        raise NoStreamError(channel)

    sorted_streams = sorted(
        streams, key=lambda k: Twitch.stream_weight(k)[0], reverse=True
    )

    best_stream = streams[sorted_streams[0]]

    return best_stream.url


def get_m3u8(
    data: str, parser: Optional[TwitchM3U8Parser] = None, url: Optional[str] = None
) -> TwitchM3U8:
    if isinstance(parser, TwitchM3U8Parser):
        return parser.parse(data)

    if not url:
        raise TypeError("url is required")

    parser = _get_parser(url)
    m3u8: TwitchM3U8 = parser.parse(data)

    return m3u8


def _get_parser(base_uri: str) -> TwitchM3U8Parser:
    return TwitchM3U8Parser(base_uri, m3u8=TwitchM3U8)


def _get_ts_url(m3u8: TwitchM3U8) -> Optional[str]:
    for seg in m3u8.segments:
        # "Amazon" in title
        if not seg.ad:
            return seg.uri
