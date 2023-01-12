from . import rhbatch_pb2_grpc as importStub

class RhBatchService(object):

    def __init__(self, router):
        self.connector = router.get_connection(RhBatchService, importStub.RhBatchStub)

    def register(self, request, timeout=None, properties=None):
        return self.connector.create_request('register', request, timeout, properties)

    def unregister(self, request, timeout=None, properties=None):
        return self.connector.create_request('unregister', request, timeout, properties)

    def executeRhActionsBatch(self, request, timeout=None, properties=None):
        return self.connector.create_request('executeRhActionsBatch', request, timeout, properties)