## $Id: browser.py 17245 2022-12-28 09:56:45Z henrik $
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
"""UI components for basic applicants and related components.
"""
import os
import sys
import grok
import transaction
from cgi import escape
from urllib import urlencode
from datetime import datetime, date
from time import time, sleep
import xmlrpclib
from zope.event import notify
from zope.component import getUtility, queryUtility, createObject, getAdapter
from zope.catalog.interfaces import ICatalog
from zope.i18n import translate
from zope.security import checkPermission
from hurry.workflow.interfaces import (
    IWorkflowInfo, IWorkflowState, InvalidTransitionError)
from reportlab.platypus.doctemplate import LayoutError
from waeup.kofa.mandates.mandate import RefereeReportMandate
from waeup.kofa.applicants.interfaces import (
    IApplicant, IApplicantEdit, IApplicantsRoot,
    IApplicantsContainer, IApplicantsContainerAdd,
    IApplicantOnlinePayment, IApplicantsUtils,
    IApplicantRegisterUpdate, ISpecialApplicant,
    IApplicantRefereeReport,
    IApplicantBalancePayment
    )
from waeup.kofa.utils.helpers import (html2dict,
    string_from_bytes, file_size, get_fileformat)
from waeup.kofa.applicants.container import (
    ApplicantsContainer, VirtualApplicantsExportJobContainer)
from waeup.kofa.applicants.applicant import search
from waeup.kofa.applicants.workflow import (
    INITIALIZED, STARTED, PAID, SUBMITTED, 
    ADMITTED, NOT_ADMITTED, CREATED, PROCESSED)
from waeup.kofa.browser import (
#    KofaPage, KofaEditFormPage, KofaAddFormPage, KofaDisplayFormPage,
    DEFAULT_PASSPORT_IMAGE_PATH)
from waeup.kofa.browser.layout import (
    KofaPage, KofaEditFormPage, KofaAddFormPage, KofaDisplayFormPage)
from waeup.kofa.browser.interfaces import ICaptchaManager
from waeup.kofa.browser.breadcrumbs import Breadcrumb
from waeup.kofa.browser.layout import (
    NullValidator, jsaction, action, UtilityView)
from waeup.kofa.browser.pages import (
    add_local_role, del_local_roles, doll_up, ExportCSVView)
from waeup.kofa.interfaces import (
    IKofaObject, ILocalRolesAssignable, IExtFileStore, IPDF, DOCLINK,
    IFileStoreNameChooser, IPasswordValidator, IUserAccount, IKofaUtils)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.permissions import get_users_with_local_roles
from waeup.kofa.students.interfaces import IStudentsUtils
from waeup.kofa.students.browser import ContactStudentFormPage
from waeup.kofa.utils.helpers import string_from_bytes, file_size, now
from waeup.kofa.widgets.datewidget import (
    FriendlyDateDisplayWidget,
    FriendlyDatetimeDisplayWidget)

grok.context(IKofaObject) # Make IKofaObject the default context

WARNING = _('Please always save the form before final submission and note that'
            ' you can not edit your application records after submission.'
            ' You really want to submit?')

class ApplicantsRootPage(KofaDisplayFormPage):
    grok.context(IApplicantsRoot)
    grok.name('index')
    grok.require('waeup.Public')
    form_fields = grok.AutoFields(IApplicantsRoot)
    label = _('Applicants Section')
    pnav = 3

    def update(self):
        super(ApplicantsRootPage, self).update()
        return

    @property
    def introduction(self):
        # Here we know that the cookie has been set
        lang = self.request.cookies.get('kofa.language')
        html = self.context.description_dict.get(lang,'')
        if html == '':
            portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
            html = self.context.description_dict.get(portal_language,'')
        return html

    @property
    def containers(self):
        if self.layout.isAuthenticated():
            return self.context.values()
        values = sorted([container for container in self.context.values()
                         if not container.hidden and container.enddate],
                        key=lambda value: value.enddate, reverse=True)
        return values

class ApplicantsSearchPage(KofaPage):
    grok.context(IApplicantsRoot)
    grok.name('search')
    grok.require('waeup.viewApplication')
    label = _('Find applicants')
    search_button = _('Find applicant')
    pnav = 3

    def update(self, *args, **kw):
        form = self.request.form
        self.results = []
        if 'searchterm' in form and form['searchterm']:
            self.searchterm = form['searchterm']
            self.searchtype = form['searchtype']
        elif 'old_searchterm' in form:
            self.searchterm = form['old_searchterm']
            self.searchtype = form['old_searchtype']
        else:
            if 'search' in form:
                self.flash(_('Empty search string'), type='warning')
            return
        self.results = search(query=self.searchterm,
            searchtype=self.searchtype, view=self)
        if not self.results:
            self.flash(_('No applicant found.'), type='warning')
        return

class ApplicantsRootManageFormPage(KofaEditFormPage):
    grok.context(IApplicantsRoot)
    grok.name('manage')
    grok.template('applicantsrootmanagepage')
    form_fields = grok.AutoFields(IApplicantsRoot)
    label = _('Manage applicants section')
    pnav = 3
    grok.require('waeup.manageApplication')
    taboneactions = [_('Save')]
    tabtwoactions = [_('Add applicants container'), _('Remove selected')]
    tabthreeactions1 = [_('Remove selected local roles')]
    tabthreeactions2 = [_('Add local role')]
    subunits = _('Applicants Containers')
    doclink = DOCLINK + '/applicants.html'

    def getLocalRoles(self):
        roles = ILocalRolesAssignable(self.context)
        return roles()

    def getUsers(self):
        return getUtility(IKofaUtils).getUsers()

    #def getUsers(self):
    #    """Get a list of all users.
    #    """
    #    for key, val in grok.getSite()['users'].items():
    #        url = self.url(val)
    #        yield(dict(url=url, name=key, val=val))

    def getUsersWithLocalRoles(self):
        return get_users_with_local_roles(self.context)

    @jsaction(_('Remove selected'))
    def delApplicantsContainers(self, **data):
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No container selected!'), type='warning')
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        deleted = []
        for id in child_id:
            try:
                del self.context[id]
                deleted.append(id)
            except:
                self.flash(_('Could not delete:') + ' %s: %s: %s' % (
                    id, sys.exc_info()[0], sys.exc_info()[1]), type='danger')
        if len(deleted):
            self.flash(_('Successfully removed: ${a}',
                mapping = {'a':', '.join(deleted)}))
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        self.context.logger.info(
            '%s - removed: %s' % (ob_class, ', '.join(deleted)))
        self.redirect(self.url(self.context, '@@manage')+'#tab2')
        return

    @action(_('Add applicants container'), validator=NullValidator)
    def addApplicantsContainer(self, **data):
        self.redirect(self.url(self.context, '@@add'))
        return

    @action(_('Add local role'), validator=NullValidator)
    def addLocalRole(self, **data):
        return add_local_role(self,3, **data)

    @action(_('Remove selected local roles'))
    def delLocalRoles(self, **data):
        return del_local_roles(self,3,**data)

    @action(_('Save'), style='primary')
    def save(self, **data):
        self.applyData(self.context, **data)
        description = getattr(self.context, 'description', None)
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        self.context.description_dict = html2dict(description, portal_language)
        self.flash(_('Form has been saved.'))
        return

class ApplicantsContainerAddFormPage(KofaAddFormPage):
    grok.context(IApplicantsRoot)
    grok.require('waeup.manageApplication')
    grok.name('add')
    grok.template('applicantscontaineraddpage')
    label = _('Add applicants container')
    pnav = 3

    form_fields = grok.AutoFields(
        IApplicantsContainerAdd).omit('code').omit('title')

    @action(_('Add applicants container'))
    def addApplicantsContainer(self, **data):
        year = data['year']
        if not data['container_number'] and not data['year']:
            self.flash(
              _('You must select either Year of Entrance or Container Number.'),
                type='warning')
            return
        if not data['container_number']:
            code = u'%s%s' % (data['prefix'], year)
        else:
            code = u'%s%s' % (data['prefix'], data['container_number'])
        apptypes_dict = getUtility(IApplicantsUtils).APP_TYPES_DICT
        title = u'%s' % apptypes_dict[data['prefix']][0]
        if year:
            title = u'%s %s/%s' % (title, year, year + 1)
        if code in self.context.keys():
            self.flash(
              _('An applicants container for the same application '
                'type and entrance year or container number '
                'already exists in the database.'),
                type='warning')
            return
        # Add new applicants container...
        container = createObject(u'waeup.ApplicantsContainer')
        self.applyData(container, **data)
        container.code = code
        container.title = title
        self.context[code] = container
        self.flash(_('Added:') + ' "%s".' % code)
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        self.context.logger.info('%s - added: %s' % (ob_class, code))
        self.redirect(self.url(self.context, u'@@manage'))
        return

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context, '@@manage'))

