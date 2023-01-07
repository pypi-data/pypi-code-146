class FileChanged(Exception):
    '''Raised when a file changes during an update'''

class IncompleteUpdateError(Exception):
    '''Raised when a backup is requested when there are files with unknown hashes.'''

class ArgumentError(Exception):
    '''Raised when an command line argument is invalid'''


class DiskNotFoundError(ArgumentError):
    '''Raised when a backup disk cannot be found'''
