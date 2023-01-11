from w.services.technical.url_service import UrlService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestUrlService(TestCaseMixin):

    """
    get_url_query_string
    """

    def test_get_url_query_string_with_success_return_str(self):
        """Ensure method succeed"""
        assert "param1=value1" == UrlService.get_url_query_string(param1="value1")
        assert "param1=value1&param2=154" == UrlService.get_url_query_string(
            param1="value1", param2=154
        )
        assert (
            "param1=value1+with+%40+%24+%C3%B9&param2=154"
            == UrlService.get_url_query_string(param1="value1 with @ $ ù", param2=154)
        )

    """
    resolve_absolute_url
    """

    def test_resolve_absolute_url_with_success_return_str(self):
        """Ensure method succeed"""
        cases = [
            ("http://baseurl.test", "/relative/url"),
            ("http://baseurl.test/", "/relative/url"),
            ("http://baseurl.test", "relative/url"),
            ("http://baseurl.test/", "relative/url"),
        ]
        for base, relative in cases:
            assert (
                "http://baseurl.test/relative/url"
                == UrlService.resolve_absolute_url(base, relative)
            )

    """
    is_valid_url
    """

    def test_is_valid_url_with_invalid_url_return_false(self):
        """Ensure we return false if url not in valid format"""
        invalid_url = "pas une url"
        response = UrlService.is_valid_url(url=invalid_url)
        assert response is False

    def test_is_valid_url_with_valid_url_return_true(self):
        """Ensure we return true if url is in valid format"""
        valid_url = "https://www.mondomaine.com"
        response = UrlService.is_valid_url(url=valid_url)
        assert response is True
