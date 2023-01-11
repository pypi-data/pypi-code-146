## $Id: batching.py 12883 2015-04-25 06:13:18Z henrik $
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
"""Batch processing components for accesscodes.

"""
import grok
from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo
from zope.interface import Interface
from waeup.kofa.interfaces import (
    IBatchProcessor, IGNORE_MARKER, IObjectHistory, IObjectConverter)
from waeup.kofa.utils.batching import BatchProcessor
from waeup.kofa.accesscodes.interfaces import IAccessCodeBatch, IAccessCode
from waeup.kofa.accesscodes.workflow import INITIALIZED, USED, DISABLED

IMPORTABLE_TRANSITIONS = (
    'init', 'use', 'disable_used', 'disable_unused', 'reeanble')

IMPORTABLE_STATES = (INITIALIZED, USED, DISABLED)

class AccessCodeBatchProcessor(BatchProcessor):
    """The Access Code Batch Processor imports containers for access codes.
    It does not import their content. There is nothing special about this
    processor.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'accesscodebatchprocessor'
    grok.name(util_name)

    name = u'AccessCodeBatch Processor'
    iface = IAccessCodeBatch

    location_fields = ['batch_id',]
    factory_name = 'waeup.AccessCodeBatch'

    mode = None

    def parentsExist(self, row, site):
        return 'accesscodes' in site.keys()

    def entryExists(self, row, site):
        return row['batch_id'] in site['accesscodes'].keys()

    def getParent(self, row, site):
        return site['accesscodes']

    def getEntry(self, row, site):
        if not self.entryExists(row, site):
            return None
        parent = self.getParent(row, site)
        return parent.get(row['batch_id'])

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        parent.addBatchByImport(obj, row['batch_id'])
        return

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.

        Returns a string describing the fields changed.
        """
        items_changed = super(AccessCodeBatchProcessor, self).updateEntry(
            obj, row, site, filename)
        # Log actions...
        location_field = self.location_fields[0]
        grok.getSite()['accesscodes'].logger.info(
            '%s - %s - %s - updated: %s'
            % (self.name, filename, row[location_field], items_changed))
        return

class AccessCodeProcessor(BatchProcessor):
    """The Access Code Processor imports access codes (ac) into their
    batches. Localization requires the `representation` of the ac
    (object id) as well as  `batch_prefix` and `batch_num` to find
    the parent container (the batch).

    Access codes follow a workflow. The `checkConversion` method validates
    the workflow `state` and `transition` in row. `checkUpdateRequirements`
    checks if the transition is allowed. This depends on the context.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'accesscodeprocessor'
    grok.name(util_name)

    name = u'AccessCode Processor'
    iface = IAccessCode

    location_fields = ['representation', 'batch_prefix', 'batch_num']
    factory_name = 'waeup.AccessCode'

    mode = None

    @property
    def available_fields(self):
        return sorted(list(set(
                    self.location_fields + [
                        'random_num', 'owner', 'cost',
                        'state', 'transition', 'batch_serial',]
                    )))

    @property
    def required_fields(self):
        return ['random_num', 'batch_serial', 'history',]

    def parentsExist(self, row, site):
        return self.getParent(row,site) is not None

    def entryExists(self, row, site):
        parent = self.getParent(row, site)
        if parent is None:
            return False
        return row['representation'] in parent.keys()

    def getParent(self, row, site):
        if not 'accesscodes' in site.keys():
            return None
        batch_id = '%s-%s' % (row['batch_prefix'], row['batch_num'])
        return site['accesscodes'].get(batch_id, None)

    def getEntry(self, row, site):
        if not self.entryExists(row, site):
            return None
        parent = self.getParent(row, site)
        return parent.get(row['representation'], None)

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        parent[row['representation']] = obj
        return

    def checkConversion(self, row, mode='create'):
        """Validates all values in row.
        """
        converter = IObjectConverter(self.iface)
        errs, inv_errs, conv_dict =  converter.fromStringDict(
            row, self.factory_name, mode=mode)
        if 'transition' in row and 'state' in row:
            if row['transition'] not in (IGNORE_MARKER, '') and \
                row['state'] not in (IGNORE_MARKER, ''):
                errs.append(('workflow','not allowed'))
                return errs, inv_errs, conv_dict
        if 'transition' in row:
            if row['transition'] not in IMPORTABLE_TRANSITIONS:
                if row['transition'] not in (IGNORE_MARKER, ''):
                    errs.append(('transition','not allowed'))
        if 'state' in row:
            if row['state'] not in IMPORTABLE_STATES:
                if row['state'] not in (IGNORE_MARKER, ''):
                    errs.append(('state','not allowed'))
                else:
                    # State is an attribute of AccessCode and must not
                    # be changed if empty.
                    conv_dict['state'] = IGNORE_MARKER
        return errs, inv_errs, conv_dict

    def checkUpdateRequirements(self, obj, row, site):
        """Checks requirements the object must fulfill when being updated.

        This method is not used in case of deleting or adding objects.

        Returns error messages as strings in case of requirement
        problems.
        """
        transition = row.get('transition', IGNORE_MARKER)
        if transition not in (IGNORE_MARKER, ''):
            allowed_transitions = IWorkflowInfo(obj).getManualTransitionIds()
            if transition not in allowed_transitions:
                return 'Transition not allowed.'
        return None

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.

        Returns a string describing the fields changed.
        """
        items_changed = ''
        # Update state
        # Attention: When importing states the counters remain unchanged.
        if 'state' in row:
            state = row.get('state', IGNORE_MARKER)
            if state not in (IGNORE_MARKER, ''):
                value = row['state']
                IWorkflowState(obj).setState(value)
                items_changed += ('%s=%s, ' % ('state', state))
                msg = "state '%s' set" % state
                IObjectHistory(obj).addMessage(msg)
            row.pop('state')
        # Trigger transition. Counters are properly changed.
        if 'transition' in row:
            transition = row.get('transition', IGNORE_MARKER)
            if transition not in (IGNORE_MARKER, ''):
                value = row['transition']
                IWorkflowInfo(obj).fireTransition(value)
                items_changed += ('%s=%s, ' % ('transition', transition))
            row.pop('transition')

        # In import files we can use the hash symbol at the end of a
        # random_num string to avoid annoying automatic number transformation
        # by Excel or Calc
        if 'random_num' in row:
            random_num = row.get('random_num', IGNORE_MARKER)
            if random_num not in (IGNORE_MARKER, ''):
                row['random_num'] = random_num.strip('#')

        items_changed += super(AccessCodeProcessor, self).updateEntry(
            obj, row, site, filename)

        # Log actions...
        grok.getSite()['accesscodes'].logger.info(
            '%s - %s - %s - updated: %s'
            % (self.name, filename, row['representation'], items_changed))
        return
