import pytest

from w.services.technical.models.request_response import RequestResponse
from w.services.technical.models.request_session import RequestSession
from w.services.technical.request_service import RequestService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestRequestService(TestCaseMixin):
    @staticmethod
    def fix_response_variable_content(response):
        response["_content"]["headers"]["User-Agent"] = "pytest-user_agent"
        response["_content"]["headers"]["X-Amzn-Trace-Id"] = "X-Amzn-Trace-Id"
        # remove all headers beginning by X-
        response["_content"]["headers"] = {
            k: v for k, v in response["_content"]["headers"].items() if k[:2] != "X-"
        }
        response["_content"]["origin"] = "pytest"
        return response

    """
    init_session
    """

    def test_init_session_with_invalid_url_raise_runtime_error(self):
        with pytest.raises(RuntimeError, match="Invalid url 'http//foobar.d'"):
            RequestService.init_session("http//foobar.d")

    def test_init_session_with_success_return_request_session(self):
        session = RequestService.init_session(
            "http://url.com",
            headers={"x-test": "true"},
            auth=("username", "password"),
            cookies="cookies-data",
        )
        assert isinstance(session, RequestSession)
        assert session.base_url == "http://url.com"
        assert session.request.auth == ("username", "password")
        assert session.request.headers == {"x-test": "true"}
        assert session.request.cookies == "cookies-data"

    """
    get
    """

    def test_get_failed_return_response(self):
        actual = RequestService.get("http://httpbin.org/post")
        assert isinstance(actual, RequestResponse)
        assert actual._orig_content
        assert actual._headers
        actual._orig_content = "original models"
        actual._headers = "some headers"
        actual._content = actual._content.upper()
        self.assert_equals_resultset(actual.__dict__)

    @pytest.mark.skip(reason="httpbin not working as expected")
    def test_get_with_redirect_return_response(self):
        actual = RequestService.get(
            "http://httpbin.org/redirect-to?url=%2Ftoto%2Ftiti&status_code=302",
            allow_redirects=False,
        )
        assert isinstance(actual, RequestResponse)
        assert actual.status_code == 302
        assert actual._headers
        assert actual.is_redirect
        actual._headers = "some headers"
        self.assert_equals_resultset(actual.__dict__)

    def test_get_success_return_response(self):
        actual = RequestService.get("http://httpbin.org/get")
        assert isinstance(actual, RequestResponse)
        assert actual._orig_content
        assert actual._headers
        actual._orig_content = "original datas"
        actual._headers = "some headers"
        actual = actual.__dict__
        actual = self.fix_response_variable_content(actual)
        self.assert_equals_resultset(actual)

    def test_get_with_parameters_return_response(self):
        actual = RequestService.get(
            "http://httpbin.org/get", params={"p1": "valueA", "p2": "valueB"}
        )
        assert isinstance(actual, RequestResponse)
        assert actual._orig_content
        assert actual._headers
        actual._orig_content = "original datas"
        actual._headers = "some headers"
        actual = actual.__dict__
        actual = self.fix_response_variable_content(actual)
        self.assert_equals_resultset(actual)

    def test_get_with_timeout_return_503(self):
        actual = RequestService.get("http://httpbin.org/delay/3", timeout=0.001)
        assert isinstance(actual, RequestResponse)
        self.assert_equals_resultset(actual.__dict__)

    def test_get_with_session_and_auth_success_return_response(self):
        session = RequestService.init_session(
            "http://httpbin.org/", auth=("anUser", "aPassword")
        )
        actual = RequestService.get("/basic-auth/anUser/aPassword", session)
        assert isinstance(actual, RequestResponse)
        assert actual._orig_content
        assert actual._headers
        actual._headers = "some headers"
        actual._orig_content = "original datas"
        self.assert_equals_resultset(actual.__dict__)

    def test_get_with_session_and_timeout_return_503(self):
        session = RequestService.init_session("http://httpbin.org/", timeout=0.001)
        actual = RequestService.get("/delay/3", session)
        assert isinstance(actual, RequestResponse)
        self.assert_equals_resultset(actual.__dict__)

    def test_get_with_pdf_io_return_response(self):
        """Ensure we can get pdf"""
        actual = RequestService.get(
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        )
        assert isinstance(actual, RequestResponse)
        assert actual

    """
    post
    """

    def test_post_failed_return_405(self):
        actual = RequestService.post(
            "http://httpbin.org/get", {"d1": "valueA", "d2": "valueB"}
        )
        assert isinstance(actual, RequestResponse)
        assert actual._orig_content
        assert actual._headers
        actual._orig_content = "original datas"
        actual._headers = "some headers"
        actual._content = actual._content.upper()
        self.assert_equals_resultset(actual.__dict__)

    def test_post_success_return_response(self):
        actual = RequestService.post(
            "http://httpbin.org/post", {"d1": "valueA", "d2": "valueB"}
        )
        assert isinstance(actual, RequestResponse)
        assert actual._orig_content
        assert actual._headers
        actual._orig_content = "original datas"
        actual._headers = "some headers"
        actual = actual.__dict__
        actual = self.fix_response_variable_content(actual)
        self.assert_equals_resultset(actual)

    def test_post_with_timeout_return_503(self):
        actual = RequestService.post(
            "http://10.255.255.1/timeout",
            {"d1": "valueA", "d2": "valueB"},
            timeout=0.001,
        )
        assert isinstance(actual, RequestResponse)
        self.assert_equals_resultset(actual.__dict__)

    def test_post_with_session_success_return_response(self):
        session = RequestService.init_session("http://httpbin.org/")
        actual = RequestService.post(
            "/post", data={"d1": "valueA", "d2": "valueB"}, session=session
        )
        assert isinstance(actual, RequestResponse)
        assert actual._orig_content
        assert actual._headers
        actual._orig_content = "original datas"
        actual._headers = "some headers"
        actual = actual.__dict__
        actual = self.fix_response_variable_content(actual)
        self.assert_equals_resultset(actual)

    """
    patch
    """
    # as code is shared with post, we can only test success
    def test_patch_with_success_return_response(self):
        actual = RequestService.patch(
            "http://httpbin.org/patch", {"d1": "valueA", "d2": "valueB"}
        )
        assert actual.success is True

    """
    put
    """

    # as code is shared with post, we can only test success
    def test_put_with_success_return_response(self):
        actual = RequestService.put(
            "http://httpbin.org/put", {"d1": "valueA", "d2": "valueB"}
        )
        assert actual.success is True

    """
    delete
    """

    # as code is shared with post, we can only test success
    def test_delete_with_success_return_response(self):
        actual = RequestService.delete(
            "http://httpbin.org/delete", {"d1": "valueA", "d2": "valueB"}
        )
        assert actual.success is True

    def test_delete_with_no_data_return_response(self):
        actual = RequestService.delete("http://httpbin.org/delete")
        assert actual.success is True
