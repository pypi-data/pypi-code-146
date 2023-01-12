from . import Foo_pb2_grpc as importStub

class FooServiceService(object):

    def __init__(self, router):
        self.connector = router.get_connection(FooServiceService, importStub.FooServiceStub)

    def FooRequest(self, request, timeout=None):
        return self.connector.create_request('FooRequest', request, timeout)