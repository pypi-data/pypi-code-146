## $Id: batching.py 16012 2020-02-24 21:26:35Z henrik $
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
"""Kofa components for batch processing.

Batch processors eat CSV files to add, update or remove large numbers
of certain kinds of objects at once.
"""
import grok
import datetime
import os
import shutil
import tempfile
import time
import unicodecsv
import zc.async.interfaces
from cStringIO import StringIO
from persistent.list import PersistentList
from zope.component import createObject, getUtility
from zope.component.hooks import setSite
from zope.interface import Interface, implementer
from zope.schema import getFields
from zope.schema.interfaces import ConstraintNotSatisfied, RequiredMissing
from zope.event import notify
from waeup.kofa.async import AsyncJob
from waeup.kofa.interfaces import (
    IBatchProcessor, FatalCSVError, IObjectConverter, IJobManager,
    ICSVExporter, IGNORE_MARKER, DuplicationError, JOB_STATUS_MAP,
    IExportJobContainer, IExportJob, IExportContainerFinder)

class BatchProcessor(grok.GlobalUtility):
    """A processor to add, update, or remove data.

    This is a non-active baseclass.
    """
    grok.implements(IBatchProcessor)
    grok.context(Interface)
    grok.baseclass()

    # Name used in pages and forms...
    name = u'Non-registered base processor'

    # Internal name...
    util_name = ''

    # Items for this processor need an interface with zope.schema fields.
    iface = Interface

    # The name must be the same as the util_name attribute in order to
    # register this utility correctly.
    grok.name(util_name)

    # Headers needed to locate items...
    location_fields = []

    # A factory with this name must be registered...
    factory_name = ''

    @property
    def required_fields(self):
        """Required fields that have no default.

        A list of names of field, whose value cannot be set if not
        given during creation. Therefore these fields must exist in
        input.

        Fields with a default != missing_value do not belong to this
        category.
        """
        result = []
        for key, field in getFields(self.iface).items():
            if key in self.location_fields:
                continue
            if field.default is not field.missing_value:
                continue
            if field.required:
                result.append(key)
        return result

    @property
    def req(self):
        result = dict(
            create = self.location_fields + self.required_fields,
            update = self.location_fields,
            remove = self.location_fields,
        )
        return result

    @property
    def available_fields(self):
        return sorted(list(set(
                    self.location_fields + getFields(self.iface).keys())))

    def getHeaders(self, mode='create'):
        return self.available_fields

    def checkHeaders(self, headerfields, mode='create'):
        req = self.req[mode]
        # Check for required fields...
        for field in req:
            if not field in headerfields:
                raise FatalCSVError(
                    "Need at least columns %s for import!" %
                    ', '.join(["'%s'" % x for x in req]))
        # Check for double fields. Cannot happen because this error is
        # already catched in views
        not_ignored_fields = [x for x in headerfields
                              if not x.startswith('--')]
        if len(set(not_ignored_fields)) < len(not_ignored_fields):
            raise FatalCSVError(
                "Double headers: each column name may only appear once.")
        return True

    def applyMapping(self, row, mapping):
        """Apply mapping to a row of CSV data.
        """
        result = dict()
        for key, replacement in mapping.items():
            if replacement == u'--IGNORE--':
                # Skip ignored columns in failed and finished data files.
                continue
            result[replacement] = row[key]
        return result

    def getMapping(self, path, headerfields, mode):
        """Get a mapping from CSV file headerfields to actually used fieldnames.

        """
        result = dict()
        reader = unicodecsv.reader(open(path, 'rb'))
        raw_header = reader.next()
        for num, field in enumerate(headerfields):
            if field not in self.location_fields and mode == 'remove':
                # Skip non-location fields when removing.
                continue
            if field == u'--IGNORE--':
                # Skip ignored columns in failed and finished data files.
                continue
            result[raw_header[num]] = field
        return result

    def stringFromErrs(self, errors, inv_errors):
        result = []
        for err in errors:
            fieldname, message = err
            result.append("%s: %s" % (fieldname, message))
        for err in inv_errors:
            result.append("invariant: %s" % err)
        return '; '.join(result)

    def callFactory(self, *args, **kw):
        return createObject(self.factory_name)

    def parentsExist(self, row, site):
        """Tell whether the parent object for data in ``row`` exists.
        """
        raise NotImplementedError('method not implemented')

    def entryExists(self, row, site):
        """Tell whether there already exists an entry for ``row`` data.
        """
        raise NotImplementedError('method not implemented')

    def getParent(self, row, site):
        """Get the parent object for the entry in ``row``.
        """
        raise NotImplementedError('method not implemented')

    def getEntry(self, row, site):
        """Get the object for the entry in ``row``.
        """
        raise NotImplementedError('method not implemented')

    def addEntry(self, obj, row, site):
        """Add the entry given given by ``row`` data.
        """
        raise NotImplementedError('method not implemented')

    def delEntry(self, row, site):
        """Delete entry given by ``row`` data.
        """
        raise NotImplementedError('method not implemented')

    def checkCreateRequirements(self, parent, row, site):
        """Checks requirements the parent object must fulfill when
        a new subobject is being created.

        This method is not used in case of updating or removing objects.

        Returns error messages as strings in case of requirement
        problems.
        """
        return None

    def checkUpdateRequirements(self, obj, row, site):
        """Checks requirements the object must fulfill when being updated.

        This method is not used in case of deleting or adding objects.

        Returns error messages as strings in case of requirement
        problems.
        """
        return None


    def checkRemoveRequirements(self, obj, row, site):
        """Checks requirements the object must fulfill when being removed.

        This method is not used in case of updating or adding objects.

        Returns error messages as strings in case of requirement
        problems.
        """
        return None

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.

        Returns a string describing the fields changed.
        """
        changed = []
        for key, value in row.items():
            # Skip fields to be ignored.
            if value == IGNORE_MARKER:
                continue
            # Skip fields not declared in interface and which are
            # not yet attributes of existing objects. We can thus not
            # add non-existing attributes here.
            if not hasattr(obj, key):
                continue
            # DefaultObjectConverter.fromStringDict fails for
            # list-of-choices fields because we are using a different
            # widget for this combination. Thus the ListFieldConverter
            # returns a useless dictionary which causes getWidgetsData to
            # skip the field. The value in row remains unchanged. 
            # We have to evaluate the string and replace the value here.
            try:
                evalvalue = eval(value)
                if isinstance(evalvalue, list):
                    value = evalvalue
            except:
                pass
            try:
                setattr(obj, key, value)
            except AttributeError:
                # Computed attributes can't be set.
                continue
            log_value = getattr(value, 'code', value)
            changed.append('%s=%s' % (key, log_value))

        # If any catalog is involved it must be updated.
        #
        # XXX: The event is also triggered when creating objects as
        # updateEntry is called also when creating entries resulting
        # in objectAdded and additional objectModified events.
        if len(changed):
            notify(grok.ObjectModifiedEvent(obj))

        return ', '.join(changed)

    def createLogfile(self, path, fail_path, num, warnings, mode, user,
                      timedelta, logger=None):
        """Write to log file.
        """
        if logger is None:
            return
        logger.info(
            "processed: %s, %s mode, %s lines (%s successful/ %s failed), "
            "%0.3f s (%0.4f s/item)" % (
            path, mode, num, num - warnings, warnings,
            timedelta, timedelta/(num or 1)))
        return

    def writeFailedRow(self, writer, row, warnings):
        """Write a row with error messages to error CSV.

        If warnings is a list of strings, they will be concatenated.
        """
        error_col = warnings
        if isinstance(warnings, list):
            error_col = ' / '.join(warnings)
        row['--ERRORS--'] = error_col
        writer.writerow(row)
        return

    def checkConversion(self, row, mode='ignore', ignore_empty=True):
        """Validates all values in row.
        """
        converter = IObjectConverter(self.iface)
        errs, inv_errs, conv_dict =  converter.fromStringDict(
            row, self.factory_name, mode=mode)
        return errs, inv_errs, conv_dict


    def emptyRow(self, row):
        """Detect empty rows.
        """
        for value in row.values():
            if not value in (None, IGNORE_MARKER) and value.strip():
                return False
        return True

    def doImport(self, path, headerfields, mode='create', user='Unknown',
                 logger=None, ignore_empty=True):
        """In contrast to most other methods, `doImport` is not supposed to
        be customized, neither in custom packages nor in derived batch
        processor classes. Therefore, this is the only place where we
        do import data.

        Before this method starts creating or updating persistent data, it
        prepares two more files in a temporary folder of the filesystem: (1)
        a file for pending data with file extension ``.pending`` and (2)
        a file for successfully processed data with file extension
        ``.finished``. Then the method starts iterating over all rows of
        the CSV file. Each row is treated as follows:

        1. An empty row is skipped.

        2. Empty strings or lists (``[]``) in the row are replaced by
           ignore markers.

        3. The `BatchProcessor.checkConversion` method validates and converts 
           all values in the row. Conversion means the transformation of strings
           into Python objects. For instance, number expressions have to be
           transformed into integers, dates into datetime objects, phone number
           expressions into phone number objects, etc. The converter returns a
           dictionary with converted values or, if the validation of one of the
           elements fails, an appropriate warning message. If the conversion
           fails a pending record is created and stored in the pending data file
           together with a warning message the converter has raised.

        4. In **create mode** only:

           The parent object must be found and a child
           object with same object id must not exist. Otherwise the row
           is skipped, a corresponding warning message is raised and a
           record is stored in the pending data file.

           The `BatchProcessor.checkCreateRequirements` method checks additional
           requirements the parent object must fulfill before a new sububject
           is being added. These requirements are not imposed by the data
           type but the context of the object. For example, the course results
           of graduated students must not changed by import, neither by 
           creating nor updating or removing course tickets.

           Now `doImport` tries to add the new object with the data
           from the conversion dictionary. In some cases this
           may fail and a `DuplicationError` is raised. For example, a new
           payment ticket is created but the same payment for same session
           has already been made. In this case the object id is unique, no
           other object with same id exists, but making the 'same' payment
           twice does not make sense. The import is skipped and a
           record is stored in the pending data file.

        5. In **update mode** only:

           If the object can't be found, the row is skipped,
           a ``no such entry`` warning message is raised and a record is
           stored in the pending data file.

           The `BatchProcessor.checkUpdateRequirements` method checks additional
           requirements the object must fulfill before being updated. These
           requirements are not imposed by the data type but the context
           of the object. For example, post-graduate students have a different
           registration workflow. With this method we do forbid certain workflow
           transitions or states. 

           Finally, `doImport` updates the existing object with the data
           from the conversion dictionary.

        6. In **remove mode** only:

           If the object can't be found, the row is skipped,
           a ``no such entry`` warning message is raised and a record is
           stored in the pending data file.

           The `BatchProcessor.checkRemoveRequirements` method checks additional
           requirements the object must fulfill before being removed.
           These requirements are not imposed by the data type but the context
           of the object. For example, the course results of graduated students
           must not changed by import, neither by creating nor updating or
           removing course tickets.

           Finally, `doImport` removes the existing object.

        """
        time_start = time.time()
        self.checkHeaders(headerfields, mode)
        mapping = self.getMapping(path, headerfields, mode)
        reader = unicodecsv.DictReader(open(path, 'rb'))

        temp_dir = tempfile.mkdtemp()

        base = os.path.basename(path)
        (base, ext) = os.path.splitext(base)
        failed_path = os.path.join(temp_dir, "%s.pending%s" % (base, ext))
        failed_headers = mapping.values()
        failed_headers.append('--ERRORS--')
        failed_writer = unicodecsv.DictWriter(open(failed_path, 'wb'),
                                              failed_headers)
        os.chmod(failed_path, 0664)
        failed_writer.writerow(dict([(x,x) for x in failed_headers]))

        finished_path = os.path.join(temp_dir, "%s.finished%s" % (base, ext))
        finished_headers = mapping.values()
        finished_writer = unicodecsv.DictWriter(open(finished_path, 'wb'),
                                                finished_headers)
        os.chmod(finished_path, 0664)
        finished_writer.writerow(dict([(x,x) for x in finished_headers]))

        num =0
        num_warns = 0
        site = grok.getSite()

        for raw_row in reader:
            num += 1
            # Skip row if empty
            if self.emptyRow(raw_row):
                continue
            string_row = self.applyMapping(raw_row, mapping)
            if ignore_empty:
                # Replace empty strings and empty lists with ignore-markers
                for key, val in string_row.items():
                    if val == '' or val == '[]':
                        string_row[key] = IGNORE_MARKER
            row = dict(string_row.items()) # create deep copy
            errs, inv_errs, conv_dict = self.checkConversion(string_row, mode)
            if errs or inv_errs:
                num_warns += 1
                conv_warnings = self.stringFromErrs(errs, inv_errs)
                self.writeFailedRow(
                    failed_writer, string_row, conv_warnings)
                continue
            row.update(conv_dict)

            if mode == 'create':
                if not self.parentsExist(row, site):
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row,
                        "Not all parents do exist yet.")
                    continue
                if self.entryExists(row, site):
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row,
                        "This object already exists.")
                    continue
                parent = self.getParent(row, site)
                create_errors = self.checkCreateRequirements(parent, row, site)
                if create_errors is not None:
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row, create_errors)
                    continue
                obj = self.callFactory()
                # Override all values in row, also
                # student_ids and applicant_ids which have been
                # generated in the respective __init__ methods before.
                self.updateEntry(obj, row, site, base)
                try:
                    self.addEntry(obj, row, site)
                except KeyError, error:
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row, error.message)
                    continue
                except DuplicationError, error:
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row, error.msg)
                    continue
                except FatalCSVError, error:
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row, error.message)
                    continue
            elif mode == 'remove':
                if not self.entryExists(row, site):
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row,
                        "Cannot remove: no such entry")
                    continue
                obj = self.getEntry(row, site)
                remove_errors = self.checkRemoveRequirements(obj, row, site)
                if remove_errors is not None:
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row, remove_errors)
                    continue
                self.delEntry(row, site)
            elif mode == 'update':
                obj = self.getEntry(row, site)
                if obj is None:
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row,
                        "Cannot update: no such entry")
                    continue
                update_errors = self.checkUpdateRequirements(obj, row, site)
                if update_errors is not None:
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row, update_errors)
                    continue
                try:
                    self.updateEntry(obj, row, site, base)
                except ConstraintNotSatisfied, err:
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row,
                        "ConstraintNotSatisfied: %s" % err)
                    continue
                except RequiredMissing, err:
                    num_warns += 1
                    self.writeFailedRow(
                        failed_writer, string_row,
                        "RequiredMissing: %s" % err)
                    continue
            finished_writer.writerow(string_row)

        time_end = time.time()
        timedelta = time_end - time_start

        self.createLogfile(path, failed_path, num, num_warns, mode, user,
                           timedelta, logger=logger)
        failed_path = os.path.abspath(failed_path)
        if num_warns == 0:
            del failed_writer
            os.unlink(failed_path)
            failed_path = None
        return (num, num_warns,
                os.path.abspath(finished_path), failed_path)

    def get_csv_skeleton(self):
        """Export CSV file only with a header of available fields.

        A raw string with CSV data should be returned.
        """
        outfile = StringIO()
        writer = unicodecsv.DictWriter(outfile, self.available_fields)
        writer.writerow(
            dict(zip(self.available_fields, self.available_fields))) # header
        outfile.seek(0)
        return outfile.read()

class ExporterBase(object):
    """A base for exporters.
    """
    grok.implements(ICSVExporter)

    #: Fieldnames considered by this exporter
    fields = ('code', 'title', 'title_prefix')

    #: The title under which this exporter will be displayed
    #: (if registered as a utility)
    title = 'Override this title'

    def mangle_value(self, value, name, context=None):
        """Hook for mangling values in derived classes.
        """
        if isinstance(value, bool):
            value = value and '1' or '0'
        elif isinstance(value, unicode):
            # CSV writers like byte streams better than unicode
            value = value.encode('utf-8')
        elif isinstance(value, datetime.datetime):
            #value = str(value)
            value = str('%s#' % value) # changed 2014-07-06, see ticket #941
        elif isinstance(value, datetime.date):
            # Order is important here: check for date after datetime as
            # datetimes are also dates.
            #
            # Append hash '#' to dates to circumvent unwanted excel automatic
            value = str('%s#' % value)
        elif value is None:
            # None is not really representable in CSV files
            value = ''
        return value

    def get_csv_writer(self, filepath=None):
        """Get a CSV dict writer instance open for writing.

        Returns a tuple (<writer>, <outfile>) where ``<writer>`` is a
        :class:`csv.DictWriter` instance and outfile is the real file
        which is written to. The latter is important when writing to
        StringIO and can normally be ignored otherwise.

        The returned file will already be filled with the header row.

        Please note that if you give a filepath, the returned outfile
        is open for writing only and you might have to close it before
        reopening it for reading.
        """
        if filepath is None:
            outfile = StringIO()
        else:
            outfile = open(filepath, 'wb')
        writer = unicodecsv.DictWriter(outfile, self.fields)
        writer.writerow(dict(zip(self.fields, self.fields))) # header
        return writer, outfile

    def write_item(self, obj, writer):
        """Write a row extracted from `obj` into CSV file using `writer`.
        """
        row = {}
        for name in self.fields:
            value = getattr(obj, name, None)
            value = self.mangle_value(value, name, obj)
            row[name] = value
        writer.writerow(row)
        return

    def close_outfile(self, filepath, outfile):
        """Close outfile.
        If filepath is None, the contents of outfile is returned.
        """
        outfile.seek(0)
        if filepath is None:
            return outfile.read()
        outfile.close()
        return

    def get_filtered(self, site, **kw):
        """Get datasets to export filtered by keyword arguments.
        Returns an iterable.
        """
        raise NotImplementedError

    def get_selected(self, site, selected):
        """Get datasets to export for selected items
        specified by a list of identifiers.
        Returns an iterable.
        """
        raise NotImplementedError

    def export(self, iterable, filepath=None):
        """Export `iterable` as CSV file.
        If `filepath` is ``None``, a raw string with CSV data should
        be returned.
        """
        raise NotImplementedError

    def export_all(self, site, filepath=None):
        """Export all appropriate objects in `site` into `filepath` as
        CSV data.
        If `filepath` is ``None``, a raw string with CSV data should
        be returned.
        """
        raise NotImplementedError

    def export_filtered(self, site, filepath=None, **kw):
        """Export items denoted by `kw`.
        If `filepath` is ``None``, a raw string with CSV data should
        be returned.
        """
        data = self.get_filtered(site, **kw)
        return self.export(data, filepath=filepath)

    def export_selected(self, site, filepath=None, **kw):
        """Export those items specified by a list of identifiers
        called `selected`.
        If `filepath` is ``None``, a raw string with CSV data should
        be returned.
        """
        selected = kw.get('selected', [])
        data = self.get_selected(site, selected)
        return self.export(data, filepath=filepath)

def export_job(site, exporter_name, **kw):
    """Export all entries delivered by exporter and store it in a temp file.

    `site` gives the site to search. It will be passed to the exporter
    and also be set as 'current site' as the function is used in
    asynchronous jobs which run in their own threads and have no site
    set initially. Therefore `site` must also be a valid value for use
    with `zope.component.hooks.setSite()`.

    `exporter_name` is the utility name under which the desired
    exporter was registered with the ZCA.

    The resulting CSV file will be stored in a new temporary directory
    (using :func:`tempfile.mkdtemp`). It will be named after the
    exporter used with `.csv` filename extension.

    Returns the path to the created CSV file.

    .. note:: It is the callers responsibility to clean up the used
              file and its parent directory.
    """
    setSite(site)
    exporter = getUtility(ICSVExporter, name=exporter_name)
    output_dir = tempfile.mkdtemp()
    filename = '%s.csv' % exporter_name
    output_path = os.path.join(output_dir, filename)
    if kw == {}:
        exporter.export_all(site, filepath=output_path)
    elif kw.has_key('selected'):
        exporter.export_selected(site, filepath=output_path, **kw)
    else:
        exporter.export_filtered(site, filepath=output_path, **kw)
    return output_path

class AsyncExportJob(AsyncJob):
    """An IJob that exports data to CSV files.

    `AsyncExportJob` instances are regular `AsyncJob` instances with a
    different constructor API. Instead of a callable to execute, you
    must pass a `site` and some `exporter_name` to trigger an export.

    The real work is done when an instance of this class is put into a
    queue. See :mod:`waeup.kofa.async` to learn more about
    asynchronous jobs.

    The `exporter_name` must be the name under which an ICSVExporter
    utility was registered with the ZCA.

    The `site` must be a valid site  or ``None``.

    The result of an `AsyncExportJob` is the path to generated CSV
    file. The file will reside in a temporary directory that should be
    removed after being used.
    """
    grok.implements(IExportJob)

    def __init__(self, site, exporter_name, *args, **kwargs):
        super(AsyncExportJob, self).__init__(
            export_job, site, exporter_name, *args, **kwargs)

    @property
    def finished(self):
        """A job is marked `finished` if it is completed.

        Please note: a finished report job does not neccessarily
        provide an IReport result. See meth:`failed`.
        """
        return self.status == zc.async.interfaces.COMPLETED

    @property
    def failed(self):
        """A report job is marked failed iff it is finished and the
        result is None.

        While a job is unfinished, the `failed` status is ``None``.

        Failed jobs normally provide a `traceback` to examine reasons.
        """
        if not self.finished:
            return None
        if getattr(self, 'result', None) is None:
            return True
        return False

class ExportJobContainer(object):
    """A mix-in that provides functionality for asynchronous export jobs.
    """
    grok.implements(IExportJobContainer)
    running_exports = PersistentList()

    def start_export_job(self, exporter_name, user_id, *args, **kwargs):
        """Start asynchronous export job.

        `exporter_name` is the name of an exporter utility to be used.

        `user_id` is the ID of the user that triggers the export.

        The job_id is stored along with exporter name and user id in a
        persistent list.

        The method supports additional positional and keyword
        arguments, which are passed as-is to the respective
        :class:`AsyncExportJob`.

        Returns the job ID of the job started.
        """
        site = grok.getSite()
        manager = getUtility(IJobManager)
        job = AsyncExportJob(site, exporter_name, *args, **kwargs)
        job_id = manager.put(job)
        # Make sure that the persisted list is stored in ZODB
        self.running_exports = PersistentList(self.running_exports)
        self.running_exports.append((job_id, exporter_name, user_id))
        return job_id

    def get_running_export_jobs(self, user_id=None):
        """Get export jobs for user with `user_id` as list of tuples.

        Each tuples holds ``<job_id>, <exporter_name>, <user_id>`` in
        that order. The ``<exporter_name>`` is the utility name of the
        used exporter.

        If `user_id` is ``None``, all running jobs are returned.
        """
        entries = []
        to_delete = []
        manager = getUtility(IJobManager)
        for entry in self.running_exports:
            if user_id is not None and entry[2] != user_id:
                continue
            if manager.get(entry[0]) is None:
                to_delete.append(entry)
                continue
            entries.append(entry)
        if to_delete:
            self.running_exports = PersistentList(
                [x for x in self.running_exports if x not in to_delete])
        return entries

    def get_export_jobs_status(self, user_id=None):
        """Get running/completed export jobs for `user_id` as list of tuples.

        Each tuple holds ``<raw status>, <status translated>,
        <exporter title>`` in that order, where ``<status
        translated>`` and ``<exporter title>`` are translated strings
        representing the status of the job and the human readable
        title of the exporter used.
        """
        entries = self.get_running_export_jobs(user_id)
        result = []
        manager = getUtility(IJobManager)
        for entry in entries:
            job = manager.get(entry[0])
            if job is None:
                continue
            status, status_translated = JOB_STATUS_MAP[job.status]
            exporter_name = getUtility(ICSVExporter, name=entry[1]).title
            result.append((status, status_translated, exporter_name))
        return result

    def delete_export_entry(self, entry):
        """Delete the export denoted by `entry`.

        Removes given entry from the local `running_exports` list and also
        removes the regarding job via the local job manager.

        `entry` must be a tuple ``(<job id>, <exporter name>, <user
        id>)`` as created by :meth:`start_export_job` or returned by
        :meth:`get_running_export_jobs`.
        """
        manager = getUtility(IJobManager)
        job = manager.get(entry[0])
        if job is not None:
            # remove created export file
            if isinstance(job.result, basestring):
                if os.path.exists(os.path.dirname(job.result)):
                    shutil.rmtree(os.path.dirname(job.result))
        manager.remove(entry[0], self)
        new_entries = [x for x in self.running_exports
                       if x != entry]
        self.running_exports = PersistentList(new_entries)
        return

    def entry_from_job_id(self, job_id):
        """Get entry tuple for `job_id`.

        Returns ``None`` if no such entry can be found.
        """
        for entry in self.running_exports:
            if entry[0] == job_id:
                return entry
        return None

class VirtualExportJobContainer(ExportJobContainer):
    """A virtual export job container.

    Virtual ExportJobContainers can be used as a mixin just like real
    ExportJobContainer.

    They retrieve and store data in the site-wide ExportJobContainer.

    Functionality is currently entirely as for regular
    ExportJobContainers, except that data is stored elsewhere.

    VirtualExportJobContainers need a registered
    IExportContainerFinder utility to find a suitable container for
    storing data.
    """
    grok.implements(IExportJobContainer)

    @property
    def _site_container(self):
        return getUtility(IExportContainerFinder)()

    # The following is a simple trick. While ExportJobContainers store
    # only one attribute in ZODB, it is sufficient to replace this
    # attribute `running_exports` with a suitable manager to make the
    # whole virtual container work like the original but with the data
    # stored in the site-wide exports container. This way, virtual
    # export containers provide the whole functionality of a regular
    # exports container but store no data at all with themselves.
    @property
    def running_exports(self):
        """Exports stored in the site-wide exports container.
        """
        return self._site_container.running_exports

    @running_exports.setter
    def running_exports(self, value):
        self._site_container.running_exports = value

    @running_exports.deleter
    def running_exports(self):
        del self._site_container.running_exports

    @property
    def logger(self):
        return self._site_container.logger

@implementer(IExportContainerFinder)
class ExportContainerFinder(grok.GlobalUtility):
    """Finder for local (site-wide) export container.
    """

    def __call__(self):
        """Get the local export container-

        If no site can be determined or the site provides no export
        container, None is returned.
        """
        site = grok.getSite()
        if site is None:
            return None
        return site.get('datacenter', None)
