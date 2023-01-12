"""Web client for the Gator API."""
import json
from types import SimpleNamespace
from typing import Any, Optional, Union
from urllib.parse import quote_plus, urljoin

import certifi
import urllib3
from gator.api.client.helpers import add_url_params
from gator.core.models.timetable import Course, Organisation
from gator.core.schemas.timetable import CourseSchema, OrganisationSchema


class GatorClient:
    """Web client for the Gator API."""

    def __init__(self, base_url: str, encoding: str = 'utf8') -> None:
        """Initialize the client.

        Args:
            base_url: The base URL of the Gator API service.
            encoding: The encoding to use for the requests.
        """
        self._base_url = base_url
        self._encoding = encoding
        self._connection_pool = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )

    # Private methods
    def _compose_url(self, path: str, **params: Any) -> str:
        """Compose a URL for the given path.

        Args:
            path: The path to compose the URL for. This path is relative to the
                base URL.
            **params: The parameters to include in the URL.

        Returns:
            The composed URL.

        Examples:
            >>> client = GatorClient('http://localhost:5000')
            >>> client._compose_url('/api/v1/users', name='John', age=42)
            'http://localhost:5000/api/v1/users?name=John&age=42'
        """
        url = urljoin(self._base_url, path)
        return add_url_params(url, **params)

    def _request(self, method: str, path: str, **params: Any) \
            -> tuple[Any, int]:
        """Make a request to the Gator API.

        Args:
            method: The HTTP method to use for the request.
            path: The path to the resource to request. This path is relative to
                the base URL.
            params: The parameters to include in the request given as a
                dictionary of key-value pairs. If None, no parameters are
                included in the request.

        Returns:
            A tuple containing the JSON response and the HTTP status code.
        """
        url = self._compose_url(path, **params)
        response = self._connection_pool.urlopen(method.upper(), url)

        body = json.loads(response.data.decode(self._encoding))
        return body, response.status

    def _construct_params(self, **kwargs: Any) -> dict:
        """Construct a dictionary of parameters from keyword arguments.

        If a keyword argument is None, it is not included in the resultant
        parameter dictionary.

        Args:
            **kwargs: The keyword arguments to include in the parameters.

        Returns:
            A dictionary of parameters.
        """
        params = {}
        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        return params

    # API methods
    def get_courses(self, ids: Optional[Union[list[str], str]] = None,
                    page_size: Optional[int] = None,
                    last_id: Optional[str] = None) -> SimpleNamespace:
        """GET /courses.

        Args:
            ids: The ids of the courses to retrieve, either as a list of
                strings or a single string of comma-separated ids. If
                specified, returns only those courses with the given ids in the
                order specified. Ignore courses that could not be found.
                Otherwise, return all courses, in no particular order.
            page_size: The number of items to return per page.
            last_id: The id of the last item returned.

        Returns:
            A SimpleNamespace with two attributes:
                - courses: A list of Course objects.
                - last_id: The id of the last item returned.
        """
        if ids is not None and isinstance(ids, list):
            ids = ','.join(ids)

        params = self._construct_params(
            page_size=page_size,
            last_id=last_id,
            ids=ids
        )

        body, _ = self._request('GET', '/courses', **params)
        body['courses'] = CourseSchema(many=True).load(body['courses'])

        return SimpleNamespace(**body)

    def get_course(self, id: str) -> Course:
        """GET /courses/{id}.

        Args:
            id: The id (full code) of the course to retrieve.

        Returns:
            The Course object.
        """
        id_url_safe = quote_plus(id)
        body, _ = self._request('GET', f'/courses/{id_url_safe}')

        return CourseSchema().load(body)

    def get_organisations(self, page_size: Optional[int] = None,
                          last_id: Optional[str] = None) -> SimpleNamespace:
        """GET /organisations.

        Args:
            page_size: The number of items to return per page.
            last_id: The id of the last item returned.

        Returns:
            A SimpleNamespace with two attributes:
                - organisations: A list of Organisation objects.
                - last_id: The id of the last item returned.
        """
        params = self._construct_params(
            page_size=page_size,
            last_id=last_id
        )

        body, _ = self._request('GET', '/organisations', **params)
        body['organisations'] = OrganisationSchema(many=True).load(
            body['organisations']
        )

        return SimpleNamespace(**body)

    def get_organisation(self, code: str) -> Organisation:
        """GET /organisations/{code}.

        Args:
            code: The code of the organisation to retrieve.

        Returns:
            The Organisation object.
        """
        code_url_safe = quote_plus(code)
        body, _ = self._request('GET', f'/organisations/{code_url_safe}')

        return OrganisationSchema().load(body)
