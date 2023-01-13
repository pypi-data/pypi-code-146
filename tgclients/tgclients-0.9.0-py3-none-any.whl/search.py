# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""TextGrid Search API."""
import logging
from io import BytesIO
from typing import Optional, List

import requests
from requests.models import Response
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser

from tgclients.config import TextgridConfig
from tgclients.databinding.tgsearch import Response as SearchResponse, TextgridUris

logger = logging.getLogger(__name__)


class TextgridSearchRequest:
    """Provide low level access to the TextGrid search service, returning the response objects."""

    def __init__(self, config: TextgridConfig = TextgridConfig(), nonpublic: bool = False) -> None:
        if nonpublic:
            self._url = config.search
        else:
            self._url = config.search_public
        self._config = config

    def info(self, textgrid_uri: str, sid: Optional[str] = None) -> Response:
        """Retrieve metadata for a textgrid object specified by its
        textgrid-uri

        Args:
            textgrid_uri (str): Textgrid URI
            sid (Optional[str]): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: metadata for uri
        """
        url = self._url + '/info/'
        response = requests.get(
            url + textgrid_uri, {'sid': sid}, timeout=self._config.http_timeout)
        return self._handle_response(response)

    def list_project_root(self, project_id: str, sid: Optional[str] = None) -> Response:
        """Get objects belonging to a project, filtered by objects that are in
        an aggregation in the same project.

        Args:
            project_id (str): the ID of the project to list
            sid (Optional[str], optional): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service, containing a list of textgrid metadata entries
        """
        response = requests.get(
            self._url + '/navigation/' + project_id, {'sid': sid},
            timeout=self._config.http_timeout)
        return self._handle_response(response)

    def list_aggregation(self, textgrid_uri: str, sid: Optional[str] = None) -> Response:
        """Get child resources of an aggregation.

        Args:
            textgrid_uri (str): Textgrid URI
            sid (Optional[str], optional): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service, containing a list of textgrid metadata entries
        """
        response = requests.get(self._url + '/navigation/agg/' +
                                textgrid_uri, {'sid': sid},
                                timeout=self._config.http_timeout)
        return self._handle_response(response)

    # pylint: disable-msg=too-many-arguments,too-many-locals
    def search(self,
               query: Optional[str] = '*',
               sid: Optional[str] = None,
               target: Optional[str] = None,
               order: Optional[str] = None,
               start: Optional[int] = None,
               limit: Optional[int] = None,
               kwic_width: Optional[int] = None,
               word_distance: Optional[int] = None,
               path: Optional[bool] = None,
               all_projects: Optional[bool] = None,
               sandbox: Optional[bool] = None,
               filters: Optional[List[str]] = None,
               facet:  Optional[List[str]] = None,
               facet_limit: Optional[int] = None) -> Response:
        """Run fulltext queries or filters on TextGrid metadata and fulltext objects.

        Please note: as the defaults of this function are mostly set to None, the defaults from
            the service are used, and also noted in this docstring. see:
            http://textgridlab.org/doc/services/submodules/tg-search/docs/api/search.html

        Args:
            query (str, optional): Lucene search string. Defaults to '*'.
            sid (str, optional): TextGrid SessionID from tgauth. Defaults to None.
            target (str, optional): where to do fulltext-searches: one of 'structure',
                                    'metadata' and 'both'. Defaults to 'both'.
            order (str, optional): key-value ascending (asc) or descending (desc) and metadata-field
                                   like asc:title or desc:author. Defaults to 'relevance'.
            start (int, optional): result number to start with.. Defaults to 0.
            limit (int, optional): number of entries to return.. Defaults to 20.
            kwic_width (int, optional): number of chars before and after a kwic match.
                                        Defaults to 40.
            word_distance (int, optional): max distance beetween two words in fulltext query.
                                           ignored if set to a number < 0, then for a hit all words
                                           must be contained in one document. Defaults to -1.
            path (boo], optional): path of found result(work->edition->aggregations) should be
                                   applied to hit. Defaults to false.
            all_projects (bool, optional): all Projects should be searched for public data,
                                           warning: this query may be slow, if many results found.
                                           Defaults to false.
            sandbox (bool, optional): show sandboxed (not yet finally published) data.
                                      Defaults to false.
            filters (List[str], optional): add filter on query results, e.g. for faceting.
                                           Defaults to None.
            facet (List[str], optional): get facets for query results. Defaults to None.
            facet_limit (int, optional): number of results to return for each facet. Defaults to 10.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service - a list of textgrid metadata entries,
                      KWIC hits, paths and facets if requested
        """

        params = {
            'q': query,
            'sid': sid,
            'target': target,
            'order': order,
            'start': start,
            'limit': limit,
            'kwicWidth': kwic_width,
            'wordDistance': word_distance,
            'path': path,
            'allProjects': all_projects,
            'sandbox': sandbox,
            'filter': filters,
            'facet': facet,
            'facetLimit': facet_limit
        }
        response = requests.get(self._url + '/search', params,
                                timeout=self._config.http_timeout)
        return self._handle_response(response)
    # pylint: enable-msg=too-many-arguments,too-many-locals

    def edition_work_metadata_for(self, textgrid_uri: str, sid: Optional[str] = None) -> Response:
        """Find parent edition for an object and the edition and work metadata

        Args:
            textgrid_uri (str): Textgrid URI
            sid (Optional[str], optional): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service - edition and work metadata for given object
                      from first matching parent edition
        """
        response = requests.get(
            self._url + '/info/' + textgrid_uri +
            '/editionWorkMeta', {'sid': sid},
            timeout=self._config.http_timeout)
        return self._handle_response(response)

    def children(self, textgrid_uri: str, sid: Optional[str] = None) -> Response:
        """List URIs for all children of this aggregation and its child aggregations

        Args:
            textgrid_uri (str): Textgrid URI of an aggregation
            sid (Optional[str], optional): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            Response: HTTP response from service - URIs for children of this
                      aggregation and its child aggregations
        """
        response = requests.get(
            self._url + '/info/' + textgrid_uri + '/children', {'sid': sid},
            timeout=self._config.http_timeout)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: Response) -> Response:
        """Error handling for responses from tgsearch

        Args:
            response (Response): a response from tgsearch

        Raises:
            TextgridSearchException: if HTTP status code >= 400

        Returns:
            Response: the response
        """
        if not response.ok:
            message = '[Error] HTTP Code: ' + \
                str(response.status_code) + ' - ' + response.text[0:255]
            logger.warning(message)
            raise TextgridSearchException(message)
        return response


