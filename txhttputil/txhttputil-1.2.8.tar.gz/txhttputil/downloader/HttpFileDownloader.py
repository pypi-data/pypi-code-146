"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging
from typing import Union

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web._newclient import ResponseDone
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from pytmpdir.spooled_named_temporary_file import (
    SpooledNamedTemporaryFile,
)

logger = logging.getLogger(__name__)


class HttpFileDownloader:
    def __init__(self, url: Union[str, bytes], tmpDir: str = None):
        self._tmpDir = tmpDir
        self._url = url.encode() if isinstance(url, str) else url

    def run(self):
        agent = Agent(reactor)

        d = agent.request(
            b"GET",
            self._url,
            Headers({b"User-Agent": [b"Synerty File Downloader"]}),
            None,
        )

        def cbResponse(response):
            if response.code == 200:
                bodyDownloader = _FileDownloaderBody(self._tmpDir)
            else:
                bodyDownloader = _BodyError(
                    response.code, response.request.absoluteURI
                )
            response.deliverBody(bodyDownloader)
            return bodyDownloader.deferred

        d.addCallback(cbResponse)

        return d


class _FileDownloaderBody(Protocol):
    def __init__(self, tmpDir: str = None):
        self._finishedDeferred = Deferred()
        self._tmpFile = SpooledNamedTemporaryFile(dir=tmpDir)
        self._writeSize = 0

    @property
    def deferred(self):
        return self._finishedDeferred

    def dataReceived(self, data: bytes):
        self._tmpFile.write(data)
        self._writeSize += len(data)

    def connectionLost(self, reason):
        self._tmpFile.flush()
        self._tmpFile.seek(0)

        if isinstance(reason.value, ResponseDone):
            logger.debug("File download complete, size=%s", self._writeSize)
            self._finishedDeferred.callback(self._tmpFile)
            return

        self._finishedDeferred.errback(reason)


class _BodyError(Protocol):
    def __init__(self, responseCode, responseUri):
        self._finishedDeferred = Deferred()
        self._responseCode = responseCode
        self._responseUri = responseUri
        self._msg = ""

    @property
    def deferred(self):
        return self._finishedDeferred

    def dataReceived(self, bytes):
        self._msg += bytes

    def connectionLost(self, reason):
        self._finishedDeferred.errback(
            Exception(
                "Server returned %s for %s\n%s\n%s"
                % (self._responseCode, self._responseUri, reason, self._msg)
            )
        )
