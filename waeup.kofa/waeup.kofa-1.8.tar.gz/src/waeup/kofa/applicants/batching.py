## $Id: batching.py 16472 2021-04-21 14:35:48Z henrik $
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
"""Batch processing for applicants.
"""
import unicodecsv as csv # XXX: csv ops should move to dedicated module.
import grok
from time import time
import unicodecsv
from zope.schema import getFields
from zope.interface import Interface
from zope.component import queryUtility, getUtility
from hurry.workflow.interfaces import IWorkflowState
from zope.catalog.interfaces import ICatalog
from waeup.kofa.interfaces import (
    IBatchProcessor, IObjectConverter, FatalCSVError,
    IGNORE_MARKER, DELETION_MARKER,
    IObjectHistory, IUserAccount, DuplicationError)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.payments.interfaces import IPayer
from waeup.kofa.utils.batching import BatchProcessor
from waeup.kofa.applicants.interfaces import (
    IApplicantsContainer, IApplicant, IApplicantUpdateByRegNo,
    IApplicantOnlinePayment)
from waeup.kofa.applicants.workflow import  IMPORTABLE_STATES, CREATED

class ApplicantsContainerProcessor(BatchProcessor):
    """The Applicants Container Processor imports containers for applicants.
    It does not import their content. There is nothing special about this
    processor.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'applicantscontainerprocessor'
    grok.name(util_name)

    name = _('ApplicantsContainer Processor')
    mode = u'create'
    iface = IApplicantsContainer

    location_fields = ['code',]
    factory_name = 'waeup.ApplicantsContainer'

    def parentsExist(self, row, site):
        return 'applicants' in site.keys()

    def entryExists(self, row, site):
        return row['code'] in site['applicants'].keys()

    def getParent(self, row, site):
        return site['applicants']

    def getEntry(self, row, site):
        if not self.entryExists(row, site):
            return None
        parent = self.getParent(row, site)
        return parent.get(row['code'])

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        parent[row['code']] = obj
        return

    def delEntry(self, row, site):
        parent = self.getParent(row, site)
        del parent[row['code']]
        return

class ApplicantProcessor(BatchProcessor):
    """The Applicant Processor imports application data (applicants).

    In create mode `container_code` is required. If `application_number` is
    given, an applicant with this number is created in the designated container.
    If `application_number` is not given, a random `application_number` is
    assigned. `applicant_id` is being determined by the system and can't be
    imported.

    In update or remove mode `container_code` and `application_number` columns
    must not exist. The applicant object is solely localized by searching
    the applicants catalog for `reg_number` or `applicant_id` .
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'applicantprocessor'
    grok.name(util_name)
    name = _('Applicant Processor')
    iface = IApplicant
    iface_byregnumber = IApplicantUpdateByRegNo
    factory_name = 'waeup.Applicant'

    mode = None

    @property
    def available_fields(self):
        return sorted(list(set(
            ['application_number',
            'container_code','state','password'] + getFields(
                self.iface).keys())))

    def checkHeaders(self, headerfields, mode='create'):
        cond1 = 'container_code' in headerfields
        cond2 = 'application_number' in headerfields
        cond3 = 'applicant_id' in headerfields
        cond4 = 'reg_number' in headerfields
        if mode == 'create':
            if not cond1:
                raise FatalCSVError(
                    "Need at least container_code column!")
            if cond3:
                raise FatalCSVError(
                    "applicant_id can't be imported in create mode!")
            for field in self.required_fields:
                if not field in headerfields:
                    raise FatalCSVError(
                        "Need at least columns %s for import!" %
                        ', '.join(["'%s'" % x for x in self.required_fields]))
        if mode in ('update', 'remove'):
            if not cond3 and not cond4:
                raise FatalCSVError(
                    "Need at least column reg_number or applicant_id!")
            if cond1 or cond2:
                raise FatalCSVError(
                    "container_code or application_number can't be imported " +
                    "in update or remove mode!")
        # Check for fields to be ignored...
        not_ignored_fields = [x for x in headerfields
                              if not x.startswith('--')]
        if len(set(not_ignored_fields)) < len(not_ignored_fields):
            raise FatalCSVError(
                "Double headers: each column name may only appear once.")
        return True

    def getLocator(self, row):
        if row.get('container_code', None) not in (IGNORE_MARKER, None):
            # create mode
            return 'container_code'
        elif row.get('applicant_id', None) not in (IGNORE_MARKER, None):
            # update or remove mode
            return 'applicant_id'
        elif row.get('reg_number', None) not in (IGNORE_MARKER, None):
            # update or remove mode
            return 'reg_number'
        else:
            return None

    def getParent(self, row, site):
        result = None
        if self.getLocator(row) == 'container_code':
            result = site['applicants'].get(row['container_code'], None)
        elif self.getLocator(row) == 'reg_number':
            reg_number = row['reg_number']
            cat = queryUtility(ICatalog, name='applicants_catalog')
            results = list(
                cat.searchResults(reg_number=(reg_number, reg_number)))
            if results:
                result = results[0].__parent__
        elif self.getLocator(row) == 'applicant_id':
            applicant_id = row['applicant_id']
            cat = queryUtility(ICatalog, name='applicants_catalog')
            results = list(
                cat.searchResults(applicant_id=(applicant_id, applicant_id)))
            if results:
                result = results[0].__parent__
        return result

    def parentsExist(self, row, site):
        return self.getParent(row, site) is not None

    def getEntry(self, row, site):
        if self.getLocator(row) == 'container_code':
            if row.get('application_number', None) not in (IGNORE_MARKER, None):
                if not self.parentsExist(row, site):
                    return None
                parent = self.getParent(row, site)
                return parent.get(row['application_number'])
            return None
        if self.getLocator(row) == 'applicant_id':
            applicant_id = row['applicant_id']
            cat = queryUtility(ICatalog, name='applicants_catalog')
            results = list(
                cat.searchResults(applicant_id=(applicant_id, applicant_id)))
            if results:
                return results[0]
        if self.getLocator(row) == 'reg_number':
            reg_number = row['reg_number']
            cat = queryUtility(ICatalog, name='applicants_catalog')
            results = list(
                cat.searchResults(reg_number=(reg_number, reg_number)))
            if results:
                return results[0]
        return None

    def entryExists(self, row, site):
        return self.getEntry(row, site) is not None

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        parent.addApplicant(obj)
        #parent.__parent__.logger.info(
        #    'Applicant imported: %s' % obj.applicant_id)
        history = IObjectHistory(obj)
        history.addMessage(_('Application record imported'))
        return

    def delEntry(self, row, site):
        applicant = self.getEntry(row, site)
        if applicant is not None:
            parent = applicant.__parent__
            del parent[applicant.application_number]
            #parent.__parent__.logger.info(
            #    'Applicant removed: %s' % applicant.applicant_id)
        pass

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        items_changed = ''
        # Remove application_number from row if empty
        if 'application_number' in row and row['application_number'] in (
            None, IGNORE_MARKER):
            row.pop('application_number')

        # Update applicant_id fom application_number and container code
        # if application_number is given
        if 'application_number' in row:
            obj.applicant_id = u'%s_%s' % (
                row['container_code'], row['application_number'])
            items_changed += ('%s=%s, ' % ('applicant_id', obj.applicant_id))
            row.pop('application_number')

        # Update 
        if 'password' in row:
            passwd = row.get('password', IGNORE_MARKER)
            if passwd not in ('', IGNORE_MARKER):
                if passwd.startswith('{SSHA}'):
                    # already encrypted password
                    obj.password = passwd
                elif passwd == DELETION_MARKER:
                    obj.password = None
                else:
                    # not yet encrypted password
                    IUserAccount(obj).setPassword(passwd)
                items_changed += ('%s=%s, ' % ('password', passwd))
            row.pop('password')

        # Update registration state
        if 'state' in row:
            state = row.get('state', IGNORE_MARKER)
            if state not in (IGNORE_MARKER, ''):
                IWorkflowState(obj).setState(state)
                msg = _("State '${a}' set", mapping = {'a':state})
                history = IObjectHistory(obj)
                history.addMessage(msg)
                items_changed += ('%s=%s, ' % ('state', state))
            row.pop('state')

        # apply other values...
        items_changed += super(ApplicantProcessor, self).updateEntry(
            obj, row, site, filename)

        # Log actions...
        parent = self.getParent(row, site)
        if self.getLocator(row) == 'container_code':
            parent.__parent__.logger.info(
                '%s - %s - imported: %s' % (self.name, filename, items_changed))
        else:
            parent.__parent__.logger.info(
                '%s - %s - updated: %s' % (self.name, filename, items_changed))
        return items_changed

    def getMapping(self, path, headerfields, mode):
        """Get a mapping from CSV file headerfields to actually used fieldnames.
        """
        result = dict()
        reader = csv.reader(open(path, 'rb'))
        raw_header = reader.next()
        for num, field in enumerate(headerfields):
            if field not in ['applicant_id', 'reg_number'] and mode == 'remove':
                continue
            if field == u'--IGNORE--':
                # Skip ignored columns in failed and finished data files.
                continue
            result[raw_header[num]] = field
        return result

    def checkConversion(self, row, mode='create'):
        """Validates all values in row.
        """
        iface = self.iface
        if self.getLocator(row) == 'reg_number' or mode == 'remove':
            iface = self.iface_byregnumber
        converter = IObjectConverter(iface)
        errs, inv_errs, conv_dict =  converter.fromStringDict(
            row, self.factory_name, mode=mode)
        cert = conv_dict.get('course1', None)
        if cert is not None and (mode in ('create', 'update')):
            # course1 application category must match container's.
            site = grok.getSite()
            parent = self.getParent(row, site)
            if parent is None:
                errs.append(('container', 'not found'))
            elif cert.application_category != parent.application_category:
                errs.append(('course1', 'wrong application category'))
        if 'state' in row and \
            not row['state'] in IMPORTABLE_STATES:
            if row['state'] not in (IGNORE_MARKER, ''):
                errs.append(('state','not allowed'))
            else:
                # state is an attribute of Applicant and must not
                # be changed if empty
                conv_dict['state'] = IGNORE_MARKER
        application_number = row.get('application_number', None)
        if application_number in (IGNORE_MARKER, ''):
                conv_dict['application_number'] = IGNORE_MARKER
        return errs, inv_errs, conv_dict

    def checkUpdateRequirements(self, obj, row, site):
        """Checks requirements the object must fulfill when being updated.

        This method is not used in case of deleting or adding objects.

        Returns error messages as strings in case of requirement
        problems.
        """
        if obj.state == CREATED:
            return 'Applicant is blocked.'
        return None

