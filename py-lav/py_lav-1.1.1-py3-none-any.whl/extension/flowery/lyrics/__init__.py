from __future__ import annotations

from typing import TYPE_CHECKING

from dacite import from_dict

from pylav.extension.flowery.lyrics.responses import Error, Lyrics, TrackList

if TYPE_CHECKING:
    from pylav.core.client import Client
    from pylav.extension.flowery.base import FloweryAPI


class LyricsAPI:
    def __init__(self, client: Client, wrapper: FloweryAPI) -> None:
        self._wrapper = wrapper
        self._base_url = "https://api.flowery.pw/v1/lyrics"
        self._session = wrapper._cached_session
        self.client = client

    async def get_lyrics(self, query: str = None, isrc: str = None, spotify_id: str = None) -> Lyrics | Error:
        params = {}
        if query:
            params["query"] = query
        if isrc:
            params["isrc"] = isrc
        if spotify_id:
            params["spotify_id"] = spotify_id
        if not params:
            raise ValueError("You must provide either a query, isrc or spotify_id")

        async with self._session.get(
            self._base_url,
            params=params,
        ) as response:
            match response.status:
                case 200 | 202:
                    return from_dict(data_class=Lyrics, data=await response.json())
                case 404 | 422 | 500:
                    return from_dict(data_class=Error, data=await response.json())
                case __:
                    raise ValueError(f"Unexpected status code: {response.status}")

    async def search_lyrics(self, query: str) -> TrackList | Error:
        async with self._session.get(
            f"{self._base_url}/search",
            params={"query": query},
        ) as response:
            match response.status:
                case 200:
                    return from_dict(data_class=TrackList, data=await response.json())
                case 404 | 422 | 500:
                    return from_dict(data_class=Error, data=await response.json())
                case __:
                    raise ValueError(f"Unexpected status code: {response.status}")