class ApplicantsRootBreadcrumb(Breadcrumb):
    """A breadcrumb for applicantsroot.
    """
    grok.context(IApplicantsRoot)
    title = _(u'Applicants')

class ApplicantsContainerBreadcrumb(Breadcrumb):
    """A breadcrumb for applicantscontainers.
    """
    grok.context(IApplicantsContainer)


class ApplicantsExportsBreadcrumb(Breadcrumb):
    """A breadcrumb for exports.
    """
    grok.context(VirtualApplicantsExportJobContainer)
    title = _(u'Applicant Data Exports')
    target = None

class ApplicantBreadcrumb(Breadcrumb):
    """A breadcrumb for applicants.
    """
    grok.context(IApplicant)

    @property
    def title(self):
        """Get a title for a context.
        """
        return self.context.application_number

class OnlinePaymentBreadcrumb(Breadcrumb):
    """A breadcrumb for payments.
    """
    grok.context(IApplicantOnlinePayment)

    @property
    def title(self):
        return self.context.p_id

class RefereeReportBreadcrumb(Breadcrumb):
    """A breadcrumb for referee reports.
    """
    grok.context(IApplicantRefereeReport)

    @property
    def title(self):
        return self.context.r_id

class ApplicantsStatisticsPage(KofaDisplayFormPage):
    """Some statistics about applicants in a container.
    """
    grok.context(IApplicantsContainer)
    grok.name('statistics')
    grok.require('waeup.viewApplicationStatistics')
    grok.template('applicantcontainerstatistics')

    @property
    def label(self):
        return "%s" % self.context.title

class ApplicantsContainerPage(KofaDisplayFormPage):
    """The standard view for regular applicant containers.
    """
    grok.context(IApplicantsContainer)
    grok.name('index')
    grok.require('waeup.Public')
    grok.template('applicantscontainerpage')
    pnav = 3

    @property
    def form_fields(self):
        form_fields = grok.AutoFields(IApplicantsContainer).omit(
            'title', 'description')
        form_fields[
            'startdate'].custom_widget = FriendlyDatetimeDisplayWidget('le')
        form_fields[
            'enddate'].custom_widget = FriendlyDatetimeDisplayWidget('le')
        if self.request.principal.id == 'zope.anybody':
            form_fields = form_fields.omit(
                'code', 'prefix', 'year', 'mode', 'hidden',
                'strict_deadline', 'application_category',
                'application_slip_notice', 'with_picture')
        return form_fields

    @property
    def introduction(self):
        # Here we know that the cookie has been set
        lang = self.request.cookies.get('kofa.language')
        html = self.context.description_dict.get(lang,'')
        if html == '':
            portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
            html = self.context.description_dict.get(portal_language,'')
        return html

    @property
    def label(self):
        return "%s" % self.context.title

class ApplicantsContainerManageFormPage(KofaEditFormPage):
    grok.context(IApplicantsContainer)
    grok.name('manage')
    grok.template('applicantscontainermanagepage')
    form_fields = grok.AutoFields(IApplicantsContainer)
    taboneactions = [_('Save'),_('Cancel')]
    tabtwoactions = [_('Remove selected'),_('Cancel'),
        _('Create students from selected')]
    tabthreeactions1 = [_('Remove selected local roles')]
    tabthreeactions2 = [_('Add local role')]
    # Use friendlier date widget...
    grok.require('waeup.manageApplication')
    doclink = DOCLINK + '/applicants.html'
    max_applicants = 2000

    @property
    def label(self):
        return _('Manage applicants container')

    pnav = 3

    @property
    def showApplicants(self):
        if self.context.counts[1] < self.max_applicants:
            return True
        return False

    def getLocalRoles(self):
        roles = ILocalRolesAssignable(self.context)
        return roles()

    #def getUsers(self):
    #    """Get a list of all users.
    #    """
    #    for key, val in grok.getSite()['users'].items():
    #        url = self.url(val)
    #        yield(dict(url=url, name=key, val=val))

    def getUsers(self):
        return getUtility(IKofaUtils).getUsers()

    def getUsersWithLocalRoles(self):
        return get_users_with_local_roles(self.context)

    @action(_('Save'), style='primary')
    def save(self, **data):
        changed_fields = self.applyData(self.context, **data)
        if changed_fields:
            changed_fields = reduce(lambda x,y: x+y, changed_fields.values())
        else:
            changed_fields = []
        description = getattr(self.context, 'description', None)
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        self.context.description_dict = html2dict(description, portal_language)
        self.flash(_('Form has been saved.'))
        fields_string = ' + '.join(changed_fields)
        self.context.writeLogMessage(self, 'saved: %s' % fields_string)
        return

    @jsaction(_('Remove selected'))
    def delApplicant(self, **data):
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No applicant selected!'), type='warning')
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        deleted = []
        for id in child_id:
            try:
                del self.context[id]
                deleted.append(id)
            except:
                self.flash(_('Could not delete:') + ' %s: %s: %s' % (
                    id, sys.exc_info()[0], sys.exc_info()[1]), type='danger')
        if len(deleted):
            self.flash(_('Successfully removed: ${a}',
                mapping = {'a':', '.join(deleted)}))
        self.redirect(self.url(self.context, u'@@manage')+'#tab2')
        return

    @action(_('Create students from selected'))
    def createStudents(self, **data):
        if not checkPermission('waeup.createStudents', self.context):
            self.flash(
                _('You don\'t have permission to create student records.'),
                type='warning')
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No applicant selected!'), type='warning')
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        created = []
        if len(child_id) > 10 and self.request.principal.id != 'admin':
            self.flash(_('A maximum of 10 applicants can be selected!'),
                       type='warning')
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        for id in child_id:
            success, msg = self.context[id].createStudent(view=self)
            if success:
                created.append(id)
        if len(created):
            self.flash(_('${a} students successfully created.',
                mapping = {'a': len(created)}))
        else:
            self.flash(_('No student could be created.'), type='warning')
        self.redirect(self.url(self.context, u'@@manage')+'#tab2')
        return

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))
        return

    @action(_('Add local role'), validator=NullValidator)
    def addLocalRole(self, **data):
        return add_local_role(self,3, **data)

    @action(_('Remove selected local roles'))
    def delLocalRoles(self, **data):
        return del_local_roles(self,3,**data)

class ApplicantAddFormPage(KofaAddFormPage):
    """Add-form to add an applicant.
    """
    grok.context(IApplicantsContainer)
    grok.require('waeup.manageApplication')
    grok.name('addapplicant')
    #grok.template('applicantaddpage')
    form_fields = grok.AutoFields(IApplicant).select(
        'firstname', 'middlename', 'lastname',
        'email', 'phone')
    label = _('Add applicant')
    pnav = 3
    doclink = DOCLINK + '/applicants.html'

    @action(_('Create application record'))
    def addApplicant(self, **data):
        applicant = createObject(u'waeup.Applicant')
        self.applyData(applicant, **data)
        self.context.addApplicant(applicant)
        self.flash(_('Application record created.'))
        self.redirect(
            self.url(self.context[applicant.application_number], 'index'))
        return

class ApplicantsContainerPrefillFormPage(KofaAddFormPage):
    """Form to pre-fill applicants containers.
    """
    grok.context(IApplicantsContainer)
    grok.require('waeup.manageApplication')
    grok.name('prefill')
    grok.template('prefillcontainer')
    label = _('Pre-fill container')
    pnav = 3
    doclink = DOCLINK + '/applicants/browser.html#preparation-and-maintenance-of-applicants-containers'

    def update(self):
        if self.context.mode == 'update':
            self.flash(_('Container must be in create mode to be pre-filled.'),
                type='danger')
            self.redirect(self.url(self.context))
            return
        super(ApplicantsContainerPrefillFormPage, self).update()
        return

    @action(_('Pre-fill now'), style='primary')
    def addApplicants(self):
        form = self.request.form
        if 'number' in form and form['number']:
            number = int(form['number'])
        for i in range(number):
            applicant = createObject(u'waeup.Applicant')
            self.context.addApplicant(applicant)
        self.flash(_('%s application records created.' % number))
        self.context.writeLogMessage(self, '%s applicants created' % (number))
        self.redirect(self.url(self.context, 'index'))
        return

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))
        return

class ApplicantsContainerPurgeFormPage(KofaEditFormPage):
    """Form to purge applicants containers.
    """
    grok.context(IApplicantsContainer)
    grok.require('waeup.manageApplication')
    grok.name('purge')
    grok.template('purgecontainer')
    label = _('Purge container')
    pnav = 3
    doclink = DOCLINK + '/applicants/browser.html#preparation-and-maintenance-of-applicants-containers'

    @action(_('Remove initialized records'),
              tooltip=_('Don\'t use if application is in progress!'),
              warning=_('Are you really sure?'),
              style='primary')
    def purgeInitialized(self):
        form = self.request.form
        purged = 0
        keys = [key for key in self.context.keys()]
        for key in keys:
            if self.context[key].state == 'initialized':
                del self.context[key]
                purged += 1
        self.flash(_('%s application records purged.' % purged))
        self.context.writeLogMessage(self, '%s applicants purged' % (purged))
        self.redirect(self.url(self.context, 'index'))
        return

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))
        return

class ApplicantDisplayFormPage(KofaDisplayFormPage):
    """A display view for applicant data.
    """
    grok.context(IApplicant)
    grok.name('index')
    grok.require('waeup.viewApplication')
    grok.template('applicantdisplaypage')
    label = _('Applicant')
    pnav = 3
    hide_hint = False

    @property
    def display_refereereports(self):
        if self.context.refereereports:
            return True
        return False

    @property
    def file_links(self):
        html = ''
        file_store = getUtility(IExtFileStore)
        additional_files = getUtility(IApplicantsUtils).ADDITIONAL_FILES
        for filename in additional_files:
            pdf = getUtility(IExtFileStore).getFileByContext(
                self.context, attr=filename[1])
            if pdf:
                html += '<a href="%s">%s</a>, ' % (self.url(
                    self.context, filename[1]), filename[0])
        html = html.strip(', ')
        return html

    @property
    def display_payments(self):
        if self.context.payments:
            return True
        if self.context.special:
            return True
        return getattr(self.context.__parent__, 'application_fee', None)

    @property
    def form_fields(self):
        if self.context.special:
            form_fields = grok.AutoFields(ISpecialApplicant).omit('locked')
        else:
            form_fields = grok.AutoFields(IApplicant).omit(
                'locked', 'course_admitted', 'password', 'suspended')
        return form_fields

    @property
    def target(self):
        return getattr(self.context.__parent__, 'prefix', None)

    @property
    def separators(self):
        return getUtility(IApplicantsUtils).SEPARATORS_DICT

    def update(self):
        self.passport_url = self.url(self.context, 'passport.jpg')
        # Mark application as started if applicant logs in for the first time
        usertype = getattr(self.request.principal, 'user_type', None)
        if usertype == 'applicant' and \
            IWorkflowState(self.context).getState() == INITIALIZED:
            IWorkflowInfo(self.context).fireTransition('start')
        if usertype == 'applicant' and self.context.state == 'created':
            session = '%s/%s' % (self.context.__parent__.year,
                                 self.context.__parent__.year+1)
            title = getattr(grok.getSite()['configuration'], 'name', u'Sample University')
            msg = _(
                '\n <strong>Congratulations!</strong>' +
                ' You have been offered provisional admission into the' +
                ' ${c} Academic Session of ${d}.'
                ' Your student record has been created for you.' +
                ' Please, logout again and proceed to the' +
                ' login page of the portal.'
                ' Then enter your new student credentials:' +
                ' user name= ${a}, password = ${b}.' +
                ' Change your password when you have logged in.',
                mapping = {
                    'a':self.context.student_id,
                    'b':self.context.application_number,
                    'c':session,
                    'd':title}
                )
            self.flash(msg)
        return

    @property
    def hasPassword(self):
        if self.context.password:
            return _('set')
        return _('unset')

    @property
    def label(self):
        container_title = self.context.__parent__.title
        return _('${a} <br /> Application Record ${b}', mapping = {
            'a':container_title, 'b':self.context.application_number})

    def getCourseAdmitted(self):
        """Return link, title and code in html format to the certificate
           admitted.
        """
        course_admitted = self.context.course_admitted
        if getattr(course_admitted, '__parent__',None):
            url = self.url(course_admitted)
            title = course_admitted.title
            code = course_admitted.code
            return '<a href="%s">%s - %s</a>' %(url,code,title)
        return ''

class ApplicantBaseDisplayFormPage(ApplicantDisplayFormPage):
    grok.context(IApplicant)
    grok.name('base')

    @property
    def form_fields(self):
        form_fields = grok.AutoFields(IApplicant).select(
            'applicant_id', 'reg_number', 'email', 'course1')
        if self.context.__parent__.prefix in ('special',):
            form_fields['reg_number'].field.title = u'Identification Number'
            return form_fields
        return form_fields

class ContactApplicantFormPage(ContactStudentFormPage):
    grok.context(IApplicant)
    grok.name('contactapplicant')
    grok.require('waeup.viewApplication')
    pnav = 3

class CreateStudentPage(UtilityView, grok.View):
    """Create a student object from applicant data.
    """
    grok.context(IApplicant)
    grok.name('createstudent')
    grok.require('waeup.createStudents')

    def update(self):
        success, msg = self.context.createStudent(view=self, send_email=True)
        if success:
            self.flash(msg)
        else:
            self.flash(msg, type='warning')
        self.redirect(self.url(self.context))
        return

    def render(self):
        return

class CreateAllStudentsPage(KofaPage):
    """Create all student objects from applicant data
    in the root container or in a specific applicants container only.
    Only PortalManagers or StudentCreators can do this.
    """
    #grok.context(IApplicantsContainer)
    grok.name('createallstudents')
    grok.require('waeup.createStudents')
    label = _('Student Record Creation Report')

    def update(self):
        grok.getSite()['configuration'].maintmode_enabled_by = u'admin'
        transaction.commit()
        # Wait 10 seconds for all transactions to be finished.
        # Do not wait in tests.
        if not self.request.principal.id == 'zope.mgr':
            sleep(10)
        cat = getUtility(ICatalog, name='applicants_catalog')
        results = list(cat.searchResults(state=(ADMITTED, ADMITTED)))
        created = []
        failed = []
        container_only = False
        applicants_root = grok.getSite()['applicants']
        if isinstance(self.context, ApplicantsContainer):
            container_only = True
        for result in results:
            if container_only and result.__parent__ is not self.context:
                continue
            success, msg = result.createStudent(view=self)
            if success:
                created.append(result.applicant_id)
            else:
                failed.append(
                    (result.applicant_id, self.url(result, 'manage'), msg))
                ob_class = self.__implemented__.__name__.replace(
                    'waeup.kofa.','')
        grok.getSite()['configuration'].maintmode_enabled_by = None
        self.successful = ', '.join(created)
        self.failed = failed
        return


class ApplicationFeePaymentAddPage(UtilityView, grok.View):
    """ Page to add an online payment ticket
    """
    grok.context(IApplicant)
    grok.name('addafp')
    grok.require('waeup.payApplicant')
    factory = u'waeup.ApplicantOnlinePayment'

    @property
    def custom_requirements(self):
        return ''

    def update(self):
        # Additional requirements in custom packages.
        if self.custom_requirements:
            self.flash(
                self.custom_requirements,
                type='danger')
            self.redirect(self.url(self.context))
            return
        if not self.context.special:
            for ticket in self.context.payments:
                if ticket.p_state == 'paid':
                      self.flash(
                          _('This type of payment has already been made.'),
                          type='warning')
                      self.redirect(self.url(self.context))
                      return
        applicants_utils = getUtility(IApplicantsUtils)
        container = self.context.__parent__
        payment = createObject(self.factory)
        failure = applicants_utils.setPaymentDetails(
            container, payment, self.context)
        if failure is not None:
            self.flash(failure, type='danger')
            self.redirect(self.url(self.context))
            return
        self.context[payment.p_id] = payment
        self.context.writeLogMessage(self, 'added: %s' % payment.p_id)
        self.flash(_('Payment ticket created.'))
        self.redirect(self.url(payment))
        return

    def render(self):
        return
        
