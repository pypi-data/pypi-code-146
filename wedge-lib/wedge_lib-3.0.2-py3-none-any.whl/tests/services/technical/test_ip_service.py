from w.services.technical.ip_service import IpService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestIpService(TestCaseMixin):
    """
    is_valid_ip
    """

    def test_is_valid_ip_with_invalid_ip_return_false(self):
        """Ensure we return false if ip not in valid format"""
        invalid_ip = "1221"
        response = IpService.is_valid_ip(ip=invalid_ip)
        assert response is False

    def test_is_valid_ip_with_valid_ip_return_true(self):
        """Ensure we return true if ip is in valid format"""
        valid_ip = "192.168.1.1"
        response = IpService.is_valid_ip(ip=valid_ip)
        assert response is True
