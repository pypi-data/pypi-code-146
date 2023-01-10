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


class Submodel6(Submodel):
    """
    Submodel containing one python actor which has a long execution time
    """

    def __init__(self, parent, name, thread_counter):
        super().__init__(parent=parent, name=name, thread_counter=thread_counter)
        self.pythonActorAdd = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorAdd.py",
            name="Python Submodel Actor Add",
            errorHandler=self,
            thread_counter=thread_counter,
        )
        self.getPort("In").connect(self.pythonActorAdd)
        self.pythonActorAdd.connect(self.getPort("Out"))


class Workflow6(Workflow):
    """
    Workflow containing one start actor,
    one submodel which has a long execution and one stop actor with short timeout.
    """

    def __init__(self, name):
        super().__init__(name)
        ctr = ThreadCounter(parent=self)
        self.startActor = StartActor(self, thread_counter=ctr)
        self.pythonActorAdd1 = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorAdd.py",
            name="Python Add Actor 1",
            thread_counter=ctr,
        )
        self.pythonActorAdd2 = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorAdd.py",
            name="Python Add Actor 2",
            thread_counter=ctr,
        )
        self.submodel6 = Submodel6(self, name="Submodel 6", thread_counter=ctr)
        self.stopActor = StopActor(self, thread_counter=ctr)
        self.startActor.connect(self.pythonActorAdd1)
        self.pythonActorAdd1.connect(self.submodel6.getPort("In"))
        self.submodel6.getPort("Out").connect(self.pythonActorAdd2)
        self.pythonActorAdd2.connect(self.stopActor)


class TestWorkflow6(WorkflowTestCase):
    def test_workflow6(self):
        workflow6 = Workflow6("Test workflow 6")
        inData = {"value": 1}
        outData = workflow6.run(
            inData, timeout=5, scaling_workers=False, max_workers=-1
        )
        self.assertEqual(outData["value"], 4)
