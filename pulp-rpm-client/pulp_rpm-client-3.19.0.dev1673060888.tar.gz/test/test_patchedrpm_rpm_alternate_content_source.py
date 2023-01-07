# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.models.patchedrpm_rpm_alternate_content_source import PatchedrpmRpmAlternateContentSource  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException

class TestPatchedrpmRpmAlternateContentSource(unittest.TestCase):
    """PatchedrpmRpmAlternateContentSource unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PatchedrpmRpmAlternateContentSource
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_rpm.models.patchedrpm_rpm_alternate_content_source.PatchedrpmRpmAlternateContentSource()  # noqa: E501
        if include_optional :
            return PatchedrpmRpmAlternateContentSource(
                name = '0', 
                last_refreshed = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                paths = [
                    '0'
                    ], 
                remote = '0'
            )
        else :
            return PatchedrpmRpmAlternateContentSource(
        )

    def testPatchedrpmRpmAlternateContentSource(self):
        """Test PatchedrpmRpmAlternateContentSource"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
