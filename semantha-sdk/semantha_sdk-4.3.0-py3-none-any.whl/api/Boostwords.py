from __future__ import annotations

from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.model.Boostwords import Boostword, Boostwords as _BoostwordsDTO


class Boostwords(SemanthaAPIEndpoint):
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/boostwords"

    def get_all(self) -> list[Boostword]:
        """ Get all boostwords """
        return self._session.get(self._endpoint).execute().to(_BoostwordsDTO).boostwords

    def post_word(self, word: str, tags: list[str] = None) -> Boostword:
        """ Create a boostword as plain word (str).

        Args:
            id (str): id of the boostword that should be updated
            word (str): the new boostword (ignored if a regex is provided)
            tags (list[str]): list of tags the boostword should be attached to
        """
        return self._session.post(
            url=self._endpoint,
            json={
                "word": word,
                "tags": tags
            }
        ).execute().to(Boostword)

    def post_regex(self, regex: str, tags: list[str] = None) -> Boostword:
        """ Create a boostword as regex (regex represented as str).

        Args:
            id (str): id of the boostword that should be updated
            regex (str): the new boostword regex
            tags (list[str]): list of tags the boostword should be attached to
        """
        return self._session.post(
            url=self._endpoint,
            json={
                "regex": regex,
                "tags": tags
            }
        ).execute().to(Boostword)

    def delete_all(self):
        """ Delete all boostwords """
        self._session.delete(self._endpoint).execute()

    def get_one(self, id: str) -> Boostword:
        """ Get a boostword by id """
        return self._session.get(self._endpoint + f"/{id}").execute().to(Boostword)

    def put_word(self, id: str, word: str, tags: list[str] = None) -> Boostword:
        """ Update a boostword as plain word (str) by id.

        Args:
            id (str): id of the boostword that should be updated
            word (str): the updated boostword
            tags (list[str]): list of tags the boostword should be attached to
        """
        return self._session.put(
            url=self._endpoint + f"/{id}",
            json={
                "word": word,
                "tags": tags
            }
        ).execute().to(Boostword)

    def put_regex(self, id: str, regex: str, tags: list[str] = None) -> Boostword:
        """ Update a boostword as regex (regex represented as str) by id.

        Args:
            id (str): id of the boostword that should be updated
            regex (str): the updated boostword regex
            tags (list[str]): list of tags the boostword should be attached to
        """
        return self._session.put(
            url=self._endpoint + f"/{id}",
            json={
                "regex": regex,
                "tags": tags
            }
        ).execute().to(Boostword)

    def delete_one(self, id: str):
        """ Delete a boostword by id """
        self._session.delete(self._endpoint + f"/{id}").execute()
