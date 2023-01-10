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
from pypushflow.Submodel import Submodel
from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
from pypushflow.ThreadCounter import ThreadCounter
from pypushflow.tests.workflowTestCase import WorkflowTestCase


class Submodel4(Submodel):
    """
    Submodel containing one python actor which throws an exception.
    """

    def __init__(self, parent, name, thread_counter):
        super().__init__(parent=parent, name=name, thread_counter=thread_counter)
        self.pythonActor = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonErrorHandlerTest.py",
            name="Python Error Handler Test",
            errorHandler=self,
            thread_counter=thread_counter,
        )
        self.getPort("In").connect(self.pythonActor)
        self.pythonActor.connect(self.getPort("Out"))


class Workflow4(Workflow):
    """
    Workflow containing one start actor,
    one submodel which throws an exception and one stop actor.
    """

    def __init__(self, name):
        super().__init__(name)
        ctr = ThreadCounter(parent=self)
        self.startActor = StartActor(thread_counter=ctr)
        self.submodel4 = Submodel4(parent=self, name="Submodel 4", thread_counter=ctr)
        self.stopActor = StopActor(thread_counter=ctr)
        self.startActor.connect(self.submodel4.getPort("In"))
        self.submodel4.getPort("Out").connect(self.stopActor)
        self.connectOnError(self.stopActor)


class TestWorkflow4(WorkflowTestCase):
    def test_workflow4(self):
        workflow4 = Workflow4("Test workflow 4")
        inData = {"name": "Dog"}
        outData = workflow4.run(
            inData, timeout=5, scaling_workers=False, max_workers=-1
        )
        self.assertIsNotNone(outData)
        self.assertTrue("WorkflowException" in outData)
