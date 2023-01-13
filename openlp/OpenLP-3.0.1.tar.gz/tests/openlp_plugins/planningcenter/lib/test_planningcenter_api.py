# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2023 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
Package to test the openlp.plugins.planningcenter.lib.planningcenter_api package.
"""
import os
import urllib.error
from unittest import TestCase
from unittest.mock import patch

from openlp.plugins.planningcenter.lib.planningcenter_api import PlanningCenterAPI
from tests.helpers.testmixin import TestMixin

TEST_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'resources', 'planningcenter'))


class TestPlanningCenterAPI(TestCase, TestMixin):
    """
    Test the PlanningCenterAPI class
    """
    def test_init(self):
        """
        Test that the api class can be instantiated with an application_id and secret
        """
        # GIVEN: A PlanningCenterAPI Class
        # WHEN:  __init__ is called with an application id and secret
        api = PlanningCenterAPI('application_id', 'secret')
        # THEN:
        # airplane mode should be false
        self.assertFalse(api.airplane_mode, 'Class init without airplane mode')

    def test_init_with_airplane_mode(self):
        """
        Test that the api class can be instantiated with an application_id and secret
        """
        # GIVEN: A PlanningCenterAPI Class
        # WHEN:  __init__ is called with an application id and secret and airplane_dir mocked
        with patch('openlp.plugins.planningcenter.lib.planningcenter_api.os.path.isdir') as airplane_isdir:
            airplane_isdir.return_value = True
            api = PlanningCenterAPI('application_id', 'secret')
        # THEN:
        # airplane mode should be true
        self.assertTrue(api.airplane_mode, 'Class init with airplane mode')

    def test_get_from_services_api(self):
        """
        Test that the get_from_services_api can be called in airplane mode
        """
        # GIVEN: A PlanningCenterAPI Class
        # WHEN:  get_from_services_api is called with empty string as input ('') and airplane mode enabled
        with patch('openlp.plugins.planningcenter.lib.planningcenter_api.os.path.isdir') as airplane_isdir, \
                patch('openlp.plugins.planningcenter.lib.planningcenter_api.urllib.request.build_opener') \
                as mock_opener, \
                patch('openlp.plugins.planningcenter.lib.planningcenter_api.open'):
            airplane_isdir.return_value = True
            api = PlanningCenterAPI('application_id', 'secret')
            mock_opener().open().read.return_value = "{\"foo\" : \"bar\"}".encode(encoding='UTF-8')
            return_value = api.get_from_services_api('test')
        # THEN:
        # we should get back the return value we mocked
        self.assertEqual(return_value['foo'], 'bar', "get_from_services_api returns correct value")

    def test_check_credentials_returns_empty_string_for_bad_credentials(self):
        """
        Test that check_credentials returns an empty string if authentication fails
        """
        # GIVEN: A PlanningCenterAPI Class with mocked out get_from_services_api that returns a 401 (http auth) error
        api = PlanningCenterAPI('application_id', 'secret')
        with patch.object(api, 'get_from_services_api') as mock_get_services:
            mock_get_services.side_effect = urllib.error.HTTPError(None, 401, None, None, None)
        # WHEN: check_credentials is called
            return_value = api.check_credentials()
        # THEN: we have an empty string returns
        assert return_value == '', "return string is empty for bad authentication"

    def test_check_credentials_raises_other_exceptions(self):
        # GIVEN: A PlanningCenterAPI Class with mocked out get_from_services_api that returns a 400 error
        api = PlanningCenterAPI('application_id', 'secret')
        with patch.object(api, 'get_from_services_api') as mock_get_services:
            mock_get_services.side_effect = urllib.error.HTTPError(None, 300, None, None, None)
            # WHEN: check_credentials is called in a try block
            error_code = 0
            try:
                api.check_credentials()
            except urllib.error.HTTPError as error:
                error_code = error.code
        # THEN: we received an exception with code of 300
        assert error_code == 300, "correct exception is raised from check_credentials"

    def test_check_credentials_pass(self):
        """
        Test that check_credentials can be called in airplane mode
        """
        # GIVEN: A PlanningCenterAPI Class
        # WHEN:  get_from_services_api is called with empty string as input ('') and airplane mode enabled
        with patch('openlp.plugins.planningcenter.lib.planningcenter_api.os.path.isdir') as airplane_isdir, \
                patch('openlp.plugins.planningcenter.lib.planningcenter_api.urllib.request.build_opener') \
                as mock_opener, \
                patch('openlp.plugins.planningcenter.lib.planningcenter_api.open'):
            airplane_isdir.return_value = True
            api = PlanningCenterAPI('application_id', 'secret')
            mock_opener().open().read.return_value = "{\"data\": {\"attributes\": {\"name\": \"jpk\"}}}".\
                encode(encoding='UTF-8')
            return_value = api.check_credentials()
        # THEN:
        # Check credentials returns our mocked value
        self.assertEqual(return_value, 'jpk', "check_credentials returns correct value for pass")
