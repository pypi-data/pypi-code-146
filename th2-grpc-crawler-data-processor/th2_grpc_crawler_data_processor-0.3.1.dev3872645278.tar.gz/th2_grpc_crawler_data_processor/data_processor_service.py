from . import crawler_data_processor_pb2_grpc as importStub

class DataProcessorService(object):

    def __init__(self, router):
        self.connector = router.get_connection(DataProcessorService, importStub.DataProcessorStub)

    def CrawlerConnect(self, request, timeout=None):
        return self.connector.create_request('CrawlerConnect', request, timeout)

    def IntervalStart(self, request, timeout=None):
        return self.connector.create_request('IntervalStart', request, timeout)

    def SendEvent(self, request, timeout=None):
        return self.connector.create_request('SendEvent', request, timeout)

    def SendMessage(self, request, timeout=None):
        return self.connector.create_request('SendMessage', request, timeout)