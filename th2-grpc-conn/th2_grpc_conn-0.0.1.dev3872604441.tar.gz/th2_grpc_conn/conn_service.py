from . import conn_pb2_grpc as importStub

class ConnService(object):

    def __init__(self, router):
        self.connector = router.get_connection(ConnService, importStub.ConnStub)

    def start(self, request, timeout=None):
        return self.connector.create_request('start', request, timeout)

    def stop(self, request, timeout=None):
        return self.connector.create_request('stop', request, timeout)