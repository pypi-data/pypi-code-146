import json
import logging
from base64 import b64decode
from base64 import b64encode

from twisted.internet import protocol
from twisted.internet.defer import Deferred
from twisted.internet.defer import inlineCallbacks
from vortex.DeferUtil import deferToThreadWrapWithLogger

from .simple_subproc_task_call_tuple import SimpleSubprocTaskCallTuple
from .simple_subproc_task_constructor_tuple import (
    SimpleSubprocTaskConstructorTuple,
)
from .simple_subproc_task_result_tuple import SimpleSubprocTaskResultTuple

logger = logging.getLogger(__name__)


class SimpleSubprocParentProtocol(protocol.ProcessProtocol):
    def __init__(self, constructorTuple: SimpleSubprocTaskConstructorTuple):
        self._constructorTuple = constructorTuple
        self._data = b""
        self._logData = b""
        self._deferredByUuid = {}

    def connectionMade(self):
        self.transport.write(
            b64encode(json.dumps(self._constructorTuple.toJsonDict()).encode())
        )
        self.transport.write(b".")

    def errReceived(self, data: bytes):
        self._logData += data

        while b"\n" in self._logData:
            message, self._logData = self._logData.split(b"\n", 1)
            if not message:
                continue

            message = message.decode()

            if ":" not in message:
                logger.error(message)

            else:
                severity, logMsg = message.split(":", 1)
                if severity == "DEBUG":
                    logger.debug(logMsg)
                elif severity == "INFO":
                    logger.info(logMsg)
                elif severity == "WARNING":
                    logger.warning(logMsg)
                elif severity == "ERROR":
                    logger.error(logMsg)
                else:
                    logger.error(message)

    @inlineCallbacks
    def outReceived(self, data):
        self._data += data

        while b"." in self._data:
            message, self._data = self._data.split(b".", 1)
            if not message:
                continue

            resultTuple = yield self._decodeResult(message)

            d = self._deferredByUuid.pop(resultTuple.commandUuid)
            if resultTuple.exceptionStr:
                d.errback(Exception(resultTuple.exceptionStr))
            else:
                d.callback(resultTuple.result)

    @inlineCallbacks
    def queueCommand(self, command: SimpleSubprocTaskCallTuple) -> Deferred:
        d = Deferred()
        self._deferredByUuid[command.commandUuid] = d

        commandMessage = yield self._encodeCall(command)
        self.transport.write(commandMessage)
        self.transport.write(b".")
        return (yield d)

    @deferToThreadWrapWithLogger(logger)
    def _encodeCall(self, command):
        return b64encode(json.dumps(command.toJsonDict()).encode())

    @deferToThreadWrapWithLogger(logger)
    def _decodeResult(self, message):
        return SimpleSubprocTaskResultTuple().fromJsonDict(
            json.loads(b64decode(message))
        )
