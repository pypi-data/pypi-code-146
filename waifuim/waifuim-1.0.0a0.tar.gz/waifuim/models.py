"""
MIT License

Copyright (c) 2023 Avimetry Development

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing_extensions import NotRequired


class ImageResponseData(TypedDict):
    """
    Represents the raw image response data from the API.
    """
    images: list[ImageData]


class TagData(TypedDict):
    tag_id: int
    name: str
    description: str
    is_nsfw: bool


class ImageData(TypedDict):
    """
    Class representing the data of an image.
    """
    signature: str
    extension: str
    image_id: int
    favourites: int
    dominant_color: str
    source: str
    uploaded_at: str
    liked_at: str | None
    is_nsfw: bool
    width: int
    height: int
    url: str
    preview_url: str
    tags: list[TagData]


class ImageParams(TypedDict):
    user_id: NotRequired[int]
    included_tags: Sequence[str] | None
    excluded_tags: Sequence[str] | None
    is_nsfw: bool | None
    gif: bool | None
    order_by: str | None
    orientation: str | None
    many: bool | None
    included_files: Sequence[str] | None
    excluded_files: Sequence[str] | None


class EditFavouriteParams(TypedDict):
    user_id: int
    image_id: int


@dataclass
class Tag:
    """
    Class representing a tag.
    """

    tag_id: int
    name: str
    description: str
    is_nsfw: bool

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Tag name={self.name}>"

    @classmethod
    def from_dict(cls, data: TagData) -> Tag:
        return cls(tag_id=data["tag_id"], name=data["name"], description=data["description"], is_nsfw=data["is_nsfw"])


@dataclass
class Image:
    """
    Class representing an image.
    """

    signature: str
    extension: str
    id: int
    favourites: int
    dominant_color: str
    source: str
    uploaded_at: datetime | str | None
    liked_at: datetime | str | None
    is_nsfw: bool
    width: int
    height: int
    url: str
    preview_url: str
    tags: list[Tag]

    def __str__(self) -> str:
        return self.url

    def __repr__(self) -> str:
        return f"<Image url={self.url}>"

    @classmethod
    def from_dict(cls, data: ImageData) -> Image:
        try:
            uploaded_at = datetime.fromisoformat(data["uploaded_at"])
            liked_at = datetime.fromisoformat(data["liked_at"]) if data["liked_at"] else None
        except ValueError:
            uploaded_at = data["uploaded_at"]
            liked_at = data["liked_at"] or None
        tags = [Tag.from_dict(tag) for tag in data["tags"]]
        return cls(
            signature=data["signature"],
            extension=data["extension"],
            id=data["image_id"],
            favourites=data["favourites"],
            dominant_color=data["dominant_color"],
            source=data["source"],
            uploaded_at=uploaded_at,
            liked_at=liked_at,
            is_nsfw=data["is_nsfw"],
            width=data["width"],
            height=data["height"],
            url=data["url"],
            preview_url=data["preview_url"],
            tags=tags,
        )
