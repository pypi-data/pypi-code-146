import pytest
from django.conf import settings
from django.test.utils import override_settings
from rest_framework.exceptions import AuthenticationFailed

from w.exceptions import InvalidCredentialsError
from w.services.technical.models.sso import SsoValidToken
from w.services.technical.sso_service import SsoService
from w.tests.helpers import sso_test_helper
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestSsoService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.user_data = {
            "email": "user@email.com",
            "username": "user@email.com",
            "first_name": "user-firstname",
            "last_name": "user-lastname",
            "password": "user-pwd",
            "client_roles": {"app1": ["role_app1"]},
        }

    def setup_method(self):
        SsoService.clear()
        SsoService.init()
        with sso_test_helper.mock_keycloak_admin_init() as m:
            SsoService._init_keycloak_admin()
        self.keycloak_admin = m

    """
    is_token_valid
    """

    def test_token_is_valid_with_not_initialize_service_raise_runtime_error(self):
        """Ensure method raise RuntimeError if service is not initialized"""
        SsoService.clear()
        match = "Service SsoService must be initialized first"
        with pytest.raises(RuntimeError, match=match):
            SsoService.is_token_valid("need-to-be-initialized")

    def test_token_is_valid_with_invalid_token_raise_error(self):
        """Ensure method raise AuthenticationFailed if token is invalid"""
        match = "Invalid or expired token."
        with sso_test_helper.valid_token_failure():
            with pytest.raises(AuthenticationFailed, match=match):
                SsoService.is_token_valid("invalid-token")

    def test_token_is_valid_with_success_return_sso_token(self):
        """Ensure method succeed"""
        self.keycloak_admin.get_clients.return_value = self.get_dataset(
            "sso/get_clients_success.json"
        )
        self.keycloak_admin.get_client_roles_of_user.return_value = self.get_dataset(
            "sso/get_client_roles.json"
        )
        with sso_test_helper.mock_keycloak_initialize_admin(), sso_test_helper.sso_introspect_success() as m:  # noqa
            actual = SsoService.is_token_valid("valid-token")
        assert isinstance(actual, SsoValidToken)
        self.assert_equals_resultset(
            {"actual": actual.to_dict(), "mock_calls": self.get_mock_calls(m)}
        )

    """
    list_user_roles
    """

    def test_list_user_roles_with_not_initialize_service_raise_runtime_error(self):
        """Ensure method raise RuntimeError if service is not initialized"""
        SsoService.clear()
        match = "Service SsoService must be initialized first"
        with pytest.raises(RuntimeError, match=match):
            SsoService.list_user_roles("ee2fa73a-2a46-41e9-a844-5f9a5cff742a")

    def test_list_user_roles_with_missing_admin_raise_error(self):
        """Ensure method raise RuntimeError if not initialized"""
        SsoService.clear()
        sso_settings = {**settings.SSO}
        sso_settings.pop("ADMIN_PASSWORD")
        SsoService.init()

        match = "Missing SSO settings ADMIN_LOGIN or ADMIN_PASSWORD"
        with override_settings(SSO=sso_settings):
            with pytest.raises(RuntimeError, match=match):
                SsoService.list_user_roles("ee2fa73a-2a46-41e9-a844-5f9a5cff742a")

    def test_list_user_roles_with_success_return_dict(self):
        """Ensure method succeeds"""
        self.keycloak_admin.get_clients.return_value = self.get_dataset(
            "sso/get_clients_success.json"
        )
        self.keycloak_admin.get_client_roles_of_user.return_value = self.get_dataset(
            "sso/get_client_roles.json"
        )
        with sso_test_helper.mock_keycloak_initialize_admin():
            actual = SsoService.list_user_roles("ee2fa73a-2a46-41e9-a844-5f9a5cff742a")
        self.assert_equals_resultset(
            {"actual": actual, "mocks": self.get_mock_calls(self.keycloak_admin)}
        )

    """
    get_clients
    """

    def test_get_clients_with_not_init_service_raise_error(self):
        """Ensure method raise RuntimeError if not initialized"""
        SsoService.clear()
        match = "Service SsoService must be initialized first"
        with pytest.raises(RuntimeError, match=match):
            SsoService.get_clients()

    def test_get_clients_with_missing_admin_raise_error(self):
        """Ensure method raise RuntimeError if not initialized"""
        SsoService.clear()
        sso_settings = {**settings.SSO}
        sso_settings.pop("ADMIN_PASSWORD")
        SsoService.init()

        match = "Missing SSO settings ADMIN_LOGIN or ADMIN_PASSWORD"
        with override_settings(SSO=sso_settings):
            with pytest.raises(RuntimeError, match=match):
                SsoService.get_clients()

    def test_get_clients_with_success_return_dict(self):
        """Ensure method succeeds"""
        self.keycloak_admin.get_clients.return_value = self.get_dataset(
            "sso/get_clients_success.json"
        )
        with sso_test_helper.mock_keycloak_initialize_admin():
            actual = SsoService.get_clients()
        self.assert_equals_resultset(actual)

    """
    get_client_roles
    """

    def test_get_client_roles_with_success_return_dict(self):
        """Ensure method succeed"""
        self.keycloak_admin.get_client_roles.return_value = self.get_dataset(
            "sso/get_client_roles.json"
        )
        with sso_test_helper.mock_keycloak_initialize_admin():
            actual = SsoService.get_client_roles("client-id")
        self.assert_equals_resultset(
            {"actual": actual, "mocks": self.get_mock_calls(self.keycloak_admin)}
        )

    """
    get_or_create_user
    """

    def test_get_or_create_user_with_unknown_user_return_user(self):
        """Ensure method create user in sso server if not exist"""
        self.keycloak_admin.get_user_id.return_value = None
        self.keycloak_admin.create_user.return_value = "user-id"
        self.keycloak_admin.get_clients.return_value = self.get_dataset(
            "sso/get_clients_success.json"
        )
        self.keycloak_admin.get_client_roles.return_value = self.get_dataset(
            "sso/get_client_roles.json"
        )
        self.keycloak_admin.assign_client_role.return_value = None
        self.keycloak_admin.get_user.return_value = self.get_dataset(
            "sso/get_user_success.json"
        )
        with sso_test_helper.mock_keycloak_initialize_admin():
            sso_user, created = SsoService.get_or_create_user(self.user_data)
        assert created is True
        self.assert_equals_resultset(
            {"actual": sso_user, "mocks": self.get_mock_calls(self.keycloak_admin)}
        )
        self.save_as_dataset(
            "sso_service/get_or_create_user_with_unknown_user_return_user.json",
            sso_user,
        )

    def test_get_or_create_user_with_known_user_return_user(self):
        """Ensure method only retrieve user in sso server if exist"""
        self.keycloak_admin.get_user_id.return_value = "user-id"
        self.keycloak_admin.get_user.return_value = self.get_dataset(
            "sso/get_user_success.json"
        )
        with sso_test_helper.mock_keycloak_initialize_admin():
            sso_user, created = SsoService.get_or_create_user(self.user_data)
        assert created is False
        self.assert_equals_resultset(
            {"actual": sso_user, "mocks": self.get_mock_calls(self.keycloak_admin)}
        )

    """
    require_update_password
    """

    def test_require_update_password_with_known_user_return_none(self):
        """Ensure method returns None if user exists"""
        self.keycloak_admin.send_update_account.return_value = None
        with sso_test_helper.mock_keycloak_initialize_admin():
            actual = SsoService.require_update_password(
                self.user_data["username"], client_id="my_client"
            )
        self.assert_equals_resultset(
            {"actual": actual, "mocks": self.get_mock_calls(self.keycloak_admin)}
        )

    """
    check_user_credentials
    """

    def test_check_user_credentials_with_invalid_credentials_raise_invalid_credentials_error(  # noqa
        self,
    ):
        """Ensure method raise InvalidCredentialsError if credentials is invalid"""
        match = "401 - Invalid Credentials"
        with sso_test_helper.mock_invalid_user_token():
            with pytest.raises(InvalidCredentialsError, match=match):
                SsoService.check_user_credentials(
                    self.user_data["username"], self.user_data["password"]
                )

    def test_check_user_credentials_with_valid_credentials_return_access_token(  # noqa
        self,
    ):
        """Ensure method return access token if credentials is valid"""
        with sso_test_helper.mock_valid_user_token() as m:
            actual = SsoService.check_user_credentials(
                self.user_data["username"], self.user_data["password"]
            )
        self.assert_equals_resultset(
            {"actual": actual, "mocks": self.get_mock_calls(m)}
        )
