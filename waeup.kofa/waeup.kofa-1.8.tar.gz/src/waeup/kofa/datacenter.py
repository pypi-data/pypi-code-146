## $Id: datacenter.py 15430 2019-05-28 06:14:44Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Kofa data center.

The waeup data center cares for management of upload data and provides
tools for importing/exporting CSV data.
"""
import codecs
import fnmatch
import grok
import os
import re
import shutil
from datetime import datetime
from zope.component import getUtility
from zope.component.interfaces import ObjectEvent
from waeup.kofa.interfaces import (IDataCenter, IDataCenterFile,
                                   IDataCenterStorageMovedEvent,
                                   IDataCenterConfig,
                                   IKofaUtils)
from waeup.kofa.utils.batching import ExportJobContainer
from waeup.kofa.utils.helpers import copy_filesystem_tree, merge_csv_files
from waeup.kofa.utils.logger import Logger


#: Regular expression describing a logfile name with backup extension
RE_LOGFILE_BACKUP_NAME = re.compile('^.+\.\d+$')

class DataCenter(grok.Container, Logger, ExportJobContainer):
    """A data center contains CSV files.
    """
    grok.implements(IDataCenter)

    logger_name = 'waeup.kofa.${sitename}.datacenter'
    logger_filename = 'datacenter.log'

    @property
    def max_files(self):
        return getUtility(IKofaUtils).MAX_FILES

    def __init__(self, *args, **kw):
        super(DataCenter, self).__init__(*args, **kw)
        self.storage = getUtility(IDataCenterConfig)['path']
        self._createSubDirs()

    def _createSubDirs(self):
        """Create standard subdirs.
        """
        for name in ['finished', 'graduated', 'unfinished', 'logs', 'deleted']:
            path = os.path.join(self.storage, name)
            if os.path.exists(path):
                continue
            os.mkdir(path)
        return

    @property
    def deleted_path(self):
        """Get the path for deleted student data.
        """
        return os.path.join(self.storage, 'deleted')

    @property
    def graduated_path(self):
        """Get the path for deleted graduated student data.
        """
        return os.path.join(self.storage, 'graduated')

    def getPendingFiles(self, sort='name'):
        """Get a list of files stored in `storage`.

        Files are sorted by basename.
        """
        result = []
        if not os.path.exists(self.storage):
            return result
        for filename in sorted(os.listdir(self.storage)):
            fullpath = os.path.join(self.storage, filename)
            if not os.path.isfile(fullpath):
                continue
            if not (filename.endswith('.csv') or filename.endswith('.gz')):
                continue
            result.append(DataCenterFile(fullpath))
        if sort == 'date':
            # sort results in newest-first order...
            result = sorted(result, key=lambda x: x.getTimeStamp(),
                            reverse=True)
        return result

    def getFinishedFiles(self):
        """Get a list of files stored in `finished` subfolder of `storage`.

        Files are unsorted.
        """
        result = []
        finished_dir = os.path.join(self.storage, 'finished')
        if not os.path.exists(finished_dir):
            return result
        mtime = lambda f: os.stat(os.path.join(finished_dir, f)).st_mtime
        finished_files = [f for f in
            sorted(os.listdir(finished_dir), key=mtime, reverse=True)
            if fnmatch.fnmatch(f, '*.finished.csv')]
        for filename in finished_files[:self.max_files]:
            fullpath = os.path.join(finished_dir, filename)
            if not os.path.isfile(fullpath):
                continue
            if not filename.endswith('.csv'):
                continue
            result.append(DataCenterFile(fullpath, 'finished'))
        return result

    def getLogFiles(self, exclude_backups=True):
        """Get the files from logs/ subdir. Files are sorted by name.

        By default backup logs ('app.log.1', etc.) and payments.log
        are excluded.
        """
        result = []
        logdir = os.path.join(self.storage, 'logs')
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        for name in sorted(os.listdir(logdir)):
            if not os.path.isfile(os.path.join(logdir, name)):
                continue
            if name == 'payments.log':
                continue
            if exclude_backups == True and RE_LOGFILE_BACKUP_NAME.match(name):
                continue
            result.append(
                LogFile(os.path.join(self.storage, 'logs', name)))
        return result

    def setStoragePath(self, path, move=False, overwrite=False):
        """Set the path where to store files.
        """
        path = os.path.abspath(path)
        not_copied = []
        if not os.path.exists(path):
            raise ValueError('The path given does not exist: %s' % path)
        if move is True:
            not_copied = copy_filesystem_tree(self.storage, path,
                                            overwrite=overwrite)
        self.storage = path
        self._createSubDirs()
        grok.notify(DataCenterStorageMovedEvent(self))
        return not_copied

    def _moveFile(self, source, dest):
        """Move file source to dest preserving ctime, mtime, etc.
        """
        if not os.path.exists(source):
            self.logger.warn('No such source path: %s' % source)
            return
        if source == dest:
            return
        shutil.copyfile(source, dest)
        shutil.copystat(source, dest)
        os.unlink(source)

    def _appendCSVFile(self, source, dest):
        """Append data from CSV file `source` to data from CSV file `dest`.

        The `source` file is deleted afterwards.
        """
        if not os.path.exists(dest):
            return self._moveFile(source, dest)
        if not os.path.exists(source):
            self.logger.warn('No such source path: %s' % source)
            return
        if source == dest:
            return
        result_path = merge_csv_files(dest, source)
        os.chmod(result_path, 0664)
        self._moveFile(result_path, dest)
        os.unlink(source)

    def distProcessedFiles(self, successful, source_path, finished_file,
                           pending_file, mode='create', move_orig=True):
        """Put processed files into final locations.

        ``successful`` is a boolean that tells, whether processing was
        successful.

        ``source_path``: path to file that was processed.

        ``finished_file``, ``pending_file``: paths to the respective
        generated .pending and .finished file. The .pending file path
        may be ``None``.

        If finished file is placed in a location outside the local
        storage dir, the complete directory is removed
        afterwards. Regular processors should put their stuff in
        dedicated temporary dirs.

        See datacenter.txt for more info about how this works.
        """
        basename = os.path.basename(source_path)
        pending_name = basename
        pending = False
        finished_dir = os.path.join(self.storage, 'finished')
        unfinished_dir = os.path.join(self.storage, 'unfinished')

        if basename.endswith('.pending.csv'):
            maybe_basename = "%s.csv" % basename.rsplit('.', 3)[0]
            maybe_src = os.path.join(unfinished_dir, maybe_basename)
            if os.path.isfile(maybe_src):
                basename = maybe_basename
                pending = True

        base, ext = os.path.splitext(basename)
        finished_name = "%s.%s.finished%s" % (base, mode, ext)
        if not pending:
            pending_name = "%s.%s.pending%s" % (base, mode, ext)

        # Put .pending and .finished file into respective places...
        pending_dest = os.path.join(self.storage, pending_name)
        finished_dest = os.path.join(finished_dir, finished_name)
        self._appendCSVFile(finished_file, finished_dest)
        if pending_file is not None:
            self._moveFile(pending_file, pending_dest)

        # Put source file into final location...
        finished_dest = os.path.join(finished_dir, basename)
        unfinished_dest = os.path.join(unfinished_dir, basename)
        if successful and not pending:
            self._moveFile(source_path, finished_dest)
        elif successful and pending:
            self._moveFile(unfinished_dest, finished_dest)
            os.unlink(source_path)
        elif not successful and not pending:
            self._moveFile(source_path, unfinished_dest)

        # If finished and pending-file were created in a location
        # outside datacenter storage, we remove it.
        maybe_temp_dir = os.path.dirname(finished_file)
        if os.path.commonprefix(
            [self.storage, maybe_temp_dir]) != self.storage:
            shutil.rmtree(maybe_temp_dir)
        return

    def _logfiles(self, basename):
        """Get sorted logfiles starting with `basename`.
        """
        def numerical_suffix(name):
            # return numerical suffix in `name` as number or 0.
            suffix = name.rsplit('.', 1)[-1]
            try:
                return int(suffix)
            except ValueError:
                return 0
            pass
        files = [basename,]
        for name in os.listdir(os.path.join(self.storage, 'logs')):
            if RE_LOGFILE_BACKUP_NAME.match(name):
                if name.rsplit('.', 1)[0] == basename:
                    files.append(name)
        return sorted(files, key=numerical_suffix, reverse=True)

    def queryLogfiles(self, basename, query=None, limit=0, start=0):
        """Search `query` in all logfiles starting with `basename`.

        Returns an iterator of those lines in logfiles starting with
        `basename` that match `query`. If you want the result as a
        list, simply list() the iterator.

        All logfiles with name `basename` and maybe some numerical
        extension ('.1', '.2', ...) are searched for the `query` term
        in correct chronological order. So, if you ask for a basename 'app.log',
        then any file named 'app2.log', 'app.log.1', 'app.log',
        etc. will be searched in that order.

        The `query` is expected to be a string containing a regular
        expression.

        If `limit` is set to some numerical value, at most this number
        of lines is returned.

        With `start` you can give the number of first matched line to
        return. `start` is zero-based, i.e. the first match has number
        0, the scond one 1, etc.

        Together with `limit` this allows some basic
        batching. Please keep in mind that batching might give
        unpredictable results, when logfiles change between two
        requests. This is not a problem when only one file is searched
        and changes include only appending new log messages.

        Matches are found per line only (no multiline matches).

        Result lines are returned as unicode instances decoded from
        UTF-8 encoding. This means that logfiles must provide UTF-8
        encoding for umlauts etc. if these should be rendered
        properly. The returned unicode lines can be fed to page
        templates even if they contain non-ASCII characters.

        This method raises ValueError if some basic condition is not
        met, for instance if the given query string is not a valid
        regular expression.

        Please note, that this exception will happen not before you
        really fetch a result line.
        """
        try:
            re_query = re.compile(query)
        except:
            raise ValueError('Invalid query string: %s' % query)

        basename = basename.replace('/../', '')
        files = self._logfiles(basename)

        # Search the log files
        num = 0
        for name in files:
            path = os.path.join(self.storage, 'logs', name)
            if not os.path.isfile(path):
                continue
            for line in codecs.open(path, 'rb', 'utf-8'):
                if not re_query.search(line):
                    continue
                num += 1
                if (num - 1) < start:
                    continue
                yield line

                if limit and (num - limit >= start):
                    raise StopIteration
        pass

class DataCenterFile(object):
    """A description of a file stored in data center.
    """
    grok.implements(IDataCenterFile)

    def __init__(self, context, folder_name=''):
        self.context = context
        self.name = os.path.basename(self.context)
        self.rel_path = os.path.join(folder_name, self.name)
        self.size = self.getSize()
        self.uploaddate = self.getDate()
        self.lines = self.getLinesNumber()

    def getDate(self):
        """Get a human readable datetime representation.
        """
        date = datetime.fromtimestamp(os.path.getmtime(self.context))
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def getTimeStamp(self):
        """Get a (machine readable) timestamp.
        """
        return os.path.getmtime(self.context)

    def getSize(self):
        """Get a human readable file size.
        """
        bytesize = os.path.getsize(self.context)
        size = "%s bytes" % bytesize
        units = ['kb', 'MB', 'GB']
        for power, unit in reversed(list(enumerate(units))):
            power += 1
            if bytesize >= 1024 ** power:
                size = "%.2f %s" % (bytesize/(1024.0**power), unit)
                break
        return size

    def getLinesNumber(self):
        """Get number of lines.
        """
        num = 0
        if not self.context.title().lower().endswith('csv'):
            return 1
        for line in open(self.context, 'rb'):
            num += 1
        return num

class LogFile(DataCenterFile):
    """A description of a log file.
    """
    def __init__(self, context):
        super(LogFile, self).__init__(context)
        self._markers = dict()
        self._parsed = False
        self.userid = self.getUserId()
        self.mode = self.getMode()
        self.stats = self.getStats()
        self.source = self.getSourcePath()

    def _parseFile(self, maxline=10):
        """Find markers in a file.
        """
        if self._parsed:
            return
        for line in codecs.open(self.context, 'rb', 'utf-8'):
            line = line.strip()
            if not ':' in line:
                continue
            name, text = line.split(':', 1)
            self._markers[name.lower()] = text
        self._parsed = True
        return

    def _getMarker(self, marker):
        marker = marker.lower()
        if not self._parsed:
            self._parseFile()
        if marker in self._markers.keys():
            return self._markers[marker]

    def getUserId(self):
        return self._getMarker('user') or '<UNKNOWN>'

    def getMode(self):
        return self._getMarker('mode') or '<NOT SET>'

    def getStats(self):
        return self._getMarker('processed') or '<Info not avail.>'

    def getSourcePath(self):
        return self._getMarker('source') or None


class DataCenterStorageMovedEvent(ObjectEvent):
    """An event fired, when datacenter storage moves.
    """
    grok.implements(IDataCenterStorageMovedEvent)
