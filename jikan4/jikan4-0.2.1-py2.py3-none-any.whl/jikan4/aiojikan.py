from __future__ import annotations

import aiohttp

from .models import (
    Anime,
    AnimeSearch,
    AnimeCharacters,
    AnimeStaff,
    AnimeEpisodes,
    Episode,
    AnimeNews,
)
from .utils.async_limiter import AsyncLimiter


class AioJikan:
    """Async Jikan API Wrapper"""

    def __init__(
        self, base_url: str = "https://api.jikan.moe/v4", rate_limit: int = 60
    ) -> None:
        """Construct a AioJikan object

        Args:
            base_url (str, optional): Base URL for Jikan API. Defaults to "https://api.jikan.moe/v4".
            rate_limit (int, optional): Rate limit in requests per minute. Defaults to 60.

        Returns:
            AioJikan: AioJikan object

        Examples:
            >>> aiojikan = AioJikan()
            >>> aiojikan = AioJikan("https://api.jikan.moe/v4")
        """

        base_url = base_url.rstrip("/")
        self.base_url = base_url

        if rate_limit:
            self.rate_limiter = AsyncLimiter(calls_limit=rate_limit / 60, period=1)
            self._get = self.rate_limiter.__call__(self._get)

    async def close(self) -> None:
        """Close the aiohttp session"""

        await self.session.close()

    async def __aenter__(self) -> AioJikan:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request to the Jikan API

        Args:
            endpoint (str): Endpoint to request
            params (dict, optional): Parameters to send with request. Defaults to None.

        Returns:
            dict: JSON response from Jikan API
        """

        url = f"{self.base_url}/{endpoint}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def get_anime(self, anime_id: int) -> Anime:
        """Get anime information

        Args:
            anime_id (int): Anime ID

        Returns:
            Anime: Anime object

        Examples:
            >>> aiojikan = AioJikan()
            >>> anime = await aiojikan.get_anime(1)
        """

        endpoint = f"anime/{anime_id}"
        response = await self._get(endpoint)

        return Anime(**response["data"])

    async def get_anime_full(self, anime_id: int) -> Anime:
        """Get anime information with full details

        Args:
            anime_id (int): Anime ID

        Returns:
            Anime: Anime object

        Examples:
            >>> aiojikan = AioJikan()
            >>> anime = await aiojikan.get_anime_full(1)
        """

        endpoint = f"anime/{anime_id}/full"
        response = await self._get(endpoint)

        return Anime(**response["data"])

    async def get_anime_characters(self, anime_id: int) -> AnimeCharacters:
        """Get anime characters

        Args:
            anime_id (int): Anime ID

        Returns:
            AnimeCharacters: AnimeCharacters object

        Examples:
            >>> aiojikan = AioJikan()
            >>> characters = await aiojikan.get_anime_characters(1)
        """

        endpoint = f"anime/{anime_id}/characters"
        response = await self._get(endpoint)

        return AnimeCharacters(**response)

    async def get_anime_staff(self, anime_id: int) -> AnimeStaff:
        """Get anime staff

        Args:
            anime_id (int): Anime ID

        Returns:
            AnimeStaff: AnimeStaff object

        Examples:
            >>> aiojikan = AioJikan()
            >>> staff = await aiojikan.get_anime_staff(1)
        """

        endpoint = f"anime/{anime_id}/staff"
        response = await self._get(endpoint)

        return AnimeStaff(**response)

    async def get_anime_episodes(self, anime_id: int) -> AnimeEpisodes:
        """Get anime episodes

        Args:
            anime_id (int): Anime ID

        Returns:
            AnimeEpisodes: AnimeEpisodes object

        Examples:
            >>> aiojikan = AioJikan()
            >>> episodes = await aiojikan.get_anime_episodes(1)
        """

        endpoint = f"anime/{anime_id}/episodes"
        response = await self._get(endpoint)

        return AnimeEpisodes(**response)

    async def get_anime_episode(self, anime_id: int, episode: int) -> Episode:
        """Get anime episode

        Args:
            anime_id (int): Anime ID
            episode (int): Episode number

        Returns:
            AnimeEpisodes: AnimeEpisodes object

        Examples:
            >>> aiojikan = AioJikan()
            >>> episode = await aiojikan.get_anime_episode(1, 1)
        """

        endpoint = f"anime/{anime_id}/episodes/{episode}"
        response = await self._get(endpoint)

        return Episode(**response["data"])

    async def get_anime_news(self, anime_id: int, page: int = None) -> AnimeNews:
        """Get anime news

        Args:
            anime_id (int): Anime ID
            page (int, optional): Page number. Defaults to None.

        Returns:
            AnimeNews: AnimeNews object

        Examples:
            >>> aiojikan = AioJikan()
            >>> news = await aiojikan.get_anime_news(1)
        """

        params = {}
        if page:
            params["page"] = page

        endpoint = f"anime/{anime_id}/news"
        response = await self._get(endpoint, params=params)

        return AnimeNews(**response)

    async def search_anime(
        self, search_type: str, query: str, page: int = 1
    ) -> AnimeSearch:
        """Search for anime

        Args:
            search_type (str): Type of search to perform (tv, movie, ova, special, ona, music)
            query (str): Query to search for
            page (int, optional): Page number. Defaults to 1.

        Returns:
            AnimeSearch: AnimeSearch object

        Examples:
            >>> aiojikan = AioJikan()
            >>> result = await aiojikan.search_anime("tv", "naruto")
        """

        endpoint = f"anime"
        params = {"q": query, "page": page, "type": search_type}
        response = await self._get(endpoint, params)

        return AnimeSearch(**response)
