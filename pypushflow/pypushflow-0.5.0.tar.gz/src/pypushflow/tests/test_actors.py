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

import unittest

from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
from pypushflow.ErrorHandler import ErrorHandler
from pypushflow.ForkActor import ForkActor
from pypushflow.JoinActor import JoinActor
from pypushflow.RouterActor import RouterActor
from pypushflow.ThreadCounter import ThreadCounter


class TestPythonActor(unittest.TestCase):
    def setUp(self):
        self.thread_counter = ThreadCounter()

    def test_PythonActor(self):
        script = "pypushflow.tests.tasks.pythonActorTest.py"
        name = "Python Actor Test"
        actor = PythonActor(
            script=script, name=name, thread_counter=self.thread_counter
        )
        stopActor = StopActor(thread_counter=self.thread_counter)
        inData = {"name": "Ragnar"}
        actor.connect(stopActor)
        actor.trigger(inData)
        stopActor.join(timeout=10)
        outData = stopActor.outData
        self.assertIsNotNone(outData)
        self.assertEqual(outData["reply"], "Hello Ragnar!")

    def test_PythonActorWithPositionalArguments(self):
        script = "pypushflow.tests.tasks.pythonActorTest.py"
        name = "Python Actor Test"
        actor = PythonActor(
            script=script, name=name, thread_counter=self.thread_counter
        )
        stopActor = StopActor(thread_counter=self.thread_counter)
        inData = {0: "Ragnar"}
        actor.connect(stopActor)
        actor.trigger(inData)
        stopActor.join(timeout=10)
        outData = stopActor.outData
        self.assertIsNotNone(outData)
        self.assertEqual(outData["reply"], "Hello Ragnar!")

    def test_ErrorHandler(self):
        return
        script = "pypushflow.tests.tasks.pythonErrorHandlerTest.py"
        name = "Python Error Handler Test"
        actor = PythonActor(
            script=script, name=name, thread_counter=self.thread_counter
        )
        stopActor = StopActor(thread_counter=self.thread_counter)
        errorHandler = ErrorHandler(
            name="Error handler", thread_counter=self.thread_counter
        )
        inData = {"name": "Ragnar"}
        actor.connect(stopActor)
        actor.connectOnError(errorHandler)
        errorHandler.connect(stopActor)
        actor.trigger(inData)
        stopActor.join(timeout=5)
        outData = stopActor.outData
        self.assertIsNotNone(outData)
        self.assertTrue("WorkflowException" in outData)

    def test_ForkAndJoinActors(self):
        start = StartActor(thread_counter=self.thread_counter)
        stop = StopActor(thread_counter=self.thread_counter)
        fork = ForkActor(thread_counter=self.thread_counter)
        joinActor = JoinActor(thread_counter=self.thread_counter)
        pythonActor1 = PythonActor(
            script="pypushflow.tests.tasks.pythonActor1.py",
            thread_counter=self.thread_counter,
        )
        pythonActor2 = PythonActor(
            script="pypushflow.tests.tasks.pythonActor2.py",
            thread_counter=self.thread_counter,
        )
        # Connections
        start.connect(fork)
        fork.connect(pythonActor1)
        fork.connect(pythonActor2)
        pythonActor1.connect(joinActor)
        joinActor.increaseNumberOfThreads()
        pythonActor2.connect(joinActor)
        joinActor.increaseNumberOfThreads()
        joinActor.connect(stop)
        # Run
        inData = {"a": 1}
        start.trigger(inData)
        stop.join(timeout=5)
        outData = stop.outData
        self.assertIsNotNone(outData)

    def test_RouterActor(self):
        start = StartActor(thread_counter=self.thread_counter)
        stop = StopActor(thread_counter=self.thread_counter)
        router = RouterActor(
            parent=None,
            itemName="a",
            listPort=["other", "null"],
            thread_counter=self.thread_counter,
        )
        pythonActor1 = PythonActor(
            script="pypushflow.tests.tasks.pythonActor1.py",
            thread_counter=self.thread_counter,
        )
        pythonActor2 = PythonActor(
            script="pypushflow.tests.tasks.pythonActor2.py",
            thread_counter=self.thread_counter,
        )
        # Connections
        start.connect(router)
        router.connect(pythonActor1, "other")
        router.connect(pythonActor2, "null")
        pythonActor1.connect(stop)
        pythonActor2.connect(stop)
        # Run
        inData = {"a": 1}
        start.trigger(inData)
        stop.join(timeout=5)
        outData = stop.outData
        self.assertIsNotNone(outData)
        self.assertTrue(outData["actor1"])
        # Run 2
        inData = {"a": None}
        start.trigger(inData)
        stop.join(timeout=5)
        outData = stop.outData
        self.assertIsNotNone(outData)
        self.assertTrue(outData["actor2"])
