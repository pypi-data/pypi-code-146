import grpc

from truera.authn.usercontext import _KEY_TRUERA_TENANT_ID
from truera.authn.usercontext import _KEY_TRUERA_USER_ID
from truera.authn.usercontext import _KEY_TRUERA_USER_NAME


# raised if the context mock didn't get the expected exception
class GrpcContextMockExceptionBad(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# raised if the context mock did get the expected exception
class GrpcContextMockExceptionGood(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GrpcContextMock():

    def __init__(
        self,
        expectedAbortMessage: str = None,
        expectedGrpcStatus: grpc.StatusCode = grpc.StatusCode.OK
    ):
        self.expectedAbortMessage = expectedAbortMessage
        self.expectedGrpcStatus = expectedGrpcStatus
        self.was_hit = False

    def abort(self, code, message):
        if not self.expectedAbortMessage:
            raise GrpcContextMockExceptionBad(message)

        assert self.expectedGrpcStatus == code
        assert message == self.expectedAbortMessage
        self.was_hit = True

        # Used so we can stop execution and distinguish between good and bad cases.
        raise GrpcContextMockExceptionGood()

    def invocation_metadata(self):
        from collections import namedtuple
        metadatum = namedtuple("metadatum", "key value")
        userid = metadatum(_KEY_TRUERA_USER_ID, "FakeHeaderUserIdValue")
        username = metadatum(_KEY_TRUERA_USER_NAME, "FakeHeaderUserNameValue")
        tenantid = metadatum(_KEY_TRUERA_TENANT_ID, "FakeHeaderTenantIdValue")
        return [userid, username, tenantid]