class BalancePaymentAddFormPage(KofaAddFormPage):
    """ Page to add an online payment which can balance s previous session
    payment.
    """
    grok.context(IApplicant)
    grok.name('addbp')
    grok.template('balancepaymentaddform')
    grok.require('waeup.manageApplication')
    form_fields = grok.AutoFields(IApplicantBalancePayment)
    label = _('Add balance')
    #pnav = 4

    @property
    def selectable_payment_options(self):
        options = getUtility(
            IKofaUtils).selectable_payment_options(self.context)
        return sorted(options.items(), key=lambda value: value[1])

    @action(_('Create ticket'), style='primary')
    def createTicket(self, **data):
        p_category = data['p_category']
        form = self.request.form
        p_option = form.get('form.p_option', None)
        balance_amount = data.get('balance_amount', None)
        applicants_utils = getUtility(IApplicantsUtils)
        error, payment = applicants_utils.setBalanceDetails(
            self.context, p_category, balance_amount)
        if error is not None:
            self.flash(error, type="danger")
            return
        if p_option:
            payment.p_option = p_option
        self.context[payment.p_id] = payment
        self.flash(_('Payment ticket created.'))
        self.context.writeLogMessage(self,'added: %s' % payment.p_id)
        self.redirect(self.url(payment))
        return

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))


