#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "28/05/2019"

import pprint
from pypushflow.ThreadCountingActor import ThreadCountingActor


class AbstractActor(ThreadCountingActor):
    def __init__(self, parent=None, name=None, **kw):
        super().__init__(name=name, parent=parent, **kw)
        self.listDownStreamActor = []
        self.actorId = None
        self.started = False
        self.finished = False

    def __str__(self) -> str:
        return self.name

    def connect(self, actor):
        self.logger.debug("connect to actor '%s'", actor.name)
        self.listDownStreamActor.append(actor)

    def trigger(self, inData):
        self.logger.info("triggered with inData =\n %s", pprint.pformat(inData))
        self.setStarted()
        self.setFinished()
        for actor in self.listDownStreamActor:
            actor.trigger(inData)

    def uploadInDataToMongo(self, actorData=None, script=None):
        if self.parent is not None:
            name = self.getActorPath() + "/" + self.name
            if actorData:
                info = dict(actorData)
            else:
                info = dict()
            if script:
                info["script"] = script
            self.actorId = self.parent.db_client.startActor(name=name, info=info)

    def uploadOutDataToMongo(self, actorData=None):
        if actorData and self.actorId is not None:
            self.parent.db_client.updateActorInfo(self.actorId, info=actorData)

    def setMongoAttribute(self, attribute, value):
        if self.actorId is not None:
            self.parent.db_client.updateActorInfo(self.actorId, info={attribute: value})

    def getActorPath(self):
        return self.parent.getActorPath()

    def hasStarted(self):
        return self.started

    def setStarted(self):
        self.logger.info("started")
        self.started = True

    def hasFinished(self):
        return self.finished

    def setFinished(self):
        self.logger.info("finished")
        self.finished = True
