import requests

from .models import (
    Anime,
    AnimeSearch,
    AnimeCharacters,
    AnimeStaff,
    AnimeEpisodes,
    Episode,
    AnimeNews,
)
from .utils.limiter import Limiter


class Jikan:
    """Jikan wrapper for the jikan.moe API"""

    def __init__(
        self, base_url: str = "https://api.jikan.moe/v4", rate_limit: int = 60
    ):
        """Construct a Jikan object

        Args:
            base_url (str, optional): Base URL for Jikan API. Defaults to "https://api.jikan.moe/v4".
            rate_limit (int, optional): Rate limit in requests per minute. Defaults to 60.

        Returns:
            Jikan: Jikan object

        Examples:
            >>> jikan = Jikan()
            >>> jikan = Jikan("https://api.jikan.moe/v4")
        """

        base_url = base_url.rstrip("/")
        self.base_url = base_url
        self.session = requests.Session()

        if rate_limit:
            self.rate_limiter = Limiter(calls_limit=rate_limit, period=60, spread=True)
            self._get = self.rate_limiter.__call__(self._get)

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request to the Jikan API

        Args:
            endpoint (str): Endpoint to request
            params (dict, optional): Parameters to send with request. Defaults to None.

        Returns:
            dict: JSON response from Jikan API
        """

        url = f"{self.base_url}/{endpoint}"

        response = self.session.get(url, params=params)

        response.raise_for_status()
        return response.json()

    def get_anime(self, anime_id: int) -> Anime:
        """Get anime information

        Args:
            anime_id (int): Anime ID

        Returns:
            Anime: Anime object

        Examples:
            >>> jikan = Jikan()
            >>> anime = jikan.get_anime(1)
        """

        endpoint = f"anime/{anime_id}"
        response = self._get(endpoint)
        return Anime(**response["data"])

    def get_anime_full(self, anime_id: int) -> Anime:
        """Get anime information with full details

        Args:
            anime_id (int): Anime ID

        Returns:
            Anime: Anime object

        Examples:
            >>> jikan = Jikan()
            >>> anime = jikan.get_anime_full(1)
        """

        endpoint = f"anime/{anime_id}/full"
        response = self._get(endpoint)
        return Anime(**response["data"])

    def get_anime_characters(self, anime_id: int) -> AnimeCharacters:
        """Get anime characters

        Args:
            anime_id (int): Anime ID

        Returns:
            AnimeCharacters: AnimeCharacters object

        Examples:
            >>> jikan = Jikan()
            >>> characters = jikan.get_anime_characters(1)
        """

        endpoint = f"anime/{anime_id}/characters"
        response = self._get(endpoint)
        return AnimeCharacters(**response)

    def get_anime_staff(self, anime_id: int) -> AnimeStaff:
        """Get anime staff

        Args:
            anime_id (int): Anime ID

        Returns:
            AnimeStaff: AnimeStaff object

        Examples:
            >>> jikan = Jikan()
            >>> staff = jikan.get_anime_staff(1)
        """

        endpoint = f"anime/{anime_id}/staff"
        response = self._get(endpoint)
        return AnimeStaff(**response)

    def get_anime_episodes(self, anime_id: int) -> AnimeEpisodes:
        """Get anime episodes

        Args:
            anime_id (int): Anime ID

        Returns:
            AnimeEpisodes: AnimeEpisodes object

        Examples:
            >>> jikan = Jikan()
            >>> episodes = jikan.get_anime_episodes(1)
        """

        endpoint = f"anime/{anime_id}/episodes"
        response = self._get(endpoint)
        return AnimeEpisodes(**response)

    def get_anime_episode(self, anime_id: int, episode: int) -> Episode:
        """Get anime episode

        Args:
            anime_id (int): Anime ID
            episode (int): Episode number

        Returns:
            Episode: Episode object

        Examples:
            >>> jikan = Jikan()
            >>> episode = jikan.get_anime_episode(1, 1)
        """

        endpoint = f"anime/{anime_id}/episodes/{episode}"
        response = self._get(endpoint)
        return Episode(**response["data"])

    def get_anime_news(self, anime_id: int, page: int = None) -> AnimeNews:
        """Get anime news

        Args:
            anime_id (int): Anime ID
            page (int, optional): Page number. Defaults to None.

        Returns:
            AnimeNews: AnimeNews object

        Examples:
            >>> jikan = Jikan()
            >>> news = jikan.get_anime_news(1)
        """

        params = {}
        if page:
            params["page"] = page

        endpoint = f"anime/{anime_id}/news"
        response = self._get(endpoint, params=params)

        return AnimeNews(**response)

    def search_anime(self, search_type: str, query: str, page: int = 1) -> AnimeSearch:
        """Search for anime

        Args:
            search_type (str): Type of search to perform (tv, movie, ova, special, ona, music)
            query (str): Query to search for
            page (int, optional): Page number. Defaults to 1.

        Returns:
            AnimeSearch: AnimeSearch object

        Examples:
            >>> jikan = Jikan()
            >>> result = jikan.search_anime("tv", "naruto")
        """

        endpoint = f"anime"
        params = {"q": query, "page": page, "type": search_type}
        response = self._get(endpoint, params)

        return AnimeSearch(**response)