class OnlinePaymentDisplayFormPage(KofaDisplayFormPage):
    """ Page to view an online payment ticket
    """
    grok.context(IApplicantOnlinePayment)
    grok.name('index')
    grok.require('waeup.viewApplication')
    form_fields = grok.AutoFields(IApplicantOnlinePayment).omit('p_item')
    form_fields[
        'creation_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    form_fields[
        'payment_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    pnav = 3

    @property
    def label(self):
        return _('${a}: Online Payment Ticket ${b}', mapping = {
            'a':self.context.__parent__.display_fullname,
            'b':self.context.p_id})

class OnlinePaymentApprovePage(UtilityView, grok.View):
    """ Approval view
    """
    grok.context(IApplicantOnlinePayment)
    grok.name('approve')
    grok.require('waeup.managePortal')

    def update(self):
        flashtype, msg, log = self.context.approveApplicantPayment()
        if log is not None:
            applicant = self.context.__parent__
            # Add log message to applicants.log
            applicant.writeLogMessage(self, log)
            # Add log message to payments.log
            self.context.logger.info(
                '%s,%s,%s,%s,%s,,,,,,' % (
                applicant.applicant_id,
                self.context.p_id, self.context.p_category,
                self.context.amount_auth, self.context.r_code))
        self.flash(msg, type=flashtype)
        return

    def render(self):
        self.redirect(self.url(self.context, '@@index'))
        return

class ExportPDFPaymentSlipPage(UtilityView, grok.View):
    """Deliver a PDF slip of the context.
    """
    grok.context(IApplicantOnlinePayment)
    grok.name('payment_slip.pdf')
    grok.require('waeup.viewApplication')
    form_fields = grok.AutoFields(IApplicantOnlinePayment).omit('p_item')
    form_fields['creation_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    form_fields['payment_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    #prefix = 'form'
    note = None

    @property
    def title(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Payment Data'), 'waeup.kofa',
            target_language=portal_language)

    @property
    def label(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Online Payment Slip'),
            'waeup.kofa', target_language=portal_language) \
            + ' %s' % self.context.p_id

    @property
    def payment_slip_download_warning(self):
        if self.context.__parent__.state not in (
            SUBMITTED, ADMITTED, NOT_ADMITTED, CREATED):
            return _('Please submit the application form before '
                     'trying to download payment slips.')
        return ''

    def render(self):
        if self.payment_slip_download_warning:
            self.flash(self.payment_slip_download_warning, type='danger')
            self.redirect(self.url(self.context))
            return
        applicantview = ApplicantBaseDisplayFormPage(self.context.__parent__,
            self.request)
        students_utils = getUtility(IStudentsUtils)
        return students_utils.renderPDF(self,'payment_slip.pdf',
            self.context.__parent__, applicantview, note=self.note)

class ExportPDFPageApplicationSlip(UtilityView, grok.View):
    """Deliver a PDF slip of the context.
    """
    grok.context(IApplicant)
    grok.name('application_slip.pdf')
    grok.require('waeup.viewApplication')
    #prefix = 'form'

    def update(self):
        if self.context.state in ('initialized', 'started', 'paid'):
            self.flash(
                _('Please pay and submit before trying to download '
                  'the application slip.'), type='warning')
            return self.redirect(self.url(self.context))
        return

    def render(self):
        try:
            pdfstream = getAdapter(self.context, IPDF, name='application_slip')(
                view=self)
        except IOError:
            self.flash(
                _('Your image file is corrupted. '
                  'Please replace.'), type='danger')
            return self.redirect(self.url(self.context))
        except LayoutError, err:
            self.flash(
                'PDF file could not be created. Reportlab error message: %s'
                % escape(err.message),
                type="danger")
            return self.redirect(self.url(self.context))
        self.response.setHeader(
            'Content-Type', 'application/pdf')
        return pdfstream

def handle_img_upload(upload, context, view):
    """Handle upload of applicant image.

    Returns `True` in case of success or `False`.

    Please note that file pointer passed in (`upload`) most probably
    points to end of file when leaving this function.
    """
    max_upload_size = getUtility(IKofaUtils).MAX_PASSPORT_SIZE
    size = file_size(upload)
    if size > max_upload_size:
        view.flash(_('Uploaded image is too big!'), type='danger')
        return False
    dummy, ext = os.path.splitext(upload.filename)
    ext.lower()
    if ext != '.jpg':
        view.flash(_('jpg file extension expected.'), type='danger')
        return False
    upload.seek(0) # file pointer moved when determining size
    store = getUtility(IExtFileStore)
    file_id = IFileStoreNameChooser(context).chooseName()
    try:
        store.createFile(file_id, upload)
    except IOError:
        view.flash(_('Image file cannot be changed.'), type='danger')
        return False
    return True

def handle_file_upload(upload, context, view, attr=None):
    """Handle upload of applicant files.

    Returns `True` in case of success or `False`.

    Please note that file pointer passed in (`upload`) most probably
    points to end of file when leaving this function.
    """
    size = file_size(upload)
    max_upload_size = 1024 * getUtility(IStudentsUtils).MAX_KB
    if size > max_upload_size:
        view.flash(_('Uploaded file is too big!'))
        return False
    upload.seek(0)  # file pointer moved when determining size
    dummy,ext = os.path.splitext(upload.filename)
    file_format = get_fileformat(None, upload.read(512))
    upload.seek(0)  # same here
    if file_format is None:
        view.flash(_('Could not determine file type.'), type="danger")
        return False
    ext.lower()
    if ext not in ('.pdf', '.jpg'):
        view.flash(_('pdf or jpg file extension expected.'), type='danger')
        return False
    download_name = attr + '.' + file_format
    store = getUtility(IExtFileStore)
    file_id = IFileStoreNameChooser(context).chooseName(attr=download_name)
    store.createFile(file_id, upload)
    return True

class ApplicantManageFormPage(KofaEditFormPage):
    """A full edit view for applicant data.
    """
    grok.context(IApplicant)
    grok.name('manage')
    grok.require('waeup.manageApplication')
    grok.template('applicanteditpage')
    manage_applications = True
    pnav = 3
    
    @property
    def display_actions(self):
        actions = [[_('Save'), _('Finally Submit')],
                   [_('Add online payment ticket'),
                    _('Add balance payment ticket'),
                    _('Remove selected tickets')]]
        applicants_utils = getUtility(IApplicantsUtils)
        if self.context.state not in applicants_utils.BALANCE_PAYMENT_STATES:
            actions[1].pop(1)
        return actions

    @property
    def display_payments(self):
        if self.context.payments:
            return True
        if self.context.special:
            return True
        return getattr(self.context.__parent__, 'application_fee', None)

    @property
    def display_refereereports(self):
        if self.context.refereereports:
            return True
        return False

    def display_fileupload(self, filename):
        """This method can be used in custom packages to avoid unneccessary
        file uploads.
        """
        return True

    @property
    def form_fields(self):
        if self.context.special:
            form_fields = grok.AutoFields(ISpecialApplicant)
            form_fields['applicant_id'].for_display = True
        else:
            form_fields = grok.AutoFields(IApplicant)
            form_fields['student_id'].for_display = True
            form_fields['applicant_id'].for_display = True
        return form_fields

    @property
    def target(self):
        return getattr(self.context.__parent__, 'prefix', None)

    @property
    def separators(self):
        return getUtility(IApplicantsUtils).SEPARATORS_DICT

    @property
    def custom_upload_requirements(self):
        return ''

    def update(self):
        super(ApplicantManageFormPage, self).update()
        max_upload_size = getUtility(IKofaUtils).MAX_PASSPORT_SIZE
        self.wf_info = IWorkflowInfo(self.context)
        self.max_upload_size = string_from_bytes(max_upload_size)
        self.upload_success = None
        upload = self.request.form.get('form.passport', None)
        if upload:
            if self.custom_upload_requirements:
                self.flash(
                    self.custom_upload_requirements,
                    type='danger')
                self.redirect(self.url(self.context))
                return
            # We got a fresh upload, upload_success is
            # either True or False
            self.upload_success = handle_img_upload(
                upload, self.context, self)
            if self.upload_success:
                self.context.writeLogMessage(self, 'saved: passport')
        file_store = getUtility(IExtFileStore)
        self.additional_files = getUtility(IApplicantsUtils).ADDITIONAL_FILES
        for filename in self.additional_files:
            upload = self.request.form.get(filename[1], None)
            if upload:
                # We got a fresh file upload
                success = handle_file_upload(
                    upload, self.context, self, attr=filename[1])
                if success:
                    self.context.writeLogMessage(
                        self, 'saved: %s' % filename[1])
                else:
                    self.upload_success = False
        self.max_file_upload_size = string_from_bytes(
            1024*getUtility(IStudentsUtils).MAX_KB)
        return

    @property
    def label(self):
        container_title = self.context.__parent__.title
        return _('${a} <br /> Application Form ${b}', mapping = {
            'a':container_title, 'b':self.context.application_number})

    def getTransitions(self):
        """Return a list of dicts of allowed transition ids and titles.

        Each list entry provides keys ``name`` and ``title`` for
        internal name and (human readable) title of a single
        transition.
        """
        allowed_transitions = [t for t in self.wf_info.getManualTransitions()
            if not t[0] in ('pay', 'create')]
        return [dict(name='', title=_('No transition'))] +[
            dict(name=x, title=y) for x, y in allowed_transitions]

    def saveCourses(self):
        """In custom packages we needed to customize the certificate
        select widget. We just save course1 and course2 if these customized
        fields appear in the form.
        """
        return None, []

    @action(_('Save'), style='primary')
    def save(self, **data):
        error, changed_courses = self.saveCourses()
        if error:
            self.flash(error, type='danger')
            return
        form = self.request.form
        password = form.get('password', None)
        password_ctl = form.get('control_password', None)
        if password:
            validator = getUtility(IPasswordValidator)
            errors = validator.validate_password(password, password_ctl)
            if errors:
                self.flash( ' '.join(errors), type='danger')
                return
        if self.upload_success is False:  # False is not None!
            # Error during image upload. Ignore other values.
            return 
        changed_fields = self.applyData(self.context, **data)
        # Turn list of lists into single list
        if changed_fields:
            changed_fields = reduce(lambda x,y: x+y, changed_fields.values())
        else:
            changed_fields = []
        changed_fields += changed_courses
        if password:
            # Now we know that the form has no errors and can set password ...
            IUserAccount(self.context).setPassword(password)
            changed_fields.append('password')
        fields_string = ' + '.join(changed_fields)
        trans_id = form.get('transition', None)
        if trans_id:
            self.wf_info.fireTransition(trans_id)
        self.flash(_('Form has been saved.'))
        if fields_string:
            self.context.writeLogMessage(self, 'saved: %s' % fields_string)
        return

    def unremovable(self, ticket):
        return False

    @property
    def picture_editable(self):
        return self.context.__parent__.with_picture

    # This method is also used by the ApplicantEditFormPage
    def delPaymentTickets(self, **data):
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No payment selected.'), type='warning')
            self.redirect(self.url(self.context))
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        deleted = []
        for id in child_id:
            # Applicants are not allowed to remove used payment tickets
            if not self.unremovable(self.context[id]):
                try:
                    del self.context[id]
                    deleted.append(id)
                except:
                    self.flash(_('Could not delete:') + ' %s: %s: %s' % (
                      id, sys.exc_info()[0], sys.exc_info()[1]), type='danger')
        if len(deleted):
            self.flash(_('Successfully removed: ${a}',
                mapping = {'a':', '.join(deleted)}))
            self.context.writeLogMessage(
                self, 'removed: % s' % ', '.join(deleted))
        return

    # We explicitely want the forms to be validated before payment tickets
    # can be created. If no validation is requested, use
    # 'validator=NullValidator' in the action directive
    @action(_('Add online payment ticket'), style='primary')
    def addPaymentTicket(self, **data):
        self.redirect(self.url(self.context, '@@addafp'))
        return

    @action(_('Add balance payment ticket'), style='primary')
    def addBalancePaymentTicket(self, **data):
        self.redirect(self.url(self.context, '@@addbp'))
        return

    @jsaction(_('Remove selected tickets'))
    def removePaymentTickets(self, **data):
        self.delPaymentTickets(**data)
        self.redirect(self.url(self.context) + '/@@manage')
        return

    # Not used in base package
    def file_exists(self, attr):
        file = getUtility(IExtFileStore).getFileByContext(
            self.context, attr=attr)
        if file:
            return True
        else:
            return False

class ApplicantEditFormPage(ApplicantManageFormPage):
    """An applicant-centered edit view for applicant data.
    """
    grok.context(IApplicantEdit)
    grok.name('edit')
    grok.require('waeup.handleApplication')
    grok.template('applicanteditpage')
    manage_applications = False
    submit_state = PAID
    mandate_days = 31

    @property
    def display_refereereports(self):
        return False

    @property
    def form_fields(self):
        if self.context.special:
            form_fields = grok.AutoFields(ISpecialApplicant).omit(
                'locked', 'suspended')
            form_fields['applicant_id'].for_display = True
        else:
            form_fields = grok.AutoFields(IApplicantEdit).omit(
                'locked', 'course_admitted', 'student_id',
                'suspended'
                )
            form_fields['applicant_id'].for_display = True
            form_fields['reg_number'].for_display = True
        return form_fields

    @property
    def display_actions(self):
        state = IWorkflowState(self.context).getState()
        # If the form is unlocked, applicants are allowed to save the form
        # and remove unused tickets.
        actions = [[_('Save')], [_('Remove selected tickets')]]
        # Only in state started they can also add tickets.
        if state == STARTED:
            actions = [[_('Save')],
                [_('Add online payment ticket'),_('Remove selected tickets')]]
        # In state paid, they can submit the data and further add tickets
        # if the application is special.
        elif self.context.special and state == PAID:
            actions = [[_('Save'), _('Finally Submit')],
                [_('Add online payment ticket'),_('Remove selected tickets')]]
        elif state == PAID:
            actions = [[_('Save'), _('Finally Submit')],
                [_('Remove selected tickets')]]
        applicants_utils = getUtility(IApplicantsUtils)
        if self.context.state in applicants_utils.BALANCE_PAYMENT_STATES:
            actions[1].append(_('Add balance payment ticket'))
        return actions

    @property
    def picture_editable(self):
        return self.context.__parent__.picture_editable

    def unremovable(self, ticket):
        return ticket.r_code

    def emit_lock_message(self):
        self.flash(_('The requested form is locked (read-only).'),
                   type='warning')
        self.redirect(self.url(self.context))
        return

    def update(self):
        if self.context.locked or (
            self.context.__parent__.expired and
            self.context.__parent__.strict_deadline):
            self.emit_lock_message()
            return
        super(ApplicantEditFormPage, self).update()
        return

    def dataNotComplete(self, data):
        if self.context.__parent__.with_picture:
            store = getUtility(IExtFileStore)
            if not store.getFileByContext(self.context, attr=u'passport.jpg'):
                return _('No passport picture uploaded.')
            if not self.request.form.get('confirm_passport', False):
                return _('Passport picture confirmation box not ticked.')
        return False

    # We explicitely want the forms to be validated before payment tickets
    # can be created. If no validation is requested, use
    # 'validator=NullValidator' in the action directive
    @action(_('Add online payment ticket'), style='primary')
    def addPaymentTicket(self, **data):
        self.redirect(self.url(self.context, '@@addafp'))
        return

    @action(_('Add balance payment ticket'), style='primary')
    def addBalancePaymentTicket(self, **data):
        self.redirect(self.url(self.context, '@@addbp'))
        return

    @jsaction(_('Remove selected tickets'))
    def removePaymentTickets(self, **data):
        self.delPaymentTickets(**data)
        self.redirect(self.url(self.context) + '/@@edit')
        return

    @action(_('Save'), style='primary')
    def save(self, **data):
        if self.upload_success is False:  # False is not None!
            # Error during image upload. Ignore other values.
            return
        self.applyData(self.context, **data)
        error, dummy = self.saveCourses()
        if error:
            self.flash(error, type='danger')
            return
        self.flash(_('Form has been saved.'))
        return

    def informReferees(self):
        site = grok.getSite()
        kofa_utils = getUtility(IKofaUtils)
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        failed = ''
        emails_sent = 0
        for referee in self.context.referees:
            if referee.email_sent:
                continue
            mandate = RefereeReportMandate(days=self.mandate_days)
            mandate.params['name'] = referee.name
            mandate.params['email'] = referee.email
            mandate.params[
                'redirect_path'] = '/applicants/%s/%s/addrefereereport' % (
                    self.context.__parent__.code,
                    self.context.application_number)
            mandate.params['redirect_path2'] = ''
            mandate.params['applicant_id'] = self.context.applicant_id
            site['mandates'].addMandate(mandate)
            # Send invitation email
            args = {'mandate_id':mandate.mandate_id}
            mandate_url = self.url(site) + '/mandate?%s' % urlencode(args)
            url_info = u'Report link: %s' % mandate_url
            success = kofa_utils.inviteReferee(referee, self.context, url_info)
            if success:
                emails_sent += 1
                self.context.writeLogMessage(
                    self, 'email sent: %s' % referee.email)
                referee.email_sent = True
            else:
                failed += '%s ' % referee.email
        return failed, emails_sent

    @property
    def _finalsubmit_msg(self):
        return _('Form has been submitted.')

    @action(_('Finally Submit'), warning=WARNING)
    def finalsubmit(self, **data):
        if self.upload_success is False:  # False is not None!
            return # error during image upload. Ignore other values
        dnt = self.dataNotComplete(data)
        if dnt:
            self.flash(dnt, type='danger')
            return
        self.applyData(self.context, **data)
        error, dummy = self.saveCourses()
        if error:
            self.flash(error, type='danger')
            return
        state = IWorkflowState(self.context).getState()
        # This shouldn't happen, but the application officer
        # might have forgotten to lock the form after changing the state
        if state != self.submit_state:
            self.flash(_('The form cannot be submitted. Wrong state!'),
                       type='danger')
            return
        msg = self._finalsubmit_msg
        # Create mandates and send emails to referees
        if getattr(self.context, 'referees', None):
            failed, emails_sent = self.informReferees()
            if failed:
                self.flash(
                    _('Some invitation emails could not be sent:') + failed,
                    type='danger')
                return
            msg = _('Form has been successfully submitted and '
                    '${a} invitation emails were sent.',
                    mapping = {'a':  emails_sent})
        IWorkflowInfo(self.context).fireTransition('submit')
        # Send confirmation email
        getUtility(IKofaUtils).informApplicant(self.context)
        # application_date is used in export files for sorting.
        # We can thus store utc.
        self.context.application_date = datetime.utcnow()
        self.flash(msg)
        self.redirect(self.url(self.context))
        return

class PassportImage(grok.View):
    """Renders the passport image for applicants.
    """
    grok.name('passport.jpg')
    grok.context(IApplicant)
    grok.require('waeup.viewApplication')

    def render(self):
        # A filename chooser turns a context into a filename suitable
        # for file storage.
        image = getUtility(IExtFileStore).getFileByContext(self.context)
        self.response.setHeader('Content-Type', 'image/jpeg')
        if image is None:
            # show placeholder image
            return open(DEFAULT_PASSPORT_IMAGE_PATH, 'rb').read()
        return image

class PassportImageForReport(PassportImage):
    """Renders the passport image for applicants for referee reports.
    """
    grok.name('passport_for_report.jpg')
    grok.context(IApplicant)
    grok.require('waeup.Public')

    def render(self):
        # Check mandate
        form = self.request.form
        self.mandate_id = form.get('mandate_id', None)
        self.mandates = grok.getSite()['mandates']
        mandate = self.mandates.get(self.mandate_id, None)
        if mandate is None:
            self.flash(_('No mandate.'), type='warning')
            self.redirect(self.application_url())
            return
        if mandate:
            # Check the mandate expiration date after redirect again
            if mandate.expires < datetime.utcnow():
                self.flash(_('Mandate expired.'),
                           type='warning')
                self.redirect(self.application_url())
                return
            # Check if mandate allows access
            if mandate.params.get('applicant_id') != self.context.applicant_id:
                self.flash(_('Wrong mandate.'),
                           type='warning')
                self.redirect(self.application_url())
                return
            return super(PassportImageForReport, self).render()
        return

class ApplicantRegistrationPage(KofaAddFormPage):
    """Captcha'd registration page for applicants.
    """
    grok.context(IApplicantsContainer)
    grok.name('register')
    grok.require('waeup.Anonymous')
    grok.template('applicantregister')

    @property
    def form_fields(self):
        form_fields = None
        if self.context.mode == 'update':
            form_fields = grok.AutoFields(IApplicantRegisterUpdate).select(
                'lastname','reg_number','email')
        else: #if self.context.mode == 'create':
            form_fields = grok.AutoFields(IApplicantEdit).select(
                'firstname', 'middlename', 'lastname', 'email', 'phone')
        return form_fields

    @property
    def label(self):
        return _('Apply for ${a}',
            mapping = {'a':self.context.title})

    def update(self):
        if self.context.expired:
            self.flash(_('Outside application period.'), type='warning')
            self.redirect(self.url(self.context))
            return
        blocker = grok.getSite()['configuration'].maintmode_enabled_by
        if blocker:
            self.flash(_('The portal is in maintenance mode '
                        'and registration temporarily disabled.'),
                       type='warning')
            self.redirect(self.url(self.context))
            return
        # Handle captcha
        self.captcha = getUtility(ICaptchaManager).getCaptcha()
        self.captcha_result = self.captcha.verify(self.request)
        self.captcha_code = self.captcha.display(self.captcha_result.error_code)
        return

    def _redirect(self, email, password, applicant_id):
        # Forward only email to landing page in base package.
        self.redirect(self.url(self.context, 'registration_complete',
            data = dict(email=email)))
        return

    @property
    def _postfix(self):
        """In customized packages we can add a container dependent string if
        applicants have been imported into several containers.
        """
        return ''

    @action(_('Send login credentials to email address'), style='primary')
    def register(self, **data):
        if not self.captcha_result.is_valid:
            # Captcha will display error messages automatically.
            # No need to flash something.
            return
        if self.context.mode == 'create':
            # Check if there are unused records in this container which
            # can be taken
            applicant = self.context.first_unused
            if applicant is None:
                # Add applicant
                applicant = createObject(u'waeup.Applicant')
                self.context.addApplicant(applicant)
            else:
                applicants_root = grok.getSite()['applicants']
                ob_class = self.__implemented__.__name__.replace(
                    'waeup.kofa.','')
                applicants_root.logger.info('%s - used: %s' % (
                    ob_class, applicant.applicant_id))
            self.applyData(applicant, **data)
            # applicant.reg_number = applicant.applicant_id
            notify(grok.ObjectModifiedEvent(applicant))
        elif self.context.mode == 'update':
            # Update applicant
            reg_number = data.get('reg_number','')
            lastname = data.get('lastname','')
            cat = getUtility(ICatalog, name='applicants_catalog')
            searchstr = reg_number + self._postfix
            results = list(
                cat.searchResults(reg_number=(searchstr, searchstr)))
            if results:
                applicant = results[0]
                if getattr(applicant,'lastname',None) is None:
                    self.flash(_('An error occurred.'), type='danger')
                    return
                elif applicant.lastname.lower() != lastname.lower():
                    # Don't tell the truth here. Anonymous must not
                    # know that a record was found and only the lastname
                    # verification failed.
                    self.flash(
                        _('No application record found.'), type='warning')
                    return
                elif applicant.password is not None and \
                    applicant.state != INITIALIZED:
                    self.flash(_('Your password has already been set and used. '
                                 'Please proceed to the login page.'),
                               type='warning')
                    return
                # Store email address but nothing else.
                applicant.email = data['email']
                notify(grok.ObjectModifiedEvent(applicant))
            else:
                # No record found, this is the truth.
                self.flash(_('No application record found.'), type='warning')
                return
        else:
            # Does not happen but anyway ...
            return
        kofa_utils = getUtility(IKofaUtils)
        password = kofa_utils.genPassword()
        IUserAccount(applicant).setPassword(password)
        # Send email with credentials
        args = {'login':applicant.applicant_id, 'password':password}
        login_url = self.url(grok.getSite()) + '/login?%s' % urlencode(args)
        url_info = u'Login: %s' % login_url
        msg = _('You have successfully been registered for the')
        if kofa_utils.sendCredentials(IUserAccount(applicant),
            password, url_info, msg):
            email_sent = applicant.email
        else:
            email_sent = None
        self._redirect(email=email_sent, password=password,
            applicant_id=applicant.applicant_id)
        return

class ApplicantRegistrationEmailSent(KofaPage):
    """Landing page after successful registration.

    """
    grok.name('registration_complete')
    grok.require('waeup.Public')
    grok.template('applicantregemailsent')
    label = _('Your registration was successful.')

    def update(self, email=None, applicant_id=None, password=None):
        self.email = email
        self.password = password
        self.applicant_id = applicant_id
        return

class ApplicantCheckStatusPage(KofaPage):
    """Captcha'd status checking page for applicants.
    """
    grok.context(IApplicantsRoot)
    grok.name('checkstatus')
    grok.require('waeup.Anonymous')
    grok.template('applicantcheckstatus')
    buttonname = _('Submit')
    pnav = 7

    def label(self):
        if self.result:
            return _('Admission status of ${a}',
                     mapping = {'a':self.applicant.applicant_id})
        return _('Check your admission status')

    def update(self, SUBMIT=None):
        form = self.request.form
        self.result = False
        # Handle captcha
        self.captcha = getUtility(ICaptchaManager).getCaptcha()
        self.captcha_result = self.captcha.verify(self.request)
        self.captcha_code = self.captcha.display(self.captcha_result.error_code)
        if SUBMIT:
            if not self.captcha_result.is_valid:
                # Captcha will display error messages automatically.
                # No need to flash something.
                return
            unique_id = form.get('unique_id', None)
            lastname = form.get('lastname', None)
            if not unique_id or not lastname:
                self.flash(
                    _('Required input missing.'), type='warning')
                return
            cat = getUtility(ICatalog, name='applicants_catalog')
            results = list(
                cat.searchResults(applicant_id=(unique_id, unique_id)))
            if not results:
                results = list(
                    cat.searchResults(reg_number=(unique_id, unique_id)))
            if results:
                applicant = results[0]
                if applicant.lastname.lower().strip() != lastname.lower():
                    # Don't tell the truth here. Anonymous must not
                    # know that a record was found and only the lastname
                    # verification failed.
                    self.flash(
                        _('No application record found.'), type='warning')
                    return
            else:
                self.flash(_('No application record found.'), type='warning')
                return
            self.applicant = applicant
            self.entry_session = "%s/%s" % (
                applicant.__parent__.year,
                applicant.__parent__.year+1)
            course_admitted = getattr(applicant, 'course_admitted', None)
            self.course_admitted = False
            if course_admitted is not None:
                try:
                    self.course_admitted = True
                    self.longtitle = course_admitted.longtitle
                    self.department = course_admitted.__parent__.__parent__.longtitle
                    self.faculty = course_admitted.__parent__.__parent__.__parent__.longtitle
                except AttributeError:
                    self.flash(_('Application record invalid.'), type='warning')
                    return
            self.result = True
            self.admitted = False
            self.not_admitted = False
            self.submitted = False
            self.not_submitted = False
            self.created = False
            if applicant.state in (ADMITTED, CREATED):
                self.admitted = True
            if applicant.state in (CREATED):
                self.created = True
                self.student_id = applicant.student_id
                self.password = applicant.application_number
            if applicant.state in (NOT_ADMITTED,):
                self.not_admitted = True
            if applicant.state in (SUBMITTED,):
                self.submitted = True
            if applicant.state in (INITIALIZED, STARTED, PAID):
                self.not_submitted = True
        return

class CheckTranscriptStatus(KofaPage):
    """A display page for checking transcript processing status.
    """
    grok.context(IApplicantsRoot)
    grok.name('checktranscript')
    grok.require('waeup.Public')
    label = _('Check transcript status')
    buttonname = _('Check status now')
    pnav = 8
    websites = (('DemoPortal', 'https://kofa-demo.waeup.org/'),)
    #websites = (('DemoPortal', 'http://localhost:8080/app/'),)
    appl_url1 = 'https://kofa-demo.waeup.org/applicants'
    appl_url2 = 'https://kofa-demo.waeup.org/applicants'

    def update(self, SUBMIT=None):
        form = self.request.form
        self.button = False
        # Handle captcha
        self.captcha = getUtility(ICaptchaManager).getCaptcha()
        self.captcha_result = self.captcha.verify(self.request)
        self.captcha_code = self.captcha.display(self.captcha_result.error_code)
        if SUBMIT:
            self.results = []
            if not self.captcha_result.is_valid:
                # Captcha will display error messages automatically.
                # No need to flash something.
                return
            unique_id = form.get('unique_id', None)
            email = form.get('email', None)
            if not unique_id or not email:
                self.flash(
                    _('Required input missing.'), type='warning')
                return
            self.button = True
            # Call webservice of all websites
            for website in self.websites:
                server = xmlrpclib.ServerProxy(website[1])
                result = server.get_grad_student(unique_id, email)
                if not result:
                    continue
                self.results.append((result, website))
        return

class ExportJobContainerOverview(KofaPage):
    """Page that lists active applicant data export jobs and provides links
    to discard or download CSV files.

    """
    grok.context(VirtualApplicantsExportJobContainer)
    grok.require('waeup.manageApplication')
    grok.name('index.html')
    grok.template('exportjobsindex')
    label = _('Data Exports')
    pnav = 3

    def update(self, CREATE=None, DISCARD=None, job_id=None):
        if CREATE:
            self.redirect(self.url('@@start_export'))
            return
        if DISCARD and job_id:
            entry = self.context.entry_from_job_id(job_id)
            self.context.delete_export_entry(entry)
            ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
            self.context.logger.info(
                '%s - discarded: job_id=%s' % (ob_class, job_id))
            self.flash(_('Discarded export') + ' %s' % job_id)
        self.entries = doll_up(self, user=self.request.principal.id)
        return

class ExportJobContainerJobStart(UtilityView, grok.View):
    """View that starts three export jobs, one for applicants, a second
    one for applicant payments and a third for referee reports.
    """
    grok.context(VirtualApplicantsExportJobContainer)
    grok.require('waeup.manageApplication')
    grok.name('start_export')

    EXPORTER_LIST = ('applicants',
                   'applicantpayments',
                   'applicantrefereereports')

    def update(self):
        utils = queryUtility(IKofaUtils)
        if not utils.expensive_actions_allowed():
            self.flash(_(
                "Currently, exporters cannot be started due to high "
                "system load. Please try again later."), type='danger')
            self.entries = doll_up(self, user=None)
            return

        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        container_code = self.context.__parent__.code
        # Start first exporter
        for exporter in self.EXPORTER_LIST:
            job_id = self.context.start_export_job(exporter,
                                          self.request.principal.id,
                                          container=container_code)
            self.context.logger.info(
                '%s - exported: %s (%s), job_id=%s'
                % (ob_class, exporter, container_code, job_id))
            # Commit transaction so that job is stored in the ZODB
            transaction.commit()
        self.flash(_('Exports started.'))
        self.redirect(self.url(self.context))
        return

    def render(self):
        return

class ExportJobContainerDownload(ExportCSVView):
    """Page that downloads a students export csv file.

    """
    grok.context(VirtualApplicantsExportJobContainer)
    grok.require('waeup.manageApplication')

class RefereesRemindPage(UtilityView, grok.View):
    """A display view for referee reports.
    """
    grok.context(IApplicant)
    grok.name('remind_referees')
    grok.require('waeup.manageApplication')

    mandate_days = 31

    def remindReferees(self):
        site = grok.getSite()
        kofa_utils = getUtility(IKofaUtils)
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        failed = ''
        emails_sent = 0
        for referee in self.context.referees:
            #if not referee.email_sent:
            #    continue
            # Check if referee has already created a report
            report_exists = False
            for report in self.context.refereereports:
                if report.email == referee.email:
                    report_exists = True
            if report_exists:
                continue
            # If not, create new mandate
            mandate = RefereeReportMandate(days=self.mandate_days)
            mandate.params['name'] = referee.name
            mandate.params['email'] = referee.email
            mandate.params[
                'redirect_path'] = '/applicants/%s/%s/addrefereereport' % (
                    self.context.__parent__.code,
                    self.context.application_number)
            mandate.params['redirect_path2'] = ''
            mandate.params['applicant_id'] = self.context.applicant_id
            site['mandates'].addMandate(mandate)
            # Send invitation email
            args = {'mandate_id':mandate.mandate_id}
            mandate_url = self.url(site) + '/mandate?%s' % urlencode(args)
            url_info = u'Report link: %s' % mandate_url
            success = kofa_utils.inviteReferee(referee, self.context, url_info)
            if success:
                emails_sent += 1
                self.context.writeLogMessage(
                    self, 'email sent: %s' % referee.email)
                referee.email_sent = True
            else:
                failed += '%s ' % referee.email
        return failed, emails_sent

    def update(self):
        if self.context.state != 'submitted':
            self.flash(
                _('Not allowed!'), type='danger')
            return self.redirect(self.url(self.context))
        failed, emails_sent = self.remindReferees()
        msg = _('${a} referee(s) have been reminded by email.',
                mapping = {'a':  emails_sent})
        self.flash(msg)
        return self.redirect(self.url(self.context))

    def render(self):
        return

class RefereeReportDisplayFormPage(KofaDisplayFormPage):
    """A display view for referee reports.
    """
    grok.context(IApplicantRefereeReport)
    grok.name('index')
    grok.require('waeup.manageApplication')
    label = _('Referee Report')
    pnav = 3
    form_fields = grok.AutoFields(IApplicantRefereeReport)
    form_fields[
        'creation_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')

class RefereeReportManageFormPage(KofaEditFormPage):
    """A displaymanage for referee reports.
    """
    grok.context(IApplicantRefereeReport)
    grok.name('manage')
    grok.require('waeup.managePortal')
    label = _('Manage Referee Report')
    pnav = 3
    form_fields = grok.AutoFields(IApplicantRefereeReport).omit('creation_date')

    @action(_('Save'), style='primary')
    def save(self, **data):
        changed_fields = self.applyData(self.context, **data)
        # Turn list of lists into single list
        if changed_fields:
            changed_fields = reduce(lambda x,y: x+y, changed_fields.values())
        else:
            changed_fields = []
        fields_string = ' + '.join(changed_fields)
        self.flash(_('Form has been saved.'))
        if fields_string:
            self.context.__parent__.writeLogMessage(
                self, '%s - saved: %s' % (self.context.r_id, fields_string))
        return

class RemoveRefereeReportPage(UtilityView, grok.View):
    """
    """
    grok.context(IApplicantRefereeReport)
    grok.name('remove')
    grok.require('waeup.manageApplication')

    def update(self):
        redirect_url = self.url(self.context.__parent__)
        self.context.__parent__.writeLogMessage(
            self, 'removed: %s' % self.context.r_id)
        del self.context.__parent__[self.context.r_id]
        self.flash(_('Referee report removed.'))
        self.redirect(redirect_url)
        return

    def render(self):
        return

class RefereeReportAddFormPage(KofaAddFormPage):
    """Add-form to add an referee report. This form
    is protected by a mandate.
    """
    grok.context(IApplicant)
    grok.require('waeup.Public')
    grok.name('addrefereereport')
    form_fields = grok.AutoFields(
        IApplicantRefereeReport).omit('creation_date')
    grok.template('refereereportpage')
    label = _('Referee Report Form')
    pnav = 3
    #doclink = DOCLINK + '/refereereports.html'

    def update(self):
        blocker = grok.getSite()['configuration'].maintmode_enabled_by
        if blocker:
            self.flash(_('The portal is in maintenance mode. '
                        'Referee report forms are temporarily disabled.'),
                       type='warning')
            self.redirect(self.application_url())
            return
        # Check mandate
        form = self.request.form
        self.mandate_id = form.get('mandate_id', None)
        self.mandates = grok.getSite()['mandates']
        mandate = self.mandates.get(self.mandate_id, None)
        if mandate is None and not self.request.form.get('form.actions.submit'):
            self.flash(_('No mandate.'), type='warning')
            self.redirect(self.application_url())
            return
        if mandate:
            # Check the mandate expiration date after redirect again
            if mandate.expires < datetime.utcnow():
                self.flash(_('Mandate expired.'),
                           type='warning')
                self.redirect(self.application_url())
                return
            args = {'mandate_id':mandate.mandate_id}
            # Check if report exists.
            # (1) If mandate has been used to create a report, 
            # redirect to the pdf file.
            if mandate.params.get('redirect_path2'):
                self.redirect(
                    self.application_url() +
                    mandate.params.get('redirect_path2') +
                    '?%s' % urlencode(args))
                return
            # (2) Report exists but was created with another mandate.
            for report in self.context.refereereports:
                if report.email == mandate.params.get('email'):
                    self.flash(_('You have already created a '
                                 'report with another mandate.'),
                               type='warning')
                    self.redirect(self.application_url())
                    return
            # Prefill form with mandate params
            self.form_fields.get(
                'name').field.default = mandate.params['name']
            self.form_fields.get(
                'email_pref').field.default = mandate.params['email']
            self.passport_url = self.url(
                self.context, 'passport_for_report.jpg') + '?%s' % urlencode(args)
        super(RefereeReportAddFormPage, self).update()
        return

    @action(_('Submit'),
              warning=_('Are you really sure? '
                        'Reports can neither be modified or added '
                        'after submission.'),
              style='primary')
    def addRefereeReport(self, **data):
        report = createObject(u'waeup.ApplicantRefereeReport')
        timestamp = ("%d" % int(time()*10000))[1:]
        report.r_id = "r%s" % timestamp
        report.email = self.mandates[self.mandate_id].params['email']
        self.applyData(report, **data)
        self.context[report.r_id] = report
        # self.flash(_('Referee report has been saved. Thank you!'))
        self.context.writeLogMessage(self, 'added: %s' % report.r_id)
        # Changed on 19/04/20: We do no longer delete the mandate
        # but set path to redirect to the pdf file
        self.mandates[self.mandate_id].params[
            'redirect_path2'] = '/applicants/%s/%s/%s/referee_report.pdf' % (
                self.context.__parent__.code,
                self.context.application_number,
                report.r_id)
        notify(grok.ObjectModifiedEvent(self.mandates[self.mandate_id]))
        args = {'mandate_id':self.mandate_id}
        self.flash(_('Your report has been successfully submitted. '
                     'Please use the report link in the email again to download '
                     'a pdf slip of your report.'))
        #self.redirect(self.url(report, 'referee_report.pdf')
        #              + '?%s' % urlencode(args))
        self.redirect(self.application_url())
        return

class ExportPDFReportSlipPage(UtilityView, grok.View):
    """Deliver a PDF slip of the context.
    """
    grok.context(IApplicantRefereeReport)
    grok.name('referee_report_slip.pdf')
    grok.require('waeup.manageApplication')
    form_fields = grok.AutoFields(IApplicantRefereeReport)
    form_fields[
        'creation_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    #prefix = 'form'
    note = None

    @property
    def title(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Referee Report'), 'waeup.kofa',
            target_language=portal_language)

    @property
    def label(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Referee Report Slip'),
            'waeup.kofa', target_language=portal_language) \
            + ' %s' % self.context.r_id

    def render(self):
        applicantview = ApplicantBaseDisplayFormPage(self.context.__parent__,
            self.request)
        students_utils = getUtility(IStudentsUtils)
        return students_utils.renderPDF(self,'referee_report_slip.pdf',
            self.context.__parent__, applicantview, note=self.note)

class ExportPDFReportSlipPage2(ExportPDFReportSlipPage):
    """Deliver a PDF slip of the context to referees.
    """
    grok.name('referee_report.pdf')
    grok.require('waeup.Public')

    def update(self):
        # Check mandate
        form = self.request.form
        self.mandate_id = form.get('mandate_id', None)
        self.mandates = grok.getSite()['mandates']
        mandate = self.mandates.get(self.mandate_id, None)
        if mandate is None:
            self.flash(_('No mandate.'), type='warning')
            self.redirect(self.application_url())
            return
        if mandate:
            # Check the mandate expiration date after redirect again
            if mandate.expires < datetime.utcnow():
                self.flash(_('Mandate expired.'),
                           type='warning')
                self.redirect(self.application_url())
                return
            # Check if form has really been submitted
            if not mandate.params.get('redirect_path2') \
                or mandate.params.get(
                    'applicant_id') != self.context.__parent__.applicant_id:
                self.flash(_('Wrong mandate.'),
                           type='warning')
                self.redirect(self.application_url())
                return
            super(ExportPDFReportSlipPage2, self).update()
        return

class AdditionalFile(grok.View):
    """Renders additional files for applicants.
    This is a baseclass.
    """
    grok.baseclass()
    grok.context(IApplicant)
    grok.require('waeup.viewApplication')

    def render(self):
        #image = getUtility(IExtFileStore).getFileByContext(
        #    self.context, attr=self.download_name)
        file = getUtility(IExtFileStore).getFileByContext(
            self.context, attr=self.__name__)
        dummy,ext = os.path.splitext(file.name)
        if ext == '.jpg':
            self.response.setHeader('Content-Type', 'image/jpeg')
        elif ext == '.pdf':
            self.response.setHeader('Content-Type', 'application/pdf')
        return file

class TestFile(AdditionalFile):
    """Renders testfile.
    """
    grok.name('testfile')