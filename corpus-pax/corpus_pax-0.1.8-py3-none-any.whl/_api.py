from http import HTTPStatus
from typing import Any
from zoneinfo import ZoneInfo

import httpx
from dateutil import parser
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(find_dotenv())

CORPUS_URL = "https://api.github.com/repos/justmars/corpus-entities"
ARTICLES_URL = "https://api.github.com/repos/justmars/lawsql-articles"


class CloudflareSetup(BaseSettings):
    """Sets up ability to upload images to Cloudflare."""

    Account: str = Field(..., repr=False, env="CF_ACCT")
    Token: str = Field(..., repr=False, env="CF_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def url(self):
        return f"https://api.cloudflare.com/client/v4/accounts/{self.Account}/images/v1"

    def set_avatar(self, img_id: str, img: bytes) -> str:
        """Upload avatar by to Cloudflare Images. This implies an image with the word `avatar` as the filename with an image extenion like .png, .jpeg."""
        # delete existing image with same id
        _ = httpx.delete(
            url=f"{self.url}/{img_id}",  # remove image with same id
            headers={"Authorization": f"Bearer {self.Token}"},
        )
        r = httpx.post(
            url=self.url,
            headers={"Authorization": f"Bearer {self.Token}"},
            data={"id": img_id},
            files={"file": (img_id, img)},
            timeout=httpx.Timeout(60.0),  # httpx defaults to 10 sec
        )
        if r.status_code == HTTPStatus.OK:
            return img_id
        raise Exception(f"Could not update image {r.json()}")


class GithubAccess(BaseSettings):
    """Sets up ability to access content from Github.

    With respect to the requisite headers, see:
    https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#get-repository-content--code-samples
    """

    Token: str = Field(..., repr=False, env="GH_TOKEN")
    Version: str = Field("2022-11-28", repr=False, env="GH_TOKEN_VERSION")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def fetch(
        self,
        url: str,
        media_type: str | None = ".raw",
        params: dict = {},
    ) -> httpx.Response:
        with httpx.Client() as client:
            headers = {
                "Accept": f"application/vnd.github{media_type}",
                "Authorization": f"token {self.Token}",
                "X-GitHub-Api-Version": self.Version,
            }
            return client.get(url, params=params, headers=headers)

    def fetch_entities(self, path: str) -> list[dict[str, Any]]:
        if path not in ("members", "orgs"):
            raise Exception(f"Improper {path=}")
        url = f"{CORPUS_URL}/contents/{path}"
        if resp := self.fetch(url):
            return resp.json()
        raise Exception(f"Could not fetch corpus entity: {url}")

    def fetch_articles(self) -> list[dict[str, Any]]:
        """Get the github repository `/articles` files metadata. Each item
        in the response will look likeso:

        ```python shell
        >>> from corpus_pax._api import gh
        >>> arts = gh.fetch_articles()
        >>> arts[1] # arts[0] is an __init__.py file
        {'name': 'digital-legal-text.md',
        'path': 'content/digital-legal-text.md',
        'sha': xxx,
        'size': 7714,
        'url': xxx,
        'html_url': xxx,
        'git_url': xxx,
        'download_url': xxx,
        'type': 'file',
        '_links': {'self': xxx, 'git': xxx, 'html': xxx}}
        ```
        """
        url = f"{ARTICLES_URL}/contents/content"
        if resp := self.fetch(url):
            return resp.json()
        raise Exception(f"Could not fetch articles content: {url}")

    def fetch_article_date_modified(self, path: str) -> float:
        """Get the latest commit date of an article `path` to get its date last modified"""
        url = f"{ARTICLES_URL}/commits"
        params = {"path": path, "page": 1, "per_page": 1}
        if resp := self.fetch(url=url, media_type="+json", params=params):
            return (
                parser.parse(resp.headers["date"])
                .astimezone(ZoneInfo("Asia/Manila"))
                .timestamp()
            )
        raise Exception(f"Could not fetch articles content: {url}")


gh = GithubAccess()  # type: ignore
cf = CloudflareSetup()  # type: ignore
