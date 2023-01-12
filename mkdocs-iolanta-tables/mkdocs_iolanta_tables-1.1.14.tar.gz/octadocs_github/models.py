from typing import TypedDict

from rdflib import Namespace


class RepoDescription(TypedDict):
    """GitHub repo description from API."""

    stargazers_count: int


GH = Namespace('https://octadocs.io/github/')
SPDX = Namespace('http://spdx.org/licenses/')
