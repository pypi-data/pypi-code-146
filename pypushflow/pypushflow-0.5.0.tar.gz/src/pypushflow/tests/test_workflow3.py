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


class Submodel1(Submodel):
    """
    Submodel containing one python actor.
    """

    def __init__(self, parent, name, thread_counter):
        super().__init__(parent=parent, name=name, thread_counter=thread_counter)
        self.pythonActor = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorTest.py",
            name="Python Actor Test",
            thread_counter=thread_counter,
        )
        self.getPort("In").connect(self.pythonActor)
        self.pythonActor.connect(self.getPort("Out"))


class Workflow3(Workflow):
    """
    Workflow containing one start actor,
    one submodel and one stop actor.
    """

    def __init__(self, name):
        super().__init__(name)
        ctr = ThreadCounter(parent=self)
        self.startActor = StartActor(parent=self, thread_counter=ctr)
        self.submodel1 = Submodel1(parent=self, name="Submodel 1", thread_counter=ctr)
        self.stopActor = StopActor(parent=self, thread_counter=ctr)
        self.startActor.connect(self.submodel1.getPort("In"))
        self.submodel1.getPort("Out").connect(self.stopActor)


class TestWorkflow3(WorkflowTestCase):
    def test_workflow3(self):
        testWorkflow3 = Workflow3("Test workflow 3")
        inData = {"name": "Cat"}
        outData = testWorkflow3.run(
            inData, timeout=15, scaling_workers=False, max_workers=-1
        )
        self.assertIsNotNone(outData)
        self.assertEqual(outData["reply"], "Hello Cat!")
