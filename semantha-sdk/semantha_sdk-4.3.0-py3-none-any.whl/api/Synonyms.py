from __future__ import annotations

from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.model.Synonyms import Synonym, Synonyms as _SynonymsDTO


class Synonyms(SemanthaAPIEndpoint):
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/synonyms"

    def get_all(self) -> list[Synonym]:
        """ Get all synonyms that are defined for the domain """
        return self._session.get(self._endpoint).execute().to(_SynonymsDTO).synonyms

    def get_one(self, id: str) -> Synonym:
        """ Get a synonym by id """
        return self._session.get(self._endpoint + f"/{id}").execute().to(Synonym)

    def post_word(self, word: str, synonym: str, tags: list[str] = None) -> Synonym:
        """ Create a synonym replacement rule: the word will be replaced by the synonym for semantic matching.

        Args:
            word (str): the word that should be replaced by the synonym (ignored if a regex is provided)
            synonym (str): the synonym that replaces the word
            tags (list[str]): list of tags the synonym should be attached to
        """
        return self._session.post(
            url=self._endpoint,
            json={
                "word": word,
                "synonym": synonym,
                "tags": tags
            }
        ).execute().to(Synonym)

    def post_regex(self, regex: str, synonym: str, tags: list[str] = None) -> Synonym:
        """ Create a synonym replacement rule: the regex (if matched in a document) will be replaced by the synonym for
        semantic matching.

        Args:
            regex (str): the regex that should be replaced by the synonym
            synonym (str): the synonym that replaces the regex
            tags (list[str]): list of tags the synonym should be attached to
        """
        return self._session.post(
            url=self._endpoint,
            json={
                "regex": regex,
                "synonym": synonym,
                "tags": tags
            }
        ).execute().to(Synonym)

    def put_word(self, id: str, word: str, synonym: str, tags: list[str] = None) -> Synonym:
        """ Update a synonym replacement rule by id: the word will be replaced by the synonym for semantic matching.

        Args:
            id (str): id of the synonym that should be updated
            word (str): the updated word that should be replaced by the synonym (ignored if a regex is provided)
            synonym (str): the synonym that replaces the word or the regex
            tags (list[str]): the updated list of tags the synonym should be attached to
        """
        return self._session.put(
            url=self._endpoint + f"/{id}",
            json={
                "word": word,
                "synonym": synonym,
                "tags": tags
            }
        ).execute().to(Synonym)

    def put_regex(self, id: str, regex: str, synonym: str, tags: list[str] = None) -> Synonym:
        """ Update a synonym replacement rule by id: the regex (if matched in a document) will be replaced by the
        synonym for semantic matching.

        Args:
            id (str): id of the synonym that should be updated
            regex (str): the updated regex that should be replaced by the synonym
            synonym (str): the synonym that replaces the word or the regex
            tags (list[str]): the updated list of tags the synonym should be attached to
        """
        return self._session.put(
            url=self._endpoint + f"/{id}",
            json={
                "regex": regex,
                "synonym": synonym,
                "tags": tags
            }
        ).execute().to(Synonym)

    def delete_all(self):
        """ Delete all synonyms """
        self._session.delete(self._endpoint).execute()

    def delete_one(self, id: str):
        """ Delete a synonym by id """
        self._session.delete(self._endpoint + f"/{id}").execute()
