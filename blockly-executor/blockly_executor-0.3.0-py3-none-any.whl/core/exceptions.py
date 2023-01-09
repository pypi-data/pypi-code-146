class LimitCommand(Exception):
    pass


class WorkspaceNotFound(Exception):
    pass


class DeferredOperation(Exception):
    # def __init__(self, name, params, uuid, context):
    #     super(DeferredOperation, self).__init__(name)
    #     self.name =
    def get_context(self):
        return self.args[2]

    def to_command(self):
        return [{
            'method': self.args[0],
            'params': self.args[1],
            'uuid': self.args[2]['__deferred']
        }]


class StepForward(Exception):
    pass

    def get_context(self):
        return self.args[2].to_dict()

    def to_command(self):
        return [self.args[0], self.args[1]]


class ReturnFromFunction(Exception):
    pass
