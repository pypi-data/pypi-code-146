import factory

from rhino_health.lib.constants import ApiEnvironment
from rhino_health.lib.rhino_client import SDKVersion
from rhino_health.lib.rhino_session import RhinoSession


class MockRhinoSession(RhinoSession):
    def login(self, *args, **kwargs):
        pass

    def _original_login(self, *args, **kwargs):
        super(MockRhinoSession, self).login(*args, **kwargs)


class RhinoSessionFactory(factory.Factory):
    class Meta:
        model = MockRhinoSession
        strategy = factory.BUILD_STRATEGY

    authentication_details = factory.Dict(
        {"username": factory.Faker("ascii_email"), "password": factory.Faker("uuid4")}
    )
    otp_code = None
    rhino_api_url = ApiEnvironment.LOCALHOST_API_URL
    sdk_version = SDKVersion.PREVIEW
    show_traceback = True

    @factory.post_generation
    def login_if_required(self, create, extracted, **kwargs):
        if create:
            # TODO: Unused, test this
            self._original_login()
