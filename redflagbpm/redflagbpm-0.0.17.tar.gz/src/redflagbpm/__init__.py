from redflagbpm.BPMService import BPMService
from redflagbpm.Services import Service, DocumentService, Context, ResourceService, ExecutionService, RuntimeService


def setupServices(self: BPMService):
    self.service = Service(self)
    self.context = Context(self)
    self.execution = ExecutionService(self)
    self.documentService = DocumentService(self)
    self.resourceService = ResourceService(self)
    self.runtimeService = RuntimeService(self)


BPMService.setupServices = setupServices
