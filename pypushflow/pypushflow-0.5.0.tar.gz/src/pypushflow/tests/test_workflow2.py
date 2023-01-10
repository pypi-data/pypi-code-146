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
__date__ = "07/04/2021"

from pypushflow.Workflow import Workflow
from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
from pypushflow.ThreadCounter import ThreadCounter
from pypushflow.tests.workflowTestCase import WorkflowTestCase


class Workflow2(Workflow):
    """
    Workflow with error handling, containing one start actor,
    one python actor and one stop actor.

    The python actor throws an exception.
    """

    def __init__(self, name):
        super().__init__(name)
        ctr = ThreadCounter(parent=self)
        self.startActor = StartActor(parent=self, thread_counter=ctr)
        self.pythonActor = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonErrorHandlerTest.py",
            name="Python Error Handler Test",
            errorHandler=self,
            thread_counter=ctr,
        )
        self.stopActor = StopActor(parent=self, thread_counter=ctr)
        self.startActor.connect(self.pythonActor)
        self.pythonActor.connect(self.stopActor)
        self.connectOnError(self.stopActor)


class TestWorkflow2(WorkflowTestCase):
    def test_Workflow2(self):
        testWorkflow2 = Workflow2("Test workflow 2")
        inData = {"name": "Tom"}
        outData = testWorkflow2.run(inData, timeout=5, scaling_workers=False)
        self.assertIsNotNone(outData)
        self.assertTrue("WorkflowException" in outData)
