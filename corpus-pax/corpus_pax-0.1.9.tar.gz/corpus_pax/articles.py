import datetime
from typing import Any
from zoneinfo import ZoneInfo

import frontmatter
from dateutil import parser
from pydantic import EmailStr, Field, HttpUrl, constr
from sqlpyd import Connection, TableConfig

from ._api import gh
from .entities import Individual


class Tag(TableConfig):
    __prefix__ = "pax"
    __tablename__ = "tags"
    tag: constr(to_lower=True) = Field(  # type: ignore
        col=str, description="Tagging mechanism for the Article model."
    )


class Article(TableConfig):
    __prefix__ = "pax"
    __tablename__ = "articles"

    url: HttpUrl = Field(col=str)
    id: str = Field(col=str)
    title: str = Field(col=str, fts=True)
    description: str = Field(col=str, fts=True)
    date: datetime.date = Field(..., col=datetime.date, index=True)
    created: float = Field(col=float)
    modified: float = Field(col=float)
    content: str = Field(col=str, fts=True)
    tags: list[str] = Field(
        default_factory=list,
        title="Subject Matter",
        description="Itemized strings, referring to the topic tag involved.",
        exclude=True,
    )
    authors: list[EmailStr] = Field(default_factory=list, exclude=True)

    @classmethod
    def extract_articles(cls):
        """Based on entries parsed from github, ignore files not formatted in .md
        and extract the Pydantic-style model based on frontmatter metadata of
        each markdown article represented by the entries.
        """
        articles = []
        for entry in gh.fetch_articles():
            if fn := entry.get("name"):
                if fn.endswith(".md"):
                    if url := entry.get("url"):
                        id = fn.removesuffix(".md")
                        modified = gh.fetch_article_date_modified(fn)
                        details = cls.extract_markdown_postmatter(url)
                        article = cls(id=id, modified=modified, **details)
                        articles.append(article)
        return articles

    @classmethod
    def extract_markdown_postmatter(cls, url: str) -> dict:
        """Convert the markdown/frontmatter file fetched via url to a dict."""
        mdfile = gh.fetch(url)
        post = frontmatter.loads(mdfile.content)
        d = parser.parse(post["date"]).astimezone(ZoneInfo("Asia/Manila"))
        return {
            "url": url,
            "created": d.timestamp(),
            "date": d.date(),
            "title": post["title"],
            "description": post["summary"],
            "content": post.content,
            "authors": post["authors"],
            "tags": post["tags"],
        }

    @classmethod
    def make_or_replace(cls, c: Connection, extract: Any):
        tbl = c.table(cls)
        row = tbl.insert(extract.dict(), replace=True, pk="id")  # type: ignore
        if row.last_pk:
            for author_email in extract.authors:
                tbl.update(row.last_pk).m2m(
                    other_table=Individual.__tablename__,
                    lookup={"email": author_email},
                    pk="id",
                )
            for tag in extract.tags:
                tbl.update(row.last_pk).m2m(
                    other_table=Tag.__tablename__,
                    lookup=Tag(**{"tag": tag}).dict(),
                )
