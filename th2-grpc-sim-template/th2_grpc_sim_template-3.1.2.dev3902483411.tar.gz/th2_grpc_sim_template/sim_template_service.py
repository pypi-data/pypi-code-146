from . import sim_template_pb2_grpc as importStub

class SimTemplateService(object):

    def __init__(self, router):
        self.connector = router.get_connection(SimTemplateService, importStub.SimTemplateStub)

    def createRuleFixSecurity(self, request, timeout=None):
        return self.connector.create_request('createRuleFixSecurity', request, timeout)

    def createDemoRule(self, request, timeout=None):
        return self.connector.create_request('createDemoRule', request, timeout)

    def createRuleFix(self, request, timeout=None):
        return self.connector.create_request('createRuleFix', request, timeout)