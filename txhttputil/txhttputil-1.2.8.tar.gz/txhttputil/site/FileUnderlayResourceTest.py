import logging
import os

from twisted.internet import reactor
from twisted.trial import unittest
from twisted.web import server
from twisted.web.resource import ErrorPage

import txhttputil
from txhttputil.downloader.HttpFileDownloader import HttpFileDownloader
from txhttputil.site.FileUnderlayResource import FileUnderlayResource

logger = logging.getLogger(__name__)


LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s:%(message)s"
DATE_FORMAT = "%d-%b-%Y %H:%M:%S"
logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT, level=logging.DEBUG)


class FileUnderlayResourceTest(unittest.TestCase):
    PORT = 7999

    def setUp(self):
        rootResource = FileUnderlayResource()

        self.fsRoot = os.path.dirname(txhttputil.__file__)
        rootResource.addFileSystemRoot(self.fsRoot)

        logger.info("Test file system root = %s", self.fsRoot)

        rootResource.putChild(
            b"test", ErrorPage(200, "This path worked, /test", "")
        )

        self.site = reactor.listenTCP(self.PORT, server.Site(rootResource))

        self.sitePath = "http://%s:%s" % ("127.0.0.1", self.site.port)

    def tearDown(self):
        d = self.site.stopListening()
        return d

    def _checkDownloadedResource(
        self, spooledNamedTempFile, fileName=None, testContents=None
    ):
        contents = spooledNamedTempFile.read()
        logger.debug(contents)

        if fileName:
            with open(fileName, "rb") as f:
                self.assertEqual(contents, f.read())

        if testContents:
            self.assertEqual(contents, testContents)

    def testDowloadUnderlayRootFile(self):
        testContents = (
            b"\n<html>\n  <head><title>200 - This path worked, /test</title><"
            b"/head>\n  <body>\n    <h1>This path worked, /test</h1>\n    "
            b"<p></p>\n  </body>\n</html>\n"
        )

        d = HttpFileDownloader(self.sitePath + "/test").run()
        d.addCallback(self._checkDownloadedResource, testContents=testContents)
        return d

    def testDowloadUnderlayFile2(self):
        fileName = "/login_page/LoginElement.py"
        realPath = self.fsRoot + fileName

        d = HttpFileDownloader(self.sitePath + fileName).run()
        d.addCallback(self._checkDownloadedResource, fileName=realPath)
        return d
