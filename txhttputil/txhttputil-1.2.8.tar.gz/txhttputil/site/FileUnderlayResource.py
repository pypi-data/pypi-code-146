import logging
from typing import Union, List

import os
from twisted.web.resource import NoResource
from twisted.web.util import Redirect

from txhttputil.site.BasicResource import BasicResource
from txhttputil.site.RedirectionRule import RedirectionRule

logger = logging.getLogger(__name__)

import mimetypes

mimetypes.init()


def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


IMAGE_EXTENSIONS = list(get_extensions_for_type('image'))
FONT_EXTENSIONS = list(get_extensions_for_type('font'))


class SinglePageAppConfig:
    def __init__(self, **kwargs):
        self.indexHtmlPath = None

        for kw, arg in kwargs.items():
            if not hasattr(self, kw):
                raise KeyError("%s is not an argument for %s" % (kw, self.__class__))
            setattr(self, kw, arg)


class FileUnderlayResource(BasicResource):
    """
    This class resolves URLs into either a static file or a C{BasicResource}

    This is a multi level search :
    1) getChild, looking for resource in the resource tree
    2) The staticFileUnderlay is searched.
    3) Request fails with NoResource()

    """

    acceptedExtensions = ['.js', '.css', '.html', '.xml']
    acceptedExtensions += FONT_EXTENSIONS
    acceptedExtensions += IMAGE_EXTENSIONS

    # TODO Implement accepted extensions

    def __init__(self):
        BasicResource.__init__(self)

        self._fileSystemRoots = []
        self._singlePageAppConfig = None
        self._redirections = {}

    def addRedirectionRule(self, redirection: RedirectionRule = None):
        if redirection is not None:
            self._redirections[redirection.origin] = redirection.destination

    def getFileResource(self, postPath):
        from txhttputil.site.StaticFileResource import StaticFileResource

        resourcePath = os.path.join(*postPath).decode() if postPath else None
        filePath = self.getRealFilePath(resourcePath) if resourcePath else None

        if filePath:
            return self._gzipIfRequired(StaticFileResource(filePath))

        if not resourcePath or not '.' in os.path.basename(resourcePath):
            singlePageResource = self._getSinglePageAppResource()
            if singlePageResource:
                return singlePageResource

        return NoResource()

    def addFileSystemRoot(self, fileSystemRoot: str):
        if not os.path.isdir(fileSystemRoot):
            raise NotADirectoryError("%s is not a directory" % fileSystemRoot)

        self._fileSystemRoots.append(fileSystemRoot)

    def enableSinglePageApplication(self, indexHtmlPath="index.html"):
        self._singlePageAppConfig = SinglePageAppConfig(indexHtmlPath=indexHtmlPath)

    def getRealFilePath(self, resourcePath: str) -> Union[str, None]:
        if not resourcePath:
            return None

        for rootDir in self._fileSystemRoots[::-1]:
            realFilePath = os.path.join(rootDir, resourcePath)

            if os.path.isdir(realFilePath):
                logger.debug("Resource path %s is a directory %s",
                             resourcePath, realFilePath)
                continue

            if os.path.isfile(realFilePath):
                return realFilePath

    def _getSinglePageAppResource(self):
        if not self._singlePageAppConfig:
            return None

        # Try to serve a single page app
        filePath = self.getRealFilePath(self._singlePageAppConfig.indexHtmlPath)
        if filePath:
            from txhttputil.site.StaticFileResource import StaticFileResource
            return self._gzipIfRequired(StaticFileResource(filePath))

    def render_GET(self, request):
        """ Render Get

        If we're being redered then that means we've exactly matched the resurce path.
        IE, The path is looking for a directory, not a file.

        """

        singlePageAppResource = self._getSinglePageAppResource()
        if singlePageAppResource:
            return singlePageAppResource.render_GET(request)

        # Else, render no resource
        return NoResource().render(request)

    def getChild(self, path, request):
        if request.uri in self._redirections.keys():
            return Redirect(self._redirections[request.uri])
        return super().getChild(path, request)