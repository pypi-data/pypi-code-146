from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os.path


if os.path.isfile("ggru.print"):
    p = True


class FromBaseURL(object):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

        self.__github_urls = self.get_github_urls()
        self.urls = []

        self.__prepare_urls()

    def __prepare_urls(self) -> None:
        r = requests.get(self.base_url)
        soup = BeautifulSoup(r.content, "html.parser")

        for i in soup.prettify().splitlines():
            for j in i.split('"'):
                if j.startswith("http"):
                    new_url = j
                elif j.startswith("/"):
                    new_url = urljoin(self.base_url, j)
                else:
                    continue

                if self.__is_repo_url(new_url) and not new_url in self.urls:
                    self.urls.append(new_url)
                    if p:
                        print(new_url)

    @staticmethod
    def get_github_urls() -> list:
        github_urls = []

        for url in [
            "topics",
            "features",
            "enterprise",
            "_graphql",
            "sponsors",
            "explore",
            "search",
            "marketplace",
            "codespaces",
            "pricing",
            "collections",
            "settings",
            "contact",
            "login",
            ">",
            "opensearch.xml",
            "manifest.json",
            "signup",
            "team",
            "customer-stories",
            "readme",
            "trending",
            "events",
        ]:
            github_urls.append("/{}".format(url))

        return github_urls

    def __is_repo_url(self, url: str) -> bool:
        if not url.startswith("https://github.com/"):
            return False

        if url.count("/") != 4:
            return False

        for github_url in self.__github_urls:
            if github_url in url:
                return False

        return True


class TopicUrls(object):
    def __init__(self) -> None:
        self.urls = []
        self.__prepare_urls(
            [
                "https://github.com/topics",
                "https://github.com/explore",
            ]
        )

    def __prepare_urls(self, urls: list) -> None:
        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")

            for i in soup.prettify().splitlines():
                for j in i.split('"'):
                    if j.startswith("/"):
                        new_url = urljoin(url, j)
                    else:
                        continue

                    if "/topics/" in new_url and not new_url in self.urls:
                        self.urls.append(new_url)


class CollectionUrls(object):
    def __init__(self) -> None:
        self.urls = []
        self.__prepare_urls(
            [
                "https://github.com/collections",
            ]
        )

    def __prepare_urls(self, urls: list) -> None:
        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")

            for i in soup.prettify().splitlines():
                for j in i.split('"'):
                    if j.startswith("/"):
                        new_url = urljoin(url, j)
                    else:
                        continue

                    if "/collections/" in new_url and not new_url in self.urls:
                        self.urls.append(new_url)


class FromExplore(FromBaseURL):
    def __init__(self) -> None:
        super().__init__("https://github.com/explore")


class FromCollections(CollectionUrls):
    def __init__(self) -> None:
        super().__init__()
        self.collection_urls = self.urls
        self.urls = []
        self.__prepare_urls_()

    def __prepare_urls_(self) -> None:
        for url in self.collection_urls:
            fromBaseURL = FromBaseURL(url)
            self.urls += fromBaseURL.urls


class FromTopics(TopicUrls):
    def __init__(self) -> None:
        super().__init__()
        self.topic_urls = self.urls
        self.urls = []
        self.__prepare_urls_()

    def __prepare_urls_(self) -> None:
        for url in self.topic_urls:
            fromBaseURL = FromBaseURL(url)
            self.urls += fromBaseURL.urls


class FromUser(FromBaseURL):
    def __init__(self, username: str) -> None:
        super().__init__("https://github.com/{}?tab=repositories".format(username))


class UserUrls(object):
    def __init__(self) -> None:
        self.urls = []
        self.__prepare_urls(
            [
                "https://github.com/trending/developers",
            ]
        )

    def __prepare_urls(self, urls: list) -> None:
        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")

            for i in soup.prettify().splitlines():
                for j in i.split('"'):
                    if j.startswith("/"):
                        new_url = urljoin(url, j)
                    else:
                        continue

                    if self.__is_user_url(new_url) and not new_url in self.urls:
                        self.urls.append(new_url)

    def __is_user_url(self, url: str) -> bool:
        if not url.startswith("https://github.com/"):
            return False

        if url.count("/") != 3:
            return False

        for github_url in FromBaseURL.get_github_urls():
            if github_url in url:
                return False

        return True

    def more_users(self, urls: list) -> None:
        for url in urls:
            new_user_url = "/".join(url.split("/")[:-1])
            if not new_user_url in self.urls:
                self.urls.append("/".join(url.split("/")[:-1]))


class FromTrending(FromBaseURL):
    def __init__(self) -> None:
        super().__init__("https://github.com/trending")


class AllUrls(object):
    def __init__(self) -> None:
        self.urls = []
        self.__prepare_urls()

    def __prepare_urls(self) -> None:
        fromExplore = FromExplore()
        fromTopics = FromTopics()
        fromCollections = FromCollections()
        fromTrending = FromTrending()

        self.urls += fromExplore.urls
        self.urls += fromTopics.urls
        self.urls += fromCollections.urls
        self.urls += fromTrending.urls

    def more_repos_from_users(self, userUrls: UserUrls) -> None:
        for user in userUrls.urls:
            fromUser = FromUser(user)
            self.urls += fromUser.urls


class AllUrlsWithMore(AllUrls):
    def __init__(self) -> None:
        super().__init__()

        userUrls = UserUrls()
        userUrls.more_users(self.urls)

        self.more_repos_from_users(userUrls)
