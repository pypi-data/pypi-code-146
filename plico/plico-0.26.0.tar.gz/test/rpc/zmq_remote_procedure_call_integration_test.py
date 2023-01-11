#!/usr/bin/env python
import unittest
import time
import io
import os
import logging
import subprocess
from test.test_helper import MessageInFileProbe, Poller, TestHelper
import shutil
import shlex
from plico.utils.logger import Logger
from plico.rpc.zmq_remote_procedure_call import ZmqRemoteProcedureCall,\
    ZmqRpcTimeoutError



class MyException(Exception):
    pass


class HasALogger():
    def __init__(self, value):
        self.logger= Logger.of('HasALogger')
        self.value= value


    def __getstate__(self):
        self.logger= None
        return self.__dict__


    def __setstate__(self, d):
        self.__dict__ = d
        self.logger= Logger.of('HasANewLogger')


class MyObject():

    def __init__(self, value):
        self._value= value


    def getValue(self):
        return self._value


class MyPublisher():
    REPLY_PORT= 4011
    PUBLISHER_PORT= 4012
    RUNNING_MESSAGE= 'imrunning'
    CYCLE_PERIOD= 0.01

    def __init__(self, timeModule=time):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self._zmq= ZmqRemoteProcedureCall()
        self._replySocket= self._zmq.replySocket(self.REPLY_PORT)
        self._publisherSocket= self._zmq.publisherSocket(self.PUBLISHER_PORT)
        self._counter= 0
        self._timeMod= timeModule
        self._isTerminated= False
        self._logger= Logger.of('MyPublisher')
        self.loop()


    def loop(self):
        self._logger.notice("%s" % self.RUNNING_MESSAGE)
        while not self._isTerminated:
            self._logger.notice('looping counter %d' % self._counter)
            self._zmq.handleRequest(self, self._replySocket,
                                    multi=False)
            anObject= MyObject(self._counter)
            self._zmq.publishPickable(self._publisherSocket, anObject)
            self._counter+= 1
            self._timeMod.sleep(self.CYCLE_PERIOD)
        self._logger.notice("Terminating")


    def getLastCounter(self):
        return self._counter


    @staticmethod
    def startUp():
        MyPublisher()


    @staticmethod
    def commandToSpawn():
        cmd= 'python -c "from %s import MyPublisher; '\
             'MyPublisher.startUp()"' % MyServer.__module__
        return cmd



class MyServer():

    SUCCESS= 123
    REPLY_PORT= 4010
    RUNNING_MESSAGE= 'imrunning'
    TIME_TO_EXECUTE= 2

    def __init__(self, timeModule=time):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self._zmq= ZmqRemoteProcedureCall()
        self._replySocket= self._zmq.replySocket(self.REPLY_PORT)
        self._timeMod= timeModule
        self._isTerminated= False
        self._logger= Logger.of('MyServer')
        self.loop()


    def loop(self):
        self._logger.notice("%s" % self.RUNNING_MESSAGE)
        while not self._isTerminated:
            self._logger.notice('looping')
            self._zmq.handleRequest(self, self._replySocket, multi=False)
            self._timeMod.sleep(0.1)
        self._logger.notice("Terminating")


    def returnSuccessAfter2Seconds(self):
        self._logger.notice('invoked returnSuccessAfter2Seconds')
        self._timeMod.sleep(self.TIME_TO_EXECUTE)
        return self.SUCCESS


    def raiseAnException(self):
        self._logger.notice('invoked raiseAnException')
        raise MyException('wanted Exception')


    def getSomethingWithALogger(self, value):
        return HasALogger(value)


    @staticmethod
    def startUpServer():
        MyServer()


    @staticmethod
    def commandToSpawn():
        cmd= 'python -c "from %s import MyServer; '\
             'MyServer.startUpServer()"' % MyServer.__module__
        return cmd


class MyClient():

    def __init__(self):
        self._zmq= ZmqRemoteProcedureCall()
        self._requestSocket= self._zmq.requestSocket(
            'localhost', MyServer.REPLY_PORT)
        self._subscriberSocket= self._zmq.subscriberSocket(
            'localhost', MyPublisher.PUBLISHER_PORT, conflate=True)
        self._requestSocketOnPublisher= self._zmq.requestSocket(
            'localhost', MyPublisher.REPLY_PORT)
        self._logger= Logger.of('MyClient')


    def callASuccessfulMethod(self, timeout):
        return self._zmq.sendRequest(
            self._requestSocket,
            'returnSuccessAfter2Seconds',
            timeout=timeout)


    def callAMethodThatRaisesMyException(self):
        return self._zmq.sendRequest(
            self._requestSocket, 'raiseAnException',
            timeout=2 * MyServer.TIME_TO_EXECUTE)


    def getAnObjectThatHasALogger(self, value):
        return self._zmq.sendRequest(
            self._requestSocket, 'getSomethingWithALogger',
            [value], timeout=1)


    def readFromPublisher(self):
        timeoutInSec= 3.
        obj= self._zmq.receivePickable(self._subscriberSocket,
                                       timeoutInSec)
        self._logger.notice('read %d from publisher' % obj.getValue())
        return obj


    def getLastCounterFromPublisher(self):
        value= self._zmq.sendRequest(
            self._requestSocketOnPublisher, 'getLastCounter',
            [], timeout=1)
        self._logger.notice('asked to publisher and got %d' % value)
        return value


