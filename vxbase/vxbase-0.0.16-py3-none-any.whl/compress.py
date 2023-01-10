import logging
from os import path
from shutil import move
from vxbase.vtypes import is_iterable, get_error_message
import tarfile
import zipfile


_logger = logging.getLogger(__name__)


def compress_files(name, files, dest_folder=None, cformat='bz2'):
    """ Compress a file, set of files or a folder in the specified cforma

    :param name: Desired file name w/o extension
    :param files: A list with the absolute o relative path to the files
                      that will be added to the compressed file
    :param dest_folder: The folder where will be stored the compressed file
    :param cformat: Desired format for compression, only supported bz2 and gz
    """
    if not dest_folder:
        dest_folder = '.'
    if cformat not in ['bz2', 'gz', 'tar']:
        raise RuntimeError('Unknown file format "{}"'.format(cformat))
    ext = ''
    if cformat == 'gz':
        fobject, modestr = tarfile.open, 'w:gz'
        ext = 'tar.gz'
    elif cformat == 'tar':
        fobject, modestr = tarfile.open, 'w:'
        ext = 'tar'
    elif cformat == 'bz2':
        fobject, modestr = tarfile.open, 'w:bz2'
        ext = 'tar.bz2'
    _logger.debug("Generating compressed file: %s in %s folder",
                  name, dest_folder)

    bkp_name = '{0}.{1}'.format(name, ext)
    full_tmp_name = path.join(
        dest_folder,
        '._{}'.format(bkp_name)
    )
    full_name = path.join(dest_folder, bkp_name)

    with fobject(full_tmp_name, mode=modestr) as tar_file:
        for fname in files:
            if is_iterable(fname):
                tar_file.add(fname[0], path.join(name, fname[1]))
            else:
                basename = path.basename(fname)
                tar_file.add(fname, path.join(name, basename))
    move(full_tmp_name, full_name)
    return full_name


class DecompressHelper:
    valid_extensions = ('tar.gz', 'tar.bz2', 'zip', 'tar')

    def __init__(self, filename):
        self.fobject = self.get_decompress_object(filename)

    @property
    def support_methods(self):
        suport_method = {
            "tar.gz": lambda fname: tarfile.open(fname, mode='r:gz'),
            "tar.bz2": lambda fname: tarfile.open(fname, mode='r:bz2'),
            "tar": lambda fname: tarfile.open(fname, mode='r:'),
            "zip": lambda fname: zipfile.ZipFile(fname, mode='r')
        }
        return suport_method

    def extractall(self, dest_folder):
        self.fobject.extractall(dest_folder)

    def name_list(self):
        values = []
        if isinstance(self.fobject, tarfile.TarFile):
            values = [i.name for i in self.fobject.getmembers()]
        if isinstance(self.fobject, zipfile.ZipFile):
            values = self.fobject.namelist()
        return values

    def get_decompress_object(self, filename):
        for ext in self.valid_extensions:
            if filename.endswith(ext):
                return self.support_methods[ext](filename)
        return False


def decompress_files(name, dest_folder):
    """ Decompress a file, set of files or a folder compressed in tar.bz2 format

    :param name: Compressed file name (full or relative path)
    :param dest_folder: Folder where the decompressed files will be extracted
    :return: The absolute path to decompressed folder or file
    """
    assert path.exists(name)
    _logger.debug("Decompressing file: %s", name)
    if path.isdir(name):
        return name
    _logger.debug('Extracting %s into %s', name, dest_folder)
    fobject = DecompressHelper(name)
    try:
        fobject.extractall(dest_folder)
    except (EOFError, IOError) as error:
        _logger.exception('Error uncompressing file %s', get_error_message(error))
        raise
    name_list = fobject.name_list()
    base_folder = dest_folder
    for fname in name_list:
        if (path.basename(fname) in
           ['dump.sql', 'database_dump.b64', 'database_dump.sql', 'database_dump']):
            base_folder = path.dirname(fname)
            break

    _logger.debug("Destination folder: %s", dest_folder)
    _logger.debug("Bakcup folder: %s", base_folder)
    if name.endswith(DecompressHelper.valid_extensions):
        fname = path.basename(name)
        dest_folder = path.join(dest_folder, base_folder)
    _logger.debug("Destination folder: %s", dest_folder)
    return dest_folder
