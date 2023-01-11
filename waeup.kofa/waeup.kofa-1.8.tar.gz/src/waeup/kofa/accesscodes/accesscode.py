## $Id: accesscode.py 13304 2015-10-08 14:40:37Z henrik $
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
"""Components to handle access codes.

Access codes (aka PINs) in waeup sites are organized in batches. That
means a certain accesscode must be part of a batch. As a site (or
university) can hold an arbitrary number of batches, we also provide a
batch container. Each university has one batch container that holds
all access code batches of which each one can hold several thousands
of access codes.
"""
import unicodecsv as csv # XXX: csv ops should move to dedicated module.
import grok
import os
from datetime import datetime
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from random import SystemRandom as random
from zope.component import getUtility
from zope.component.interfaces import IFactory
from waeup.kofa.interfaces import IKofaUtils, IKofaPluggable, IObjectHistory
from waeup.kofa.utils.helpers import now
from waeup.kofa.utils.logger import Logger
from waeup.kofa.accesscodes.interfaces import (
    IAccessCode, IAccessCodeBatch, IAccessCodeBatchContainer
    )
from waeup.kofa.accesscodes.workflow import DISABLED, USED, ac_states_dict

class AccessCode(grok.Model):
    """An access code (aka PIN).

    Implements
    :class:`waeup.kofa.accesscodes.interfaces.IAccessCode`. :class:`AccessCode`
    instances are normally part of an :class:`AccessCodeBatch` so
    their representation (or code) is built with the containing batch
    involved.

    `batch_serial`
       the serial number of the new :class:`AccessCode` inside its batch.

    `random_num`
       a 10-digit number representing the main part of the code.

    :class:`AccessCode` instances normally have a representation (or
    code) like

      ``APP-XXX-YYYYYYYYYY``

    where ``APP`` is the prefix of the containing batch, ``XXX`` is
    the batch number and ``YYYYYYYYYY`` is the real code. The complete
    PIN is portal-wide unique.

    Access code instances are far more than simple strings. They have
    a state, a history (so that all changes can be tracked) and a
    cost (given as a float number).

    The state of an access code is something like 'used', 'disabled',
    etc. and determined by the workflow defined in
    :mod:`waeup.kofa.accesscodes.workflow`. This also means that
    instead of setting the status of an access code directly (you
    can't do that easily, and yes, that's intentionally), you have to
    trigger a transition (that might fail, if the transition is not
    allowed in terms of logic or permissions). See
    :mod:`waeup.kofa.accesscodes.workflow` for details.

    """
    grok.implements(IAccessCode)

    def __init__(self, batch_serial=None, random_num=None):
        super(AccessCode, self).__init__()
        self.batch_serial = batch_serial
        self.random_num = random_num
        self.owner = None
        self.cost = None
        IWorkflowInfo(self).fireTransition('init')

    @property
    def representation(self):
        """A string representation of the :class:`AccessCode`.

        It has format ``APP-XXX-YYYYYYYYYY`` as described above.
        """
        return '%s-%s-%s' % (
            self.batch_prefix, self.batch_num, self.random_num)

    @property
    def batch(self):
        """The batch this :class:`AccessCode` is contained.
        """
        return getattr(self, '__parent__', None)

    @property
    def batch_prefix(self):
        """The prefix of the batch this :class:`AccessCode` belongs to.
        """
        if self.batch is None:
            return ''
        return self.batch.prefix

    @property
    def batch_num(self):
        """The number of the batch this :class:`AccessCode` belongs to. A
        read-only attribute.
        """
        if self.batch is None:
            return ''
        return self.batch.num

    #@property
    #def cost(self):
    #    """A float representing the price or ``None``. A read-only attribute.
    #    """
    #    if self.batch is None:
    #        return None
    #    return self.batch.cost

    @property
    def state(self):
        """The workflow state. A read-only attribute.
        """
        return IWorkflowState(self).getState()

    @property
    def translated_state(self):
        """The translated workflow state. A read-only attribute.
        """
        return ac_states_dict[self.state]

    @property
    def history(self):
        """A :class:`waeup.kofa.objecthistory.ObjectHistory` instance.
        """
        history = IObjectHistory(self)
        return '||'.join(history.messages)

class AccessCodeBatch(grok.Container):
    """A batch of access codes.
    """
    grok.implements(IAccessCodeBatch)

    def __init__(self, creation_date=None, creator=None, batch_prefix=None,
                 cost=None, entry_num=0, num=None):
        super(AccessCodeBatch, self).__init__()
        self.creation_date = creation_date
        self.creator = creator
        try:
            self.prefix = batch_prefix.upper()
        except AttributeError:
            self.prefix = None
        self.cost = cost
        self.entry_num = entry_num
        self.num = num
        self.used_num = 0
        self.disabled_num = 0

    def _createEntries(self):
        """Create the entries for this batch.
        """
        for num, pin in enumerate(self.getNewRandomNum(num=self.entry_num)):
            self.addAccessCode(num, pin, self.cost)
        return

    def getNewRandomNum(self, num=1):
        """Create a set of ``num`` random numbers of 10 digits each.

        The number is returned as string.
        """
        curr = 1
        while curr <= num:
            pin = ''
            for x in range(10):
                pin += str(random().randint(0, 9))
            if not '%s-%s-%s' % (self.prefix, self.num, pin) in self.keys():
                curr += 1
                yield pin
            # PIN already in use

    def _getStoragePath(self):
        """Get the directory, where we store all batch-related CSV files.
        """
        site = grok.getSite()
        storagepath = site['datacenter'].storage
        ac_storage = os.path.join(storagepath, 'accesscodes')
        if not os.path.exists(ac_storage):
            os.mkdir(ac_storage)
        return ac_storage

    def getAccessCode(self, ac_id):
        """Get the AccessCode with ID ``ac_id`` or ``KeyError``.
        """
        return self[ac_id]

    def addAccessCode(self, num, pin, cost=0.0, owner=None):
        """Add an access-code.
        """
        ac = AccessCode(num, pin)
        if owner:
            ac.owner = owner
        ac.cost = cost
        ac.__parent__ = self
        self[ac.representation] = ac
        return

    def createCSVLogFile(self):
        """Create a CSV file with data in batch.

        Data will not contain invalidation date nor student ids.  File
        will be created in ``accesscodes`` subdir of data center
        storage path.

        Returns name of created file.
        """
        date = self.creation_date.strftime('%Y_%m_%d_%H_%M_%S')
        ac_storage = self._getStoragePath()
        csv_path = os.path.join(
            ac_storage, '%s-%s-%s-%s.csv' % (
                self.prefix, self.num, date, self.creator)
            )
        writer = csv.writer(open(csv_path, 'w'), quoting=csv.QUOTE_ALL)
        writer.writerow(['serial', 'ac', 'cost'])
        writer.writerow([self.prefix, str(self.num), "%0.2f" % self.cost])

        for value in sorted(self.values(),
                            cmp=lambda x, y: cmp(
                x.batch_serial, y.batch_serial)):
            writer.writerow(
                [str(value.batch_serial), str(value.representation)]
                )
        site = grok.getSite()
        logger = site.logger
        logger.info(
            "Created batch %s-%s" % (self.prefix, self.num))
        logger.info(
            "Written batch CSV to %s" % csv_path)
        return os.path.basename(csv_path)

    def archive(self):
        """Create a CSV file for archive.
        """
        ac_storage = self._getStoragePath()
        tz = getUtility(IKofaUtils).tzinfo
        dt_now = now(tz)
        timestamp = dt_now.strftime('%Y_%m_%d_%H_%M_%S')
        csv_path = os.path.join(
            ac_storage, '%s-%s_archive-%s-%s.csv' % (
                self.prefix, self.num, timestamp, self.creator)
            )
        writer = csv.writer(open(csv_path, 'w'), quoting=csv.QUOTE_ALL)
        writer.writerow(['prefix', 'serial', 'ac', 'state', 'history',
            'cost','owner'])
        writer.writerow([self.prefix, '%0.2f' % self.cost, str(self.num),
                         str(self.entry_num)])
        for value in sorted(
            self.values(),
            cmp = lambda x, y: cmp(x.batch_serial, y.batch_serial)
            ):
            writer.writerow([
                    self.prefix, value.batch_serial, value.representation,
                    value.state, value.history, value.cost, value.owner
                    ])
        return os.path.basename(csv_path)

@grok.subscribe(IAccessCodeBatch, grok.IObjectAddedEvent)
def handle_batch_added(batch, event):
    # A (maybe dirty?) workaround to make batch containers work
    # without self-maintained acids: as batches should contain their
    # set of data immediately after creation, but we cannot add
    # subobjects as long as the batch was not added already to the
    # ZODB, we trigger the item creation for the time after the batch
    # was added to the ZODB.
    batch._createEntries()
    return


class AccessCodeBatchContainer(grok.Container, Logger):
    grok.implements(IAccessCodeBatchContainer)

    def _getStoragePath(self):
        """Get the directory, where batch import files are stored.

        If the path does not exist yet, it is created. The path is
        normally ``accesscodes/imports`` below the datacenter storage
        path (see :data:`waeup.kofa.accesscodes.Datacenter.storage`).
        """
        site = grok.getSite()
        storagepath = site['datacenter'].storage
        ac_storage = os.path.join(storagepath, 'accesscodes')
        import_path = os.path.join(ac_storage, 'imports')
        for path in [ac_storage, import_path]:
            if not os.path.exists(path):
                os.mkdir(path)
                site.logger.info('created path %s' % path)
        return import_path

    def addBatch(self, batch):
        """Add an already created `batch`.
        """
        batch.num = self.getNum(batch.prefix)
        key = "%s-%s" % (batch.prefix, batch.num)
        self[key] = batch
        self._p_changed = True
        return

    def addBatchByImport(self, batch, batch_id):
        """Add an already created `batch` by import with defined id.

        We want to create a batch without access codes. Since num_entry
        access codes are automatically added by handle_batch_added when
        the batch is added to the ZODB, we have to temporarily set entry_num
        to zero when adding the batch persistently.
        """
        orig_entry_num = batch.entry_num
        batch.entry_num = 0
        self[batch_id] = batch
        self._p_changed = True
        batch.entry_num = orig_entry_num
        return

    def createBatch(self, creation_date, creator, prefix, cost,
                    entry_num):
        """Create and add a batch.
        """
        batch_num = self.getNum(prefix)
        batch = AccessCodeBatch(creation_date, creator, prefix,
                                cost, entry_num, num=batch_num)
        self.addBatch(batch)
        return batch

    def getNum(self, prefix):
        """Get next unused num for given prefix.
        """
        # School fee, clearance, hostel application and transcript 
        # batches start with 0.These batches are being emptily 
        # created during initialization of the university instance.
        if prefix in ('CLR', 'SFE', 'HOS', 'TSC'):
            num = 0
        else:
            num = 1
        while self.get('%s-%s' % (prefix, num), None) is not None:
            num += 1
        return num

    def getImportFiles(self):
        """Return a generator with basenames of available import files.
        """
        path = self._getStoragePath()
        for filename in sorted(os.listdir(path)):
            yield filename

    # This is temporary reimport solution. Access codes will be imported
    # with state initialized no matter if they have been used before.
    def reimport(self, filename, creator=u'UNKNOWN'):
        """Reimport a batch given in CSV file.

        CSV file must be of format as generated by createCSVLogFile
        method.
        """
        path = os.path.join(self._getStoragePath(), filename)
        reader = csv.DictReader(open(path, 'rb'), quoting=csv.QUOTE_ALL)
        entry = reader.next()
        cost = float(entry['serial'])
        num = int(entry['ac'])
        prefix = entry['prefix']
        batch_name = '%s-%s' % (prefix, num)
        if batch_name in self.keys():
            raise KeyError('Batch already exists: %s' % batch_name)
        batch = AccessCodeBatch(
            datetime.utcnow(), creator, prefix, cost, 0, num=num)
        num_entries = 0
        self[batch_name] = batch
        for row in reader:
            pin = row['ac']
            serial = int(row['serial'])
            try:
                cost = float(row['cost'])
            except ValueError:
                cost = 0.0
            rand_num = pin.rsplit('-', 1)[-1]
            batch.addAccessCode(serial, rand_num, cost)
            num_entries += 1
        batch.entry_num = num_entries
        batch.createCSVLogFile()
        return

    def getAccessCode(self, ac_id):
        """Get the AccessCode with ID ``ac_id`` or ``KeyError``.
        """
        for batchname in self.keys():
            batch = self[batchname]
            try:
                return batch.getAccessCode(ac_id)
            except KeyError:
                continue
        return None

    def disable(self, ac_id, comment=None):
        """Disable the AC with ID ``ac_id``.

        ``user_id`` is the user ID of the user triggering the
        process. Already disabled ACs are left untouched.
        """
        ac = self.getAccessCode(ac_id)
        if ac is None:
            return
        disable_accesscode(ac_id, comment)
        return

    def enable(self, ac_id, comment=None):
        """(Re-)enable the AC with ID ``ac_id``.

        This leaves the given AC in state ``unused``. Already enabled
        ACs are left untouched.
        """
        ac = self.getAccessCode(ac_id)
        if ac is None:
            return
        reenable_accesscode(ac_id, comment)
        return

    logger_name = 'waeup.kofa.${sitename}.accesscodes'
    logger_filename = 'accesscodes.log'

    def logger_info(self, ob_class, comment=None):
        """Get the logger's info method.
        """
        self.logger.info('%s - %s' % (
                ob_class, comment))
        return

class AccessCodePlugin(grok.GlobalUtility):
    grok.name('accesscodes')
    grok.implements(IKofaPluggable)

    def setup(self, site, name, logger):
        basecontainer = AccessCodeBatchContainer()
        site['accesscodes'] = basecontainer
        logger.info('Installed container for access code batches.')
        # Create empty school fee, clearance, hostel application
        # and transcript AC
        # batches during initialization of university instance.
        cost = 0.0
        creator = 'system'
        entry_num = 0
        creation_date = datetime.utcnow()
        basecontainer.createBatch(creation_date, creator,
            'SFE', cost, entry_num)
        basecontainer.createBatch(creation_date, creator,
            'CLR', cost, entry_num)
        basecontainer.createBatch(creation_date, creator,
            'HOS', cost, entry_num)
        basecontainer.createBatch(creation_date, creator,
            'TSC', cost, entry_num)
        logger.info('Installed empty SFE, CLR, HOS and TSC access code batches.')
        return

    def update(self, site, name, logger):
        site_name = getattr(site, '__name__', '<Unnamed Site>')
        if not 'accesscodes' in site.keys():
            logger.info('Updating site at %s. Installing access codes.' % (
                    site,))
            self.setup(site, name, logger)
        else:
            logger.info(
                'AccessCodePlugin: Updating site at %s: Nothing to do.' % (
                    site_name, ))
        return

class AccessCodeBatchFactory(grok.GlobalUtility):
    """A factory for accesscodebatches.

    We need this factory for the accesscodebatchprocessor.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.AccessCodeBatch')
    title = u"Create a new accesscode batch.",
    description = u"This factory instantiates new accesscode batch instances."

    def __call__(self, *args, **kw):
        return AccessCodeBatch()

    def getInterfaces(self):
        return implementedBy(AccessCodeBatch)

class AccessCodeFactory(grok.GlobalUtility):
    """A factory for accesscodes.

    We need this factory for the accesscodeprocessor.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.AccessCode')
    title = u"Create a new accesscode.",
    description = u"This factory instantiates new accesscode instances."

    def __call__(self, *args, **kw):
        return AccessCode(*args, **kw)

    def getInterfaces(self):
        return implementedBy(AccessCode)

def get_access_code(access_code):
    """Get an access code instance.

    An access code here is a string like ``PUDE-1-1234567890``.

    Returns ``None`` if the given code cannot be found.

    This is a convenicence function that is faster than looking up a
    batch container for the approriate access code.
    """
    site = grok.getSite()
    if not isinstance(access_code, basestring):
        return None
    try:
        batch_id, ac_id = access_code.rsplit('-', 1)
    except:
        return None
    batch = site['accesscodes'].get(batch_id, None)
    if batch is None:
        return None
    try:
        code = batch.getAccessCode(access_code)
    except KeyError:
        return None
    return code

def fire_transition(access_code, arg, toward=False, comment=None, owner=None):
    """Fire workflow transition for access code.

    The access code instance is looked up via `access_code` (a string
    like ``APP-1-12345678``).

    `arg` tells what kind of transition to trigger. This will be a
    transition id like ``'use'`` or ``'init'``, or some transition
    target like :data:`waeup.kofa.accesscodes.workflow.INITIALIZED`.

    If `toward` is ``False`` (the default) you have to pass a
    transition id as `arg`, otherwise you must give a transition
    target.

    If `comment` is specified (default is ``None``) the given string
    will be passed along as transition comment. It will appear in the
    history of the changed access code. You can use this to place
    remarks like for which object the access code was used or similar.

    If `owner` is specified, the owner attribute of the access code is checked.
    If the access code has an owner but is different, :func:`fire_transition`
    fails and returns False.

    :func:`fire_transition` might raise exceptions depending on the
    reason why the requested transition cannot be performed.

    The following exceptions can occur during processing:

    :exc:`KeyError`:
      signals not existent access code, batch or site.

    :exc:`ValueError`:
      signals illegal format of `access_code` string. The regular format is
      ``APP-N-XXXXXXXX``.

    :exc:`hurry.workflow.interfaces.InvalidTransitionError`:
      the transition requested cannot be performed because the workflow
      rules forbid it.

    :exc:`Unauthorized`:
      the current user is not allowed to perform the requested transition.

    """
    try:
        batch_id, ac_id = access_code.rsplit('-', 1)
    except ValueError:
        raise ValueError(
            'Invalid access code format: %s (use: APP-N-XXXXXXXX)' % (
                access_code,))
    try:
        ac = grok.getSite()['accesscodes'][batch_id].getAccessCode(access_code)
    except TypeError:
        raise KeyError(
            'No site available for looking up accesscodes')
    if owner:
        ac_owner = getattr(ac, 'owner', None)
        if ac_owner and ac_owner != owner:
            return False
    info = IWorkflowInfo(ac)
    if toward:
        info.fireTransitionToward(arg, comment=comment)
    else:
        info.fireTransition(arg, comment=comment)
    return True

def invalidate_accesscode(access_code, comment=None, owner=None):
    """Invalidate AccessCode denoted by string ``access_code``.

    Fires an appropriate transition to perform the task.

    `comment` is a string that will appear in the access code
    history.

    See :func:`fire_transition` for possible exceptions and their
    meanings.
    """
    try:
        return fire_transition(access_code, 'use', comment=comment, owner=owner)
    except:
        return False

def disable_accesscode(access_code, comment=None):
    """Disable AccessCode denoted by string ``access_code``.

    Fires an appropriate transition to perform the task.

    `comment` is a string that will appear in the access code
    history.

    See :func:`fire_transition` for possible exceptions and their
    meanings.
    """
    return fire_transition(
        access_code, DISABLED, toward=True, comment=comment)

def reenable_accesscode(access_code, comment=None):
    """Reenable AccessCode denoted by string ``access_code``.

    Fires an appropriate transition to perform the task.

    `comment` is a string that will appear in the access code
    history.

    See :func:`fire_transition` for possible exceptions and their
    meanings.
    """
    return fire_transition(access_code, 'reenable', comment=comment)

def create_accesscode(batch_prefix, batch_num, cost, owner):
    """
    """
    batch_id = '%s-%s' % (batch_prefix, batch_num)
    try:
        batch = grok.getSite()['accesscodes'][batch_id]
    except KeyError:
        return None, u'No AC batch available.'
    rand_num = list(batch.getNewRandomNum())[0]
    num = len(batch) + 1
    batch.addAccessCode(num, rand_num, cost, owner)
    batch.entry_num += 1
    pin = u'%s-%s-%s' % (batch_prefix,batch_num,rand_num)
    return pin, None
