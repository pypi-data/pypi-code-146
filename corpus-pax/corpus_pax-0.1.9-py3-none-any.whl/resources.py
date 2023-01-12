import datetime
import io
from enum import Enum
from http import HTTPStatus
from typing import NamedTuple
from urllib.parse import urlparse

import yaml
from jinja2 import Environment, PackageLoader, select_autoescape
from pydantic import BaseModel, EmailStr, Field, HttpUrl

from ._api import cf, gh

persons_env = Environment(
    loader=PackageLoader("corpus_pax"), autoescape=select_autoescape()
)

DETAILS_FILE = "details.yaml"
AVATAR_IMG = "avatar.jpeg"
"""Each member / entity folder will have a `details.yaml` and an `avatar.jpeg`."""


class RankStatus(int, Enum):
    Prioritized = 1
    Good = 2
    Ordinary = 3
    Ignored = 0


class MemberURL(NamedTuple):
    """Each corpus entity in the `gh` repository will contain 2 files: a details.yaml and an avatar.jpeg.

    The repository's root should contain 2 folders to `orgs` and `members`:

    orgs/ <-- `kind`
        org_a/ <-- `id`

            - details.yaml # contains the key value pairs for the org represented by the id
            - avatar.jpeg # is the image that should be placed in cloudflare
    members/ # same structure for orgs
        member_xyz/

            - details.yaml
            - avatar.jpeg

    Assuming a valid `id` url to the github `gh` repo, the `setter()` function will generate the proper `img_id` to use as a filename for the `cf` storage area.
    """

    id: str
    img_id: str
    target_url: str

    @classmethod
    def setter(cls, url: str, with_img_id: bool = True):
        """Retrieve the id from the path and create a new url for parsing the registered member."""
        obj = urlparse(url)
        parts = obj.path.split("/")
        pk = parts[-1]
        kind = parts[-2]
        img_id = f"{kind}-{pk}"
        new_url = obj.scheme + "://" + obj.netloc + obj.path
        if with_img_id:
            cls.set_avatar_from(img_id, new_url)
        return cls(id=pk, img_id=img_id, target_url=new_url)

    @classmethod
    def set_avatar_from(cls, id: str, url: str) -> str:
        """Add the avatar jpeg from github to cloudflare, retrieve the cloudflare id."""
        obj = f"{url}/{AVATAR_IMG}"
        if img_resp := gh.fetch(obj):
            if img_resp.status_code != HTTPStatus.OK:
                raise Exception(
                    f"See {img_resp.status_code=} github file {obj}; avatar"
                    f" {url=}"
                )
            if img := io.BytesIO(img_resp.content):
                return cf.set_avatar(id, img.read())
        raise Exception(f"Could not setup avatar {url=}")


class RegisteredMember(BaseModel):
    """Common validator for corpus entities: Individuals and Orgs. Note that the `col` attribute is for use in `sqlpyd`."""

    id: str = Field(col=str)
    created: float = Field(col=float)
    modified: float = Field(col=float)
    search_rank: RankStatus | None = Field(
        RankStatus.Ordinary,
        title="Search Rank",
        description="Can use as a means to determine rank in SERP",
        col=int,
    )
    email: EmailStr = Field(col=str)
    img_id: str | None = Field(
        None,
        title="Cloudflare Image ID",
        description=(
            "Based on email, upload a unique avatar that can be called via"
            " Cloudflare Images."
        ),
        col=str,
    )
    display_url: HttpUrl | None = Field(
        title="Associated URL",
        description=(
            "When visiting the profile of the member, what URL is associated"
            " with the latter?"
        ),
        col=str,
    )
    display_name: str = Field(
        ...,
        title="Display Name",
        description="Preferred way of being designated in the platform.",
        min_length=5,
        col=str,
        fts=True,
    )
    caption: str | None = Field(
        None,
        description=(
            "For individuals, the way by which a person is to be known, e.g."
            " Lawyer and Programmer; if an organization, it's motto or quote,"
            " i.e. 'just do it'."
        ),
        col=str,
    )
    description: str | None = Field(
        None,
        title="Member Description",
        description=(
            "Useful for both SEO and for contextualizing the profile object."
        ),
        min_length=10,
        col=str,
        fts=True,
    )
    twitter: str | None = Field(None, title="Twitter username", col=str)
    github: str | None = Field(None, title="Github username", col=str)
    linkedin: str | None = Field(None, title="LinkedIn username", col=str)
    facebook: str | None = Field(None, title="Facebook page", col=str)
    areas: list[str] | None = Field(
        default_factory=list,
        title="Practice Areas",
        description=(
            "Itemized strings, referring to specialization of both natural and"
            " artificial persons, that will be mapped to a unique table"
        ),
        exclude=True,
    )
    categories: list[str] | None = Field(
        default_factory=list,
        title="Entity Categories",
        description=(
            "Itemized strings, referring to type of entity of both natural"
            " (e.g. lawyer) and artificial (e.g. law firm) persons, that will"
            " be mapped to a unique table"
        ),
        exclude=True,
    )
    members: list[dict[str, int | str | EmailStr]] | None = Field(
        default_factory=list, exclude=True
    )

    class Config:
        use_enum_values = True

    @classmethod
    def extract_details(cls, url: str) -> dict:
        """Convert the yaml file in the repository to a dict."""
        if details_resp := gh.fetch(f"{url}/{DETAILS_FILE}"):
            return yaml.safe_load(details_resp.content)
        raise Exception(f"Could not get details from {url=}")

    @classmethod
    def from_url(cls, url: str, set_img: bool = False):
        """Each member url can be converted to a fully validated object via a valid Github `url`; if `set_img` is set to true, an `img_id` is created on Cloudflare."""
        obj = MemberURL.setter(url, set_img)
        return cls(
            **cls.extract_details(obj.target_url),
            id=obj.id,
            img_id=obj.img_id,
            created=datetime.datetime.now().timestamp(),
            modified=datetime.datetime.now().timestamp(),
        )