class ZmqRemoteProcedureCallTest(unittest.TestCase):

    THIS_DIR= os.path.abspath(os.path.dirname(__file__))
    TEST_DIR= os.path.join(THIS_DIR, "./tmp/")
    LOG_DIR= os.path.join(TEST_DIR, "log")
    SERVER_LOG_PATH= os.path.join(LOG_DIR, "server.log")
    PUBLISHER_LOG_PATH= os.path.join(LOG_DIR, "publisher.log")



    def setUp(self, timeModule=time):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self._removeTestFolderIfItExists()
        self._makeTestDir()
        self._server= None
        self._publisher= None
        self._client= MyClient()
        self._wasSuccessful= False
        self._timeMod= timeModule


    def _makeTestDir(self):
        os.mkdir(self.TEST_DIR)
        os.mkdir(self.LOG_DIR)


    def _removeTestFolderIfItExists(self):
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)


    def _spawnProcess(self,
                      commandToSpawn,
                      logFilePath,
                      runningMessage):
        processLog= io.open(os.path.join(logFilePath), "w")
        cmd= "%s" % commandToSpawn()
        print(cmd)
        process= subprocess.Popen(
            shlex.split(cmd),
            stdout=processLog, stderr=processLog
        )
        Poller(5).check(MessageInFileProbe(runningMessage,
                                           logFilePath))
        return process


    def _spawnServer(self):
        self._server= self._spawnProcess(MyServer.commandToSpawn,
                                         self.SERVER_LOG_PATH,
                                         MyServer.RUNNING_MESSAGE)


    def _spawnPublisher(self):
        self._publisher= self._spawnProcess(MyPublisher.commandToSpawn,
                                            self.PUBLISHER_LOG_PATH,
                                            MyPublisher.RUNNING_MESSAGE)



    def tearDown(self):
        print('tearingDown')
        TestHelper.dumpFileToStdout(self.SERVER_LOG_PATH)
        TestHelper.dumpFileToStdout(self.PUBLISHER_LOG_PATH)

        if self._server is not None:
            TestHelper.terminateSubprocess(self._server)
        if self._publisher is not None:
            TestHelper.terminateSubprocess(self._publisher)

        if self._wasSuccessful:
            self._removeTestFolderIfItExists()


    def _testExecuteWithSuccess(self):
        timeoutInSec= 2 * MyServer.TIME_TO_EXECUTE
        ret= self._client.callASuccessfulMethod(timeoutInSec)
        self.assertEqual(
            ret, MyServer.SUCCESS,
            'got %s instead of %s' % (str(ret), MyServer.SUCCESS))


    def _testExecuteAndTimeoutTwiceToAssesSocketIsStillValid(self):
        shortTimeout= 0.5 * MyServer.TIME_TO_EXECUTE
        self.assertRaises(
            ZmqRpcTimeoutError,
            self._client.callASuccessfulMethod, shortTimeout)
        self.assertRaises(
            ZmqRpcTimeoutError,
            self._client.callASuccessfulMethod, shortTimeout)


    def _raiseOnClientSideIfServerRaises(self):
        self.assertRaises(
            MyException,
            self._client.callAMethodThatRaisesMyException)


    def _testReturnObjectWithALogger(self):
        res= self._client.getAnObjectThatHasALogger(13)
        self.assertTrue(res.logger is not None)
        self.assertEqual(13, res.value)


    def _testPublisher(self):
        a= self._client.readFromPublisher()
        b= self._client.readFromPublisher()
        self.assertGreaterEqual(b.getValue(), a.getValue())



    def testMain(self):
        self._spawnServer()
        self._spawnPublisher()
        self._testExecuteWithSuccess()
        self._testExecuteAndTimeoutTwiceToAssesSocketIsStillValid()
        self._raiseOnClientSideIfServerRaises()
        self._testReturnObjectWithALogger()
        self._testPublisher()
        self._wasSuccessful= True


if __name__ == "__main__":
    unittest.main()
