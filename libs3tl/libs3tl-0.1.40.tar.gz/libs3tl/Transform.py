from libs3tl import Step


class Transform(Step.Step):
    def __init__(self):
        self.setStartTime()
        self.step = "Tr"
        self.paramsFile = 'Transform.properties'
        self.logger = 'logTransform'
        self.logFile = self.getRelativeFile('../logs/Transform.log')

    def startup(self):
        super(Transform,self).startup()
        self.startSubscriber()

    def doWorkAndHandoff(self):
        pass

    def doWork(self):
        pass