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
__date__ = "03/05/2021"

from pypushflow.Workflow import Workflow
from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
from pypushflow.RouterActor import RouterActor
from pypushflow.ThreadCounter import ThreadCounter
from pypushflow.tests.workflowTestCase import WorkflowTestCase


class Workflow10(Workflow):
    def __init__(self, name):
        super().__init__(name)
        ctr = ThreadCounter(parent=self)
        self.startActor = StartActor(self, thread_counter=ctr)
        self.pythonActorAddWithoutSleep = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorAddWithoutSleep.py",
            name="Add without sleep",
            thread_counter=ctr,
        )
        self.pythonActorCheck = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorCheck.py",
            name="Check",
            thread_counter=ctr,
        )
        self.check = RouterActor(
            parent=self,
            name="Check",
            itemName="doContinue",
            listPort=["true", "false"],
            thread_counter=ctr,
        )
        self.stopActor = StopActor(self, thread_counter=ctr)
        self.startActor.connect(self.pythonActorAddWithoutSleep)
        self.pythonActorAddWithoutSleep.connect(self.pythonActorCheck)
        self.pythonActorCheck.connect(self.check)
        self.check.connect(self.pythonActorAddWithoutSleep, expectedValue="true")
        self.check.connect(self.stopActor, expectedValue="false")


class TestWorkflow10(WorkflowTestCase):
    def test_workflow10(self):
        limit = 10
        workflow10 = Workflow10(f"Test workflow {limit}")
        inData = {"value": 1, "limit": limit}
        outData = workflow10.run(
            inData, timeout=1200, scaling_workers=False, max_workers=-1
        )
        self.assertEqual(outData["value"], limit)
