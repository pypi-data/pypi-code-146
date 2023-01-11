import subprocess
import time
from typing import Optional

from requests import Session

from .exceptions import AttemptsExceededError
from .ffmpeg import _make_ffmpeg_args
from .streamlink import _get_parser, _get_ts_url, get_m3u8, get_stream_url


def get_ts_url(
    stream: str, wait_seconds: Optional[int] = 3, max_try: Optional[int] = 10
) -> str:
    session = Session()
    parser = _get_parser(stream)

    count = max_try

    while True if count is None else count:
        data = session.get(stream)
        text = data.text

        m3u8 = get_m3u8(text, parser=parser)
        ts_url = _get_ts_url(m3u8)

        if ts_url:
            session.close()

            return ts_url

        count -= 1

        time.sleep(m3u8.target_duration if wait_seconds is None else wait_seconds)

    session.close()
    raise AttemptsExceededError(max_try)


def download_thumbnail(
    channel: str,
    path: str,
    stream: Optional[str] = None,
    twitch_oauth: Optional[str] = None,
) -> str:
    if stream is None:
        stream = get_stream_url(channel, twitch_oauth)
    ts_url = get_ts_url(stream)

    subprocess.run(
        _make_ffmpeg_args(ts_url, path),
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )

    return stream
