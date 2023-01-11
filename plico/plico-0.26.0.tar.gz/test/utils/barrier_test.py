#!/usr/bin/env python

import unittest
from plico.utils.barrier import Predicate, Barrier, BarrierTimeout,\
    FunctionPredicate
from plico.utils.decorator import override


__version__="$Id: barrier_test.py 26 2018-01-26 19:06:25Z lbusoni $"


class Dummy:

    def __init__(self):
        self._isTrueInvocations= 0


    def isTrue(self):
        if self._isTrueInvocations < 3:
            self._isTrueInvocations+= 1
            return False
        return True


    def getIsTrueInvocations(self):
        return self._isTrueInvocations


class MyTimeModule():
    def __init__(self):
        self._count= 0
        self._returnValues= None

    def setReturnValues(self, returnValues):
        self._returneValues= returnValues
        self._count= 0

    def time(self):
        ret= self._returnValues[self._count]
        self._count+= 1
        return ret


class MyPredicate(Predicate):

    def __init__(self):
        self._errorMessage= None
        self._isFullfilledValues= [False]
        self._count= 0

    def setErrorMessage(self, msg):
        self._errorMessage= msg

    @override
    def errorMessage(self):
        return self._errorMessage

    def setFullfilledValues(self, fullfilledValues):
        self._isFullfilledValues= fullfilledValues
        self._count= 0

    @override
    def isFullfilled(self):
        nElements= len(self._isFullfilledValues)
        ret= self._isFullfilledValues[self._count % nElements]
        self._count+= 1
        return ret



class BarrierStaticMethodTest(unittest.TestCase):

    def trueFunction(self):
        return True


    def falseFunction(self):
        return False


    def test_should_return_True(self):
        Barrier.waitUntil(self.trueFunction, 0.5, 0.15)


    def test_should_raise_timeout_exception(self):
        TIMEOUT_IN_SEC= 0.5
        timeModule= MyTimeModule()
        timeModule.setReturnValues([0, TIMEOUT_IN_SEC])
        self.assertRaises(Exception, Barrier.waitUntil,
                          self.falseFunction,
                          TIMEOUT_IN_SEC, 0.15, timeModule)


    def test_invocations(self):
        dummy= Dummy()

        Barrier.waitUntil(dummy.isTrue, 2, 0.01)
        self.assertTrue(dummy.getIsTrueInvocations() == 3)



class BarrierDynamicMethodTest(unittest.TestCase):

    def setUp(self):
        class TimeFakeModule(object):

            def __init__(self):
                self._currentTime= 0


            def time(self):
                self._currentTime+= 0.1
                return self._currentTime


            def sleep(self, sleepDurationInSec):
                pass

        self.predicate= MyPredicate()
        self.predicate.setErrorMessage("predicate failure")

        self.barrier= Barrier(
            timeoutSec=3, pollingPeriodSec=0.1,
            timeModule=TimeFakeModule())


    def test_should_wait_for_predicate(self):
        self.predicate= MyPredicate()
        self.predicate.setFullfilledValues([False, True])
        self.barrier.waitFor(self.predicate)


    def test_should_detect_timeout(self):
        self.predicate= MyPredicate()
        self.predicate.setFullfilledValues([False])
        self.predicate.setErrorMessage("Tux failure")

        exceptionThrown= False
        try:
            self.barrier.waitFor(self.predicate)
        except BarrierTimeout as e:
            exceptionThrown= True
            self.assertTrue("Tux failure" in str(e))
        self.assertTrue(exceptionThrown)


    def test_should_forward_predicate_failures(self):
        class FailingPredicate(Predicate):

            @override
            def isFullfilled(self):
                raise Exception("test")


            @override
            def errorMessage(self):
                assert False

        try:
            self.barrier.waitFor(FailingPredicate())
        except BarrierTimeout:
            self.fail("No barrier timeout expected")
        except Exception as e:
            self.assertEqual("test", str(e))
            return

        self.fail("Exception expected")


class FunctionPredicateTest(unittest.TestCase):


    def test_creation(self):
        def foo(a, b):
            return a == b
        pred= FunctionPredicate.create(foo, 3, 4)
        self.assertFalse(pred.isFullfilled())

        pred= FunctionPredicate.create(foo, 1, 1)
        self.assertTrue(pred.isFullfilled())

        print("pred:", pred.errorMessage())
        self.assertTrue("foo" in pred.errorMessage())


if __name__ == "__main__":
    unittest.main()
