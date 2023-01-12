"""Test the gator.api.client module."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from pytest_httpserver import HTTPServer
from gator.core.schemas.timetable import CourseSchema, OrganisationSchema

from gator.api.client import GatorClient

fixtures_dir = Path(__file__).parent / 'fixtures'


class TestGatorClient:
    """Test the :class:`gator.api.client.GatorClient` class."""
    @staticmethod
    @pytest.mark.usefixtures('httpserver')
    @pytest.fixture
    def gator_client(httpserver: HTTPServer) -> GatorClient:
        """Configures a GatorClient for testing."""
        return GatorClient(httpserver.url_for('/'))

    @pytest.mark.usefixtures('gator_client', 'httpserver')
    def test_get_courses_all(self, gator_client: GatorClient,
                             httpserver: HTTPServer) -> None:
        """Test the get_courses API method with no ids parameter."""
        courses_fixture = json.load(open(fixtures_dir / 'courses_all.json'))
        httpserver.expect_request('/courses', method='GET').respond_with_json(
            courses_fixture)

        expected = SimpleNamespace(
            courses=CourseSchema(many=True).load(courses_fixture['courses']),
            last_id=courses_fixture['last_id'],
        )

        assert gator_client.get_courses() == expected

    @pytest.mark.usefixtures('gator_client', 'httpserver')
    def test_get_courses_some(self, gator_client: GatorClient,
                              httpserver: HTTPServer) -> None:
        """Test the get_courses API method with ids parameter."""
        courses_fixture = json.load(open(fixtures_dir / 'courses_some.json'))
        course_ids = [c['id'] for c in courses_fixture['courses']]

        httpserver.expect_request(
            '/courses',
            query_string=dict(ids=','.join(course_ids)),
            method='GET'
        ).respond_with_json(courses_fixture)

        expected = SimpleNamespace(
            courses=CourseSchema(many=True).load(courses_fixture['courses']),
            last_id=courses_fixture['last_id'],
        )

        # Test comma-separated input
        assert gator_client.get_courses(ids=','.join(course_ids)) == expected
        # Test list input
        assert gator_client.get_courses(ids=course_ids) == expected

    @pytest.mark.usefixtures('gator_client', 'httpserver')
    def test_get_course(self, gator_client: GatorClient,
                        httpserver: HTTPServer) -> None:
        """Test the get_course API method."""
        course_fixture = json.load(open(fixtures_dir / 'course_ACT350.json'))
        course_id = course_fixture['id']

        httpserver.expect_request(f'/courses/{course_id}', method='GET')\
            .respond_with_json(course_fixture)

        expected = CourseSchema().load(course_fixture)

        assert gator_client.get_course('ACT350H1-F-20229') == expected

    @pytest.mark.usefixtures('gator_client', 'httpserver')
    def test_get_organisations(self, gator_client: GatorClient,
                               httpserver: HTTPServer) -> None:
        """Test the get_organisations API method."""
        organisations_fixture = json.load(open(
            fixtures_dir / 'organisations.json'))

        httpserver.expect_request('/organisations', method='GET').respond_with_json(
            organisations_fixture)

        expected = SimpleNamespace(
            organisations=OrganisationSchema(many=True).load(
                organisations_fixture['organisations']),
            last_id=organisations_fixture['last_id'],
        )

        assert gator_client.get_organisations() == expected

    @pytest.mark.usefixtures('gator_client', 'httpserver')
    def test_get_organisation(self, gator_client: GatorClient,
                              httpserver: HTTPServer) -> None:
        """Test the get_organisation API method."""
        organisation_fixture = json.load(open(
            fixtures_dir / 'organisation_MAT.json'))

        organisation_code = organisation_fixture['code']

        httpserver.expect_request(f'/organisations/{organisation_code}', method='GET')\
            .respond_with_json(organisation_fixture)

        expected = OrganisationSchema().load(organisation_fixture)

        assert gator_client.get_organisation('MAT') == expected
