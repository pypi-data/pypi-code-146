#!/usr/bin/env python3


if __name__ == '__main__':
    raise NotImplementedError('Please import Watch_Path instead')


import os
from collections import Iterator


class Watch_Path(dict, Iterator):
    """
    Python 2/3 compatible iterator that watches `path`
    for modified time changes and calls `callback`
    """

    def __init__(self, path, callback, **kwargs):
        # super(Watch_Path, self).__init__(**kwargs)
        self.update(time_stamp = self.file_modified_time(path),
                    path = path,
                    callback = callback)

        self.update(callback_kwargs = kwargs)

    def __iter__(self):
        return self

    def throw(self, type = None, traceback = None):
        raise StopIteration

    @staticmethod
    def file_modified_time(path):
        return os.stat(path).st_mtime

    def next(self):
        """
        When `self['time_stamp']` does not equal `new_time_stamp`
        calls and returns results of `self['callback']` function
        with argument similar to...

            path = self['path']
            time_stamp = self['time_stamp']
        """
        try:
            new_time_stamp = self.file_modified_time(self['path'])
        except OSError as e:
            print(e)
            self.throw(GeneratorExit)

        if new_time_stamp != self['time_stamp']:
            self['time_stamp'] = new_time_stamp
            return self['callback'](path = self['path'],
                                    time_stamp = new_time_stamp,
                                    **self['callback_kwargs'])

    __next__ = next
