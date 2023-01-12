from . import Bar_pb2_grpc as importStub

class BarServiceService(object):

    def __init__(self, router):
        self.connector = router.get_connection(BarServiceService, importStub.BarServiceStub)

    def BarRequest(self, request, timeout=None):
        return self.connector.create_request('BarRequest', request, timeout)

    def EmptyRequest(self, request, timeout=None):
        return self.connector.create_request('EmptyRequest', request, timeout)