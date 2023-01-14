#!/usr/bin/env python3
'''
URI manipulation.
'''

import logging
import pathlib
import urllib.parse


LOGGER = logging.getLogger(__name__)
FILENAME = 'meta.yaml'


class URITransformer():
    '''
    Transform URIs, including file paths.
    '''
    def __init__(self, uri):
        self.uri = uri
        self.parts = list(urllib.parse.urlparse(uri))
        self.path = self.parts[2]

    def __str__(self):
        parts = self.parts.copy()
        parts[2] = str(parts[2])
        if not parts[0]:
            return parts[2]
        return urllib.parse.urlunparse(parts)

    @property
    def scheme(self):
        '''
        The URI scheme.
        '''
        return self.parts[0]

    @property
    def is_local_file(self):
        '''
        True if the URI points to a local path, else False. The path may not exist.
        '''
        scheme = self.scheme
        return (not scheme) or scheme.lower() == 'file://'

    def _get_path(self):
        return self.parts[2]

    def _set_path(self, path):
        path = pathlib.Path(path)
        if self.is_local_file and not path.is_absolute():
            path = path.resolve()
        self.parts[2] = path

    path = property(
        fget=_get_path,
        fset=_set_path,
        doc='The URI path component'
    )
