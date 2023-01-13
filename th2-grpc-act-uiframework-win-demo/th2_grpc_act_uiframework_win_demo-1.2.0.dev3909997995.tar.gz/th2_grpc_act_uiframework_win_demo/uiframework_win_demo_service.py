from . import uiframework_win_demo_pb2_grpc as importStub

class UIFrameworkActService(object):

    def __init__(self, router):
        self.connector = router.get_connection(UIFrameworkActService, importStub.UIFrameworkActStub)

    def register(self, request, timeout=None):
        return self.connector.create_request('register', request, timeout)

    def unregister(self, request, timeout=None):
        return self.connector.create_request('unregister', request, timeout)

    def openApplication(self, request, timeout=None):
        return self.connector.create_request('openApplication', request, timeout)

    def closeApplication(self, request, timeout=None):
        return self.connector.create_request('closeApplication', request, timeout)

    def initConnection(self, request, timeout=None):
        return self.connector.create_request('initConnection', request, timeout)

    def closeConnection(self, request, timeout=None):
        return self.connector.create_request('closeConnection', request, timeout)

    def sendNewOrderSingle(self, request, timeout=None):
        return self.connector.create_request('sendNewOrderSingle', request, timeout)

    def extractLastOrderDetails(self, request, timeout=None):
        return self.connector.create_request('extractLastOrderDetails', request, timeout)

    def extractLastSystemMessage(self, request, timeout=None):
        return self.connector.create_request('extractLastSystemMessage', request, timeout)