class ApplicantOnlinePaymentProcessor(BatchProcessor):
    """The Applicant Online Payment Processor imports applicant payment tickets.
    The tickets are located in the applicant container.

    The `checkConversion` method checks the format of the payment identifier.
    In create mode it does also ensures that same p_id does not exist
    elsewhere. It must be portal-wide unique.

    When adding a payment ticket, the `addEntry` method checks if a
    payment has already been made. If so, a `DuplicationError` is raised.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'applicantpaymentprocessor'
    grok.name(util_name)

    name = _('ApplicantOnlinePayment Processor')
    iface = IApplicantOnlinePayment
    factory_name = 'waeup.ApplicantOnlinePayment'

    location_fields = ['applicant_id',]

    @property
    def available_fields(self):
        af = sorted(list(set(
            self.location_fields + getFields(self.iface).keys())) +
            ['p_id',])
        af.remove('display_item')
        return af

    def checkHeaders(self, headerfields, mode='ignore'):
        super(ApplicantOnlinePaymentProcessor, self).checkHeaders(headerfields)
        if mode in ('update', 'remove') and not 'p_id' in headerfields:
            raise FatalCSVError(
                "Need p_id for import in update and remove modes!")
        return True

    def getMapping(self, path, headerfields, mode):
        """Get a mapping from CSV file headerfields to actually used fieldnames.

        """
        result = dict()
        reader = unicodecsv.reader(open(path, 'rb'))
        raw_header = reader.next()
        for num, field in enumerate(headerfields):
            if field not in  ['applicant_id', 'p_id'] and mode == 'remove':
                continue
            if field == u'--IGNORE--':
                continue
            result[raw_header[num]] = field
        return result

    def parentsExist(self, row, site):
        return self.getParent(row, site) is not None

    def getParent(self, row, site):
        applicant_id = row['applicant_id']
        cat = queryUtility(ICatalog, name='applicants_catalog')
        results = list(
            cat.searchResults(applicant_id=(applicant_id, applicant_id)))
        if results:
            return results[0]
        return None

    def getEntry(self, row, site):
        applicant = self.getParent(row, site)
        if applicant is None:
            return None
        p_id = row.get('p_id', None)
        if p_id in (None, IGNORE_MARKER):
            return None
        # We can use the hash symbol at the end of p_id in import files
        # to avoid annoying automatic number transformation
        # by Excel or Calc
        p_id = p_id.strip('#')
        entry = applicant.get(p_id)
        return entry

    def entryExists(self, row, site):
        return self.getEntry(row, site) is not None

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        items_changed = super(ApplicantOnlinePaymentProcessor, self).updateEntry(
            obj, row, site, filename)
        applicant = self.getParent(row, site)
        applicant.__parent__.__parent__.logger.info(
            '%s - %s - %s - updated: %s'
            % (self.name, filename, applicant.applicant_id, items_changed))
        return

    def samePaymentMade(self, applicant, category):
        for key in applicant.keys():
            ticket = applicant[key]
            if ticket.p_state == 'paid' and\
                ticket.p_category == category:
                return True
        return False

    def addEntry(self, obj, row, site):
        applicant = self.getParent(row, site)
        p_id = row['p_id'].strip('#')
        if not (obj.p_item and obj.p_item.startswith(
            'Balance')) and self.samePaymentMade(applicant, obj.p_category):
            applicant.__parent__.__parent__.logger.info(
                '%s - %s - previous update cancelled'
                % (self.name, applicant.applicant_id))
            raise DuplicationError('Payment has already been made.')
        applicant[p_id] = obj
        return

    def delEntry(self, row, site):
        payment = self.getEntry(row, site)
        applicant = self.getParent(row, site)
        if payment is not None:
            applicant.__parent__.__parent__.logger.info('%s - Payment ticket removed: %s'
                % (applicant.applicant_id, payment.p_id))
            del applicant[payment.p_id]
        return

    def checkConversion(self, row, mode='ignore'):
        """Validates all values in row.
        """
        errs, inv_errs, conv_dict = super(
            ApplicantOnlinePaymentProcessor, self).checkConversion(row, mode=mode)
        # We have to check p_id.
        p_id = row.get('p_id', None)
        if mode == 'create' and p_id in (None, IGNORE_MARKER):
            timestamp = ("%d" % int(time()*10000))[1:]
            p_id = "p%s" % timestamp
            conv_dict['p_id'] = p_id
            return errs, inv_errs, conv_dict
        elif p_id in (None, IGNORE_MARKER):
            errs.append(('p_id','missing'))
            return errs, inv_errs, conv_dict
        else:
            p_id = p_id.strip('#')
            if not len(p_id) == 14:
                errs.append(('p_id','invalid length'))
                return errs, inv_errs, conv_dict
        if mode == 'create':
            cat = getUtility(ICatalog, name='payments_catalog')
            results = list(cat.searchResults(p_id=(p_id, p_id)))
            if len(results) > 0:
                sids = [IPayer(payment).id for payment in results]
                sids_string = ''
                for id in sids:
                    sids_string += '%s ' % id
                errs.append(('p_id','p_id exists in %s' % sids_string))
                return errs, inv_errs, conv_dict
        return errs, inv_errs, conv_dict
