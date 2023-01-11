import requests

class ConsumetAPI:
    """
    A wrapper class for the consumet api.
    """
    def __init__(self, base_url='https://api.consumet.org'):
        """
        Initialize the ConsumetAPI object with a base URL for the API.
        :param base_url: str: The base URL for the API (default: 'https://api.consumet.org')
        """
        self.base_url = base_url
        self.anime = self.Anime()

    class Anime:
        """
        A class for the Anime category of the ConsumetAPI.
        """
        def __init__(self):
            """
            Initialize the Anime object and create instances of the AnimePahe, Enime, Gogoanime and Zoro classes.
            """
            self.animepahe = self.AnimePahe()
            self.enime = self.Enime()
            self.gogoanime = self.Gogoanime()
            self.zoro = self.Zoro()
            self.animepahe = self.AnimePahe()
            self.enime = self.Enime()
            self.gogoanime = self.Gogoanime()
            self.zoro = self.Zoro()

        class AnimePahe:
            """
            A class for the animepahe provider of the ConsumetAPI.
            """
            def search(self, query):
                """
                Search for an anime by title.
                :param query: str: The title of the anime to search for.
                :return: dict: The search results in json format
                """
                url = f'{self.base_url}/anime/animepahe/{query}'
                return requests.get(url).json()

            def info(self, id):
                """
                Get detailed information about an anime.
                :param id: str: The id of the anime to get information for.
                :return: dict: The anime's information in json format
                """
                url = f'{self.base_url}/anime/animepahe/info/{id}'
                return requests.get(url).json()

            def watch(self, episodeId):
                """
                Get streaming links for an episode of an anime.
                :param episodeId: str: The id of the episode to watch.
                :return: dict: The episode information in json format
                """
                url = f'{self.base_url}/anime/animepahe/watch/{episodeId}'
                return requests.get(url).json()

        class Enime:
            """
            A class for the enime provider of the ConsumetAPI.
            """
            def search(self, query):
                """
                Search for an anime by title.
                :param query: str: The title of the anime to search for.
                :return: dict: The search results in json format
                """
                url = f'{self.base_url}/anime/enime/{query}'
                return requests.get(url).json()

            def info(self, id):
                """
                Get detailed information about an anime.
                :param id: str: The id of the anime to get information for.
                :return: dict: The anime's information in json format
                """
                url = f'{self.base_url}/anime/enime/info?id={id}'
                return requests.get(url).json()

            def watch(self, episodeId):
                """
                Get streaming links for an episode of an anime.
                :param episodeId: str: The id of the episode to watch.
                :return: dict: The episode information in json format
                """
                url = f'{self.base_url}/anime/enime/watch?episodeId={episodeId}'
                return requests.get(url).json()

        class Gogoanime:
            """
            A class for the gogoanime provider of the ConsumetAPI.
            """
            def search(self, query):
                """
                Search for an anime by title.
                :param query: str: The title of the anime to search for.
                :return: dict: The search results in json format
                """
                url = f'{self.base_url}/anime/gogoanime/{query}'
                return requests.get(url).json()

            def info(self, id):
                """
                Get detailed information about an anime.
                :param id: str: The id of the anime to get information for.
                :return: dict: The anime's information in json format
                """
                url = f'{self.base_url}/anime/gogoanime/info/{id}'
                return requests.get(url).json()

            def top_airing(self, page=1):
                """
                Get the top airing anime.
                :param page: int: The page number of top airing anime to get.
                :return: dict: The top airing anime in json format
                """
                url = f'{self.base_url}/anime/gogoanime/top-airing'
                params = {'page': page}
                return requests.get(url, params=params).json()

            def recent_episodes(self, type=1, page=1):
                """
                Get the recent episodes of an anime.
                :param type: int : type of anime (1 for Japanese with subtitles, 2 for English/dub without subtitles, 3 for chinese with english subtitles)
                :param page: int : The page number of recent episode of anime to get.
                :return: dict: The recent episodes in json format
                """
                url = f'{self.base_url}/anime/gogoanime/recent-episodes'
                params = {'type': type, 'page': page}
                return requests.get(url, params=params).json()

            def watch(self, episodeId, server='gogocdn'):
                """
                Watch the episode of an anime
                :param episodeId: str: The id of the episode to watch.
                :param server: str: the server to use
                :return: dict: The episode information in json format
                """
                url = f'{self.base_url}/anime/gogoanime/watch/{episodeId}'
                params = {'server': server}
                return requests.get(url, params=params).json()

            def servers(self, episodeId):
                """
                Get the servers for an anime episode
                :param episodeId: str: The id of the episode
                :return: dict: servers for the episode in json format
                """
                url = f'{self.base_url}/anime/gogoanime/servers/{episodeId}'
                return requests.get(url).json()

class Zoro:
            """
            A class for the zoro provider of the ConsumetAPI.
            """
            def search(self, query):
                """
                Search for an anime by title.
                :param query: str: The title of the anime to search for.
                :return: dict: The search results in json format
                """
                url = f'{self.base_url}/anime/zoro/{query}'
                return requests.get(url).json()
            def recent_episodes(self, page=1):
                """
                Get the recent episodes of an anime.
                :param page: int : The page number of recent episode of anime to get.
                :return: dict: The recent episodes in json format
                """
                url = f'{self.base_url}/anime/zoro/recent-episodes'
                params = {'page': page}
                return requests.get(url, params=params).json()
            def info(self, id):
                """
                Get detailed information about an anime.
                :param id: str: The id of the anime to get information for.
                :return: dict: The anime's information in json format
                """
                url = f'{self.base_url}/anime/zoro/info?id={id}'
                return requests.get(url).json()
            def watch(self, episodeId):
                """
                Watch the episode of an anime
                :param episodeId: str: The id of the episode to watch.
                :return: dict: The episode information in json format
                """
                url = f'{self.base_url}/anime/zoro/watch?episodeId={episodeId}'
                return requests.get(url).json()

