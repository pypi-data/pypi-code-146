import asyncio
from typing import Optional

from aiohttp import ClientSession

from .exceptions import AttemptsExceededError
from .ffmpeg import _make_ffmpeg_args
from .streamlink import _get_parser, _get_ts_url, get_m3u8, get_stream_url


async def get_ts_url(
    stream: str, wait_seconds: Optional[int] = 3, max_try: Optional[int] = 10
) -> str:
    session = ClientSession()
    parser = _get_parser(stream)

    count = max_try

    while True if count is None else count:
        data = await session.get(stream)
        text = await data.text()

        m3u8 = get_m3u8(text, parser=parser)
        ts_url = _get_ts_url(m3u8)

        if ts_url:
            await session.close()

            return ts_url

        count -= 1

        await asyncio.sleep(
            m3u8.target_duration if wait_seconds is None else wait_seconds
        )

    await session.close()
    raise AttemptsExceededError(max_try)


async def download_thumbnail(
    channel: str,
    path: str,
    stream: Optional[str] = None,
    twitch_oauth: Optional[str] = None,
) -> str:
    if stream is None:
        stream = await asyncio.to_thread(get_stream_url, channel, twitch_oauth)

    ts_url = await get_ts_url(stream)

    proc = await asyncio.create_subprocess_shell(
        _make_ffmpeg_args(ts_url, path, join=True),
        stderr=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.DEVNULL,
    )

    await proc.communicate()

    return stream