class TextgridSearch(TextgridSearchRequest):
    """Provide access to the TextGrid search service using a XML data binding """

    def __init__(self, config: TextgridConfig = TextgridConfig(), nonpublic: bool = False) -> None:
        super().__init__(config, nonpublic)
        # It’s recommended to either reuse the same parser/serializer instance
        # or reuse the context instance. see https://xsdata.readthedocs.io/en/latest/xml.html
        context = XmlContext()
        self._parser = XmlParser(context=context)

    def info(self, textgrid_uri: str, sid: Optional[str] = None) -> SearchResponse:
        """Retrieve metadata for a textgrid object specified by its
        textgrid-uri

        Args:
            textgrid_uri (str): Textgrid URI
            sid (Optional[str]): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            SearchResponse: metadata for uri
        """
        response = super().info(textgrid_uri, sid)
        return self._parser.parse(BytesIO(response.content), SearchResponse)

    def list_project_root(self, project_id: str, sid: Optional[str] = None) -> SearchResponse:
        """Get objects belonging to a project, filtered by objects that are in
        an aggregation in the same project.

        Args:
            project_id (str): the ID of the project to list
            sid (Optional[str], optional): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            SearchResponse: A list of textgrid metadata entries
        """
        response = super().list_project_root(project_id, sid)
        return self._parser.parse(BytesIO(response.content), SearchResponse)

    def list_aggregation(self, textgrid_uri: str, sid: Optional[str] = None) -> SearchResponse:
        """Get child resources of an aggregation.

        Args:
            textgrid_uri (str): Textgrid URI
            sid (Optional[str], optional): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            SearchResponse: A list of textgrid metadata entries
        """
        response = super().list_aggregation(textgrid_uri, sid)
        return self._parser.parse(BytesIO(response.content), SearchResponse)

    # pylint: disable-msg=too-many-arguments,too-many-locals

    def search(self,
               query: Optional[str] = '*',
               sid: Optional[str] = None,
               target: Optional[str] = None,
               order: Optional[str] = None,
               start: Optional[int] = None,
               limit: Optional[int] = None,
               kwic_width: Optional[int] = None,
               word_distance: Optional[int] = None,
               path: Optional[bool] = None,
               all_projects: Optional[bool] = None,
               sandbox: Optional[bool] = None,
               filters: Optional[List[str]] = None,
               facet:  Optional[List[str]] = None,
               facet_limit: Optional[int] = None) -> SearchResponse:
        """Run fulltext queries or filters on TextGrid metadata and fulltext objects.

        Please note: as the defaults of this function are mostly set to None, the defaults from
            the service are used, and also noted in this docstring. see:
            http://textgridlab.org/doc/services/submodules/tg-search/docs/api/search.html

        Args:
            query (str, optional): Lucene search string. Defaults to '*'.
            sid (str, optional): TextGrid SessionID from tgauth. Defaults to None.
            target (str, optional): where to do fulltext-searches: one of 'structure',
                                    'metadata' and 'both'. Defaults to 'both'.
            order (str, optional): key-value ascending (asc) or descending (desc) and metadata-field
                                   like asc:title or desc:author. Defaults to 'relevance'.
            start (int, optional): result number to start with.. Defaults to 0.
            limit (int, optional): number of entries to return.. Defaults to 20.
            kwic_width (int, optional): number of chars before and after a kwic match.
                                        Defaults to 40.
            word_distance (int, optional): max distance beetween two words in fulltext query.
                                           ignored if set to a number < 0, then for a hit all words
                                           must be contained in one document. Defaults to -1.
            path (boo], optional): path of found result(work->edition->aggregations) should be
                                   applied to hit. Defaults to false.
            all_projects (bool, optional): all Projects should be searched for public data,
                                           warning: this query may be slow, if many results found.
                                           Defaults to false.
            sandbox (bool, optional): show sandboxed (not yet finally published) data.
                                      Defaults to false.
            filters (List[str], optional): add filter on query results, e.g. for faceting.
                                           Defaults to None.
            facet (List[str], optional): get facets for query results. Defaults to None.
            facet_limit (int, optional): number of results to return for each facet. Defaults to 10.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            SearchResponse: a list of textgrid metadata entries,
                            KWIC hits, paths and facets if requested
        """

        response = super().search(query=query,
                                  sid=sid,
                                  target=target,
                                  order=order,
                                  start=start,
                                  limit=limit,
                                  kwic_width=kwic_width,
                                  word_distance=word_distance,
                                  path=path,
                                  all_projects=all_projects,
                                  sandbox=sandbox,
                                  filters=filters,
                                  facet=facet,
                                  facet_limit=facet_limit)
        return self._parser.parse(BytesIO(response.content), SearchResponse)
    # pylint: enable-msg=too-many-arguments,too-many-locals

    def edition_work_metadata_for(self, textgrid_uri: str,
                                  sid: Optional[str] = None) -> SearchResponse:
        """Find parent edition for an object and the edition and work metadata

        Args:
            textgrid_uri (str): Textgrid URI
            sid (Optional[str], optional): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            SearchResponse: Edition and work metadata for given object
                            from first matching parent edition
        """
        response = super().edition_work_metadata_for(textgrid_uri, sid)
        return self._parser.parse(BytesIO(response.content), SearchResponse)

    def children(self, textgrid_uri: str, sid: Optional[str] = None) -> TextgridUris:
        """List URIs for all children of this aggregation and its child aggregations

        Args:
            textgrid_uri (str): Textgrid URI of an aggregation
            sid (Optional[str], optional): Session ID. Defaults to None.

        Raises:
            TextgridSearchException: if HTTP status code >= 400   (# noqa: DAR402)

        Returns:
            TextgridUris: URIs for children of this aggregation and its child aggregations
        """
        response = super().children(textgrid_uri, sid)
        return self._parser.parse(BytesIO(response.content), TextgridUris)


class TextgridSearchException(Exception):
    """Exception communicating with tgsearch"""
