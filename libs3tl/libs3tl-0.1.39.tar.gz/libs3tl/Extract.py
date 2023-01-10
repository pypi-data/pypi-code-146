from libs3tl import Step

class Extract(Step.Step):
    def __init__(self):
        self.setStartTime()
        self.step = "Ex"
        self.paramsFile = 'Extract.properties'
        self.logger = 'logExtract'
        self.logFile =self.getRelativeFile('../logs/Extract.log')

    def startup(self):
        super(Extract,self).startup()

    def doWorkAndHandoff(self):
        pass

    def doWork(self):
        pass

    

