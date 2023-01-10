import unittest

from .testbed import KcBaseTestCase


class TestServerInfo(KcBaseTestCase):
    def test_serverinfo_api(self):
        kc = self.testbed.getKeycloak()
        serverinfo_api = kc.build_serverinfo()

        serverinfo = serverinfo_api.get(None).verify().resp().json()

        expected_server_version_all = [
            "9.0.3",
            "15.0.2",
        ]

        self.assertIsInstance(serverinfo, dict)
        self.assertIn(serverinfo["systemInfo"]["version"], expected_server_version_all)
        expected_sv = serverinfo["systemInfo"]["version"]  # "15.0.2"
        expected_sv_p1 = '.'.join(expected_sv.split('.')[0:1])  # "15"
        expected_sv_p2 = '.'.join(expected_sv.split('.')[0:2])  # "15.0"
        # expected_sv_p2 = '.'.join(expected_sv.split('.')[0:3])

        self.assertEqual(expected_sv, serverinfo["systemInfo"]["version"])
        self.assertEqual("community", serverinfo["profileInfo"]["name"])
        self.assertEqual(expected_sv, kc.server_info.version)
        self.assertEqual("community", kc.server_info.profile_name)

        self.assertEqual("community " + expected_sv_p2, kc.server_info_compound_profile_version())
        self.assertEqual("community " + expected_sv_p1, kc.server_info_compound_profile_version(1))
        self.assertEqual("community " + expected_sv_p2, kc.server_info_compound_profile_version(2))
        self.assertEqual("community " + expected_sv, kc.server_info_compound_profile_version(3))
        self.assertEqual("community " + expected_sv, kc.server_info_compound_profile_version(10))
