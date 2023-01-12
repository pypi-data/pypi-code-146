"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""

import logging
import mimetypes
import os
from collections import namedtuple
from datetime import date, timedelta
from time import mktime
from urllib.request import pathname2url
from wsgiref.handlers import format_date_time

from filetype import filetype
from twisted.internet.task import cooperate
from twisted.web.server import NOT_DONE_YET
from txhttputil.site.BasicResource import BasicResource
from txhttputil.util.DeferUtil import deferToThreadWrap

logger = logging.getLogger(__name__)

FileData = namedtuple("FileData", ["fobj", "size", "cacheControl", "expires"])


class StaticFileResource(BasicResource):
    """ """

    isLeaf = True

    __STATIC_MIME_TYPES = [
        (".js.map", "application/json"),
        (".js", "application/javascript"),
    ]

    def __init__(
        self, filePath: str, expireMinutes: int = 30, chunkSize: int = 128000
    ):
        BasicResource.__init__(self)
        self._filePath = filePath
        self.cancelDownload = False
        self.expireMinutes = expireMinutes
        self.chunkSize = chunkSize

        # Set the MIME Type
        for extension, mimetype in self.__STATIC_MIME_TYPES:
            if filePath.endswith(extension):
                self._mimetype = mimetype
                return

        fileTypeGuess = filetype.guess(filePath)
        if fileTypeGuess:
            self._mimetype = fileTypeGuess.mime

        else:
            self._mimetype = mimetypes.guess_type(
                pathname2url(filePath), strict=False
            )[0]

        assert self._mimetype, "Unknown mime type for: %s" % filePath

    def render_GET(self, request):
        request.responseHeaders.setRawHeaders(b"content-type", [self._mimetype])
        return self.serveStaticFileWithCache(request)

    def serveStaticFileWithCache(self, request):
        """Resource Create And Serve Static File

        This should probably be a class now.

        """

        d = self.loadFileInThread(request)
        d.addCallback(self._setHeaders, request)
        d.addCallback(self._writeData, request)
        d.addErrback(self._fileFailed, request)

        request.notifyFinish().addErrback(self._closedError)

        return NOT_DONE_YET

    @deferToThreadWrap
    def loadFileInThread(self, request):
        requestPath = request.path
        if not self._filePath or not os.path.exists(self._filePath):
            raise Exception(
                "File %s doesn't exist for resource %s"
                % (self._filePath, requestPath)
            )

        size = os.stat(self._filePath).st_size
        fobj = open(self._filePath, "rb")

        expiry = (date.today() + timedelta(self.expireMinutes)).timetuple()
        expiresTime = format_date_time(mktime(expiry))

        cacheControl = (
            b"max-age=" + str(self.expireMinutes * 60).encode()
        )  # In Seconds
        cacheControl += b", private"

        return FileData(
            fobj=fobj, size=size, cacheControl=cacheControl, expires=expiresTime
        )

    def _setHeaders(self, fileData, request):
        # DISABLED
        # Cache control is disabled for gziped resources as they are chunk-encoded
        # request.setHeader("Cache-Control", fileData.cacheControl)
        # request.setHeader("Expires", fileData.expires)
        request.setHeader(b"Content-Length", str(fileData.size))
        return fileData

    def _writeData(self, fileData, request):
        def writer():
            try:
                data = fileData.fobj.read(self.chunkSize)
                while data and not self.cancelDownload:
                    request.write(data)
                    yield None  # Yield to the reactor for a bit
                    data = fileData.fobj.read(self.chunkSize)
                    yield None  # Allow any "NotifyFinish" updates

                if not self.cancelDownload:
                    request.finish()

                fileData.fobj.close()

            except Exception as e:
                logger.error(
                    "An error occured loading and sending the file"
                    " data for file %s for resource %s",
                    self._filePath,
                    request.path,
                )
                logger.exception(e)

        return cooperate(writer())

    def _fileFailed(self, failure, request):
        self.cancelDownload = True
        request.setResponseCode(404)
        logger.error(str(failure.value))
        request.finish()

        logger.error(
            "Failed to send file %s for resource %s",
            self._filePath,
            request.path,
        )
        logger.exception(failure.value)

    def _closedError(self, failure):
        self.cancelDownload = True
        logger.error("Got closedError %s" % failure)
