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
"""UI components for students and related components.
"""
import csv
import grok
import pytz
import sys
import os
import textwrap
from cStringIO import StringIO
from datetime import datetime
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from urllib import urlencode
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, getUtility, createObject
from zope.event import notify
from zope.formlib.textwidgets import BytesDisplayWidget
from zope.i18n import translate
from zope.schema.interfaces import ConstraintNotSatisfied, RequiredMissing
from zope.security import checkPermission
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from waeup.kofa.smtp import encode_address
from waeup.kofa.accesscodes import invalidate_accesscode, get_access_code
from waeup.kofa.accesscodes.workflow import USED
from waeup.kofa.browser.pdf import ENTRY1_STYLE
from waeup.kofa.browser.breadcrumbs import Breadcrumb
from waeup.kofa.browser.interfaces import ICaptchaManager
from waeup.kofa.browser.layout import (
    KofaPage, KofaFormPage, KofaEditFormPage, KofaAddFormPage, KofaDisplayFormPage,
    NullValidator, jsaction, action, UtilityView)
from waeup.kofa.browser.pages import (
    ContactAdminFormPage, ExportCSVView, doll_up, exports_not_allowed,
    LocalRoleAssignmentUtilityView)
from waeup.kofa.hostels.hostel import NOT_OCCUPIED
from waeup.kofa.interfaces import (
    IKofaObject, IUserAccount, IExtFileStore, IPasswordValidator, IContactForm,
    IKofaUtils, IObjectHistory, academic_sessions, ICSVExporter,
    academic_sessions_vocab, IDataCenter, DOCLINK)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.mandates.mandate import PasswordMandate, ParentsPasswordMandate
from waeup.kofa.university.interfaces import (
    IDepartment, ICertificate, ICourse, IFlashNotice)
from waeup.kofa.university.certificate import (
    VirtualCertificateExportJobContainer)
from waeup.kofa.university.department import (
    VirtualDepartmentExportJobContainer)
from waeup.kofa.university.faculty import VirtualFacultyExportJobContainer
from waeup.kofa.university.facultiescontainer import (
    VirtualFacultiesExportJobContainer)
from waeup.kofa.university.course import (
    VirtualCourseExportJobContainer,)
from waeup.kofa.university.vocabularies import course_levels
from waeup.kofa.utils.batching import VirtualExportJobContainer
from waeup.kofa.utils.helpers import get_current_principal, now
from waeup.kofa.widgets.datewidget import FriendlyDatetimeDisplayWidget
from waeup.kofa.students.interfaces import (
    IStudentsContainer, IStudent, IUGStudentClearance, IPGStudentClearance,
    IStudentPersonal, IStudentPersonalEdit, IStudentBase, IStudentStudyCourse,
    IStudentStudyCourseTransfer,
    IStudentAccommodation, IStudentStudyLevel, ICourseTicket, ICourseTicketAdd,
    IStudentPaymentsContainer, IStudentOnlinePayment, IStudentPreviousPayment,
    IStudentBalancePayment, IBedTicket, IStudentsUtils, IStudentRequestPW,
    )
from waeup.kofa.students.catalog import search, StudentQueryResultItem
from waeup.kofa.students.vocabularies import StudyLevelSource
from waeup.kofa.students.workflow import (
    ADMITTED, PAID, CLEARANCE, REQUESTED, RETURNING, CLEARED, REGISTERED,
    VALIDATED, GRADUATED, TRANSREQ, TRANSVAL, TRANSREL, FORBIDDEN_POSTGRAD_TRANS
    )


grok.context(IKofaObject)  # Make IKofaObject the default context


class TicketError(Exception):
    """A course ticket could not be added
    """
    pass

# Save function used for save methods in pages
def msave(view, **data):
    changed_fields = view.applyData(view.context, **data)
    # Turn list of lists into single list
    if changed_fields:
        changed_fields = reduce(lambda x, y: x+y, changed_fields.values())
    # Inform catalog if certificate has changed
    # (applyData does this only for the context)
    if 'certificate' in changed_fields:
        notify(grok.ObjectModifiedEvent(view.context.student))
    fields_string = ' + '.join(changed_fields)
    view.flash(_('Form has been saved.'))
    if fields_string:
        view.context.writeLogMessage(view, 'saved: %s' % fields_string)
    return

def emit_lock_message(view, msg=None):
    """Flash a lock message.
    """
    if msg:
        view.flash(msg, type="warning")
        view.redirect(view.url(view.context))
        return
    view.flash(_('The requested form is locked (read-only).'), type="warning")
    view.redirect(view.url(view.context))
    return

def translated_values(view):
    """Translate course ticket attribute values to be displayed on
    studylevel pages.
    """
    lang = view.request.cookies.get('kofa.language')
    for value in view.context.values():
        # We have to unghostify (according to Tres Seaver) the __dict__
        # by activating the object, otherwise value_dict will be empty
        # when calling the first time.
        value._p_activate()
        value_dict = dict([i for i in value.__dict__.items()])
        value_dict['url'] = view.url(value)
        value_dict['removable_by_student'] = value.removable_by_student
        value_dict['mandatory'] = translate(str(value.mandatory), 'zope',
            target_language=lang)
        value_dict['carry_over'] = translate(str(value.carry_over), 'zope',
            target_language=lang)
        value_dict['outstanding'] = translate(str(value.outstanding), 'zope',
            target_language=lang)
        value_dict['automatic'] = translate(str(value.automatic), 'zope',
            target_language=lang)
        value_dict['grade'] = value.grade
        value_dict['weight'] = value.weight
        value_dict['course_category'] = value.course_category
        value_dict['total_score'] = value.total_score
        semester_dict = getUtility(IKofaUtils).SEMESTER_DICT
        value_dict['semester'] = semester_dict[
            value.semester].replace('mester', 'm.')
        yield value_dict

def addCourseTicket(view, course=None):
    students_utils = getUtility(IStudentsUtils)
    ticket = createObject(u'waeup.CourseTicket')
    ticket.automatic = False
    ticket.carry_over = False
    warning = students_utils.warnCreditsOOR(view.context, course)
    if warning:
        view.flash(warning, type="warning")
        return False
    warning = students_utils.warnCourseAlreadyPassed(view.context, course)
    if warning:
        view.flash(warning, type="warning")
        return False
    try:
        view.context.addCourseTicket(ticket, course)
    except KeyError:
        view.flash(_('The ticket exists.'), type="warning")
        return False
    except TicketError, error:
        # Ticket errors are not being raised in the base package.
        view.flash(error, type="warning")
        return False
    view.flash(_('Successfully added ${a}.',
        mapping = {'a':ticket.code}))
    view.context.writeLogMessage(
        view,'added: %s|%s|%s' % (
        ticket.code, ticket.level, ticket.level_session))
    return True

def level_dict(studycourse):
    portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
    level_dict = {}
    studylevelsource = StudyLevelSource().factory
    for code in studylevelsource.getValues(studycourse):
        title = translate(studylevelsource.getTitle(studycourse, code),
            'waeup.kofa', target_language=portal_language)
        level_dict[code] = title
    return level_dict

class StudentsBreadcrumb(Breadcrumb):
    """A breadcrumb for the students container.
    """
    grok.context(IStudentsContainer)
    title = _('Students')

    @property
    def target(self):
        user = get_current_principal()
        if getattr(user, 'user_type', None) == 'student':
            return None
        return self.viewname

class StudentBreadcrumb(Breadcrumb):
    """A breadcrumb for the student container.
    """
    grok.context(IStudent)

    def title(self):
        return self.context.display_fullname

class SudyCourseBreadcrumb(Breadcrumb):
    """A breadcrumb for the student study course.
    """
    grok.context(IStudentStudyCourse)

    def title(self):
        if self.context.is_current:
            return _('Study Course')
        else:
            return _('Previous Study Course')

class PaymentsBreadcrumb(Breadcrumb):
    """A breadcrumb for the student payments folder.
    """
    grok.context(IStudentPaymentsContainer)
    title = _('Payments')

class OnlinePaymentBreadcrumb(Breadcrumb):
    """A breadcrumb for payments.
    """
    grok.context(IStudentOnlinePayment)

    @property
    def title(self):
        return self.context.p_id

class AccommodationBreadcrumb(Breadcrumb):
    """A breadcrumb for the student accommodation folder.
    """
    grok.context(IStudentAccommodation)
    title = _('Accommodation')

class BedTicketBreadcrumb(Breadcrumb):
    """A breadcrumb for bed tickets.
    """
    grok.context(IBedTicket)

    @property
    def title(self):
        return _('Bed Ticket ${a}',
            mapping = {'a':self.context.getSessionString()})

class StudyLevelBreadcrumb(Breadcrumb):
    """A breadcrumb for course lists.
    """
    grok.context(IStudentStudyLevel)

    @property
    def title(self):
        return self.context.level_title

class StudentsContainerPage(KofaPage):
    """The standard view for student containers.
    """
    grok.context(IStudentsContainer)
    grok.name('index')
    grok.require('waeup.viewStudentsContainer')
    grok.template('containerpage')
    label = _('Find students')
    search_button = _('Find student(s)')
    pnav = 4

    def update(self, *args, **kw):
        prefix = getUtility(IStudentsUtils).STUDENT_ID_PREFIX
        self.curr_stud_id = "%s%s" % (
            prefix, self.context._curr_stud_id - 1)
        form = self.request.form
        self.hitlist = []
        if form.get('searchtype', None) in (
            'suspended', TRANSREQ, TRANSVAL, GRADUATED):
            self.searchtype = form['searchtype']
            self.searchterm = None
        elif 'searchterm' in form and form['searchterm']:
            self.searchterm = form['searchterm']
            self.searchtype = form['searchtype']
        elif 'old_searchterm' in form:
            self.searchterm = form['old_searchterm']
            self.searchtype = form['old_searchtype']
        else:
            if 'search' in form:
                self.flash(_('Empty search string'), type="warning")
            return
        if self.searchtype == 'current_session':
            try:
                self.searchterm = int(self.searchterm)
            except ValueError:
                self.flash(_('Only year dates allowed (e.g. 2011).'),
                           type="danger")
                return
        self.hitlist = search(query=self.searchterm,
            searchtype=self.searchtype, view=self)
        if not self.hitlist:
            self.flash(_('No student found.'), type="warning")
        return

class StudentsContainerManagePage(KofaPage):
    """The manage page for student containers.
    """
    grok.context(IStudentsContainer)
    grok.name('manage')
    grok.require('waeup.manageStudent')
    grok.template('containermanagepage')
    pnav = 4
    label = _('Manage students section')
    search_button = _('Find student(s)')
    remove_button = _('Remove selected')
    send_email_button = _('Send bulk email')
    doclink = DOCLINK + '/students.html'

    def update(self, *args, **kw):
        form = self.request.form
        self.hitlist = []
        if form.get('searchtype', None) in (
            'suspended', TRANSREQ, TRANSVAL, GRADUATED):
            self.searchtype = form['searchtype']
            self.searchterm = None
        elif 'searchterm' in form and form['searchterm']:
            self.searchterm = form['searchterm']
            self.searchtype = form['searchtype']
        elif 'old_searchterm' in form:
            self.searchterm = form['old_searchterm']
            self.searchtype = form['old_searchtype']
        else:
            if 'search' in form:
                self.flash(_('Empty search string'), type="warning")
            return
        if self.searchtype == 'current_session':
            try:
                self.searchterm = int(self.searchterm)
            except ValueError:
                self.flash(_('Only year dates allowed (e.g. 2011).'),
                           type="danger")
                return
        if not 'entries' in form:
            self.hitlist = search(query=self.searchterm,
                searchtype=self.searchtype, view=self)
            if not self.hitlist:
                self.flash(_('No student found.'), type="warning")
            if 'remove' in form or 'send_email' in form:
                self.flash(_('No item selected.'), type="warning")
            return
        entries = form['entries']
        if isinstance(entries, basestring):
            entries = [entries]
        entries.sort()
        if 'send_email' in form and len(entries)>50:
            self.flash(_(
                'Maximum of 50 emails can be sent. Please select less students.'),
                type="warning")
            return
        deleted = []
        emails_tobesent = []
        for entry in entries:
            if 'remove' in form:
                del self.context[entry]
                deleted.append(entry)
            if 'send_email' in form and self.context[entry].email:
                emails_tobesent.append((
                    self.context[entry].email,
                    self.context[entry].student_id))
        if 'send_email' in form and not len(emails_tobesent):
            self.flash(_('No email address found.'), type="warning")
            return
        if len(emails_tobesent):
            args = {'bcc_to': emails_tobesent}
            self.redirect(self.url(self.context) +
                '/send_bulk_email?%s' % urlencode(args))
            return
        self.hitlist = search(query=self.searchterm,
            searchtype=self.searchtype, view=self)
        if len(deleted):
            self.flash(_('Successfully removed: ${a}',
                mapping = {'a':', '.join(deleted)}))
        return

class StudentAddFormPage(KofaAddFormPage):
    """Add-form to add a student.
    """
    grok.context(IStudentsContainer)
    grok.require('waeup.manageStudent')
    grok.name('addstudent')
    form_fields = grok.AutoFields(IStudent).select(
        'firstname', 'middlename', 'lastname', 'reg_number')
    label = _('Add student')
    pnav = 4

    @action(_('Create student'), style='primary')
    def addStudent(self, **data):
        student = createObject(u'waeup.Student')
        self.applyData(student, **data)
        self.context.addStudent(student)
        self.flash(_('Student record created.'))
        self.redirect(self.url(self.context[student.student_id], 'index'))
        return

    @action(_('Create graduated student'), style='primary')
    def addGraduatedStudent(self, **data):
        student = createObject(u'waeup.Student')
        self.applyData(student, **data)
        self.context.addStudent(student)
        IWorkflowState(student).setState(GRADUATED)
        notify(grok.ObjectModifiedEvent(student))
        history = IObjectHistory(student)
        history.addMessage("State 'graduated' set")
        self.flash(_('Graduated student record created.'))
        self.redirect(self.url(self.context[student.student_id], 'index'))
        return

class LoginAsStudentStep1(KofaEditFormPage):
    """ View to temporarily set a student password.
    """
    grok.context(IStudent)
    grok.name('loginasstep1')
    grok.require('waeup.loginAsStudent')
    grok.template('loginasstep1')
    pnav = 4

    def update(self):
        super(LoginAsStudentStep1, self).update()
        kofa_utils = getUtility(IKofaUtils)
        self.temp_password_minutes = kofa_utils.TEMP_PASSWORD_MINUTES
        return

    def label(self):
        return _(u'Set temporary password for ${a}',
            mapping = {'a':self.context.display_fullname})

    @action('Set password now', style='primary')
    def setPassword(self, *args, **data):
        kofa_utils = getUtility(IKofaUtils)
        password = kofa_utils.genPassword()
        self.context.setTempPassword(self.request.principal.id, password)
        self.context.writeLogMessage(
            self, 'temp_password generated: %s' % password)
        args = {'password':password}
        self.redirect(self.url(self.context) +
            '/loginasstep2?%s' % urlencode(args))
        return

class LoginAsStudentStep2(KofaPage):
    """ View to temporarily login as student with a temporary password.
    """
    grok.context(IStudent)
    grok.name('loginasstep2')
    grok.require('waeup.Public')
    grok.template('loginasstep2')
    login_button = _('Login now')
    pnav = 4

    def label(self):
        return _(u'Login as ${a}',
            mapping = {'a':self.context.student_id})

    def update(self, SUBMIT=None, password=None):
        self.password = password
        if SUBMIT is not None:
            self.flash(_('You successfully logged in as student.'))
            self.redirect(self.url(self.context))
        return

class StudentBaseDisplayFormPage(KofaDisplayFormPage):
    """ Page to display student base data
    """
    grok.context(IStudent)
    grok.name('index')
    grok.require('waeup.viewStudent')
    grok.template('basepage')
    form_fields = grok.AutoFields(IStudentBase).omit(
        'password', 'suspended', 'suspended_comment', 'flash_notice')
    pnav = 4

    @property
    def label(self):
        if self.context.suspended:
            return _('${a}: Base Data (account deactivated)',
                mapping = {'a':self.context.display_fullname})
        return  _('${a}: Base Data',
            mapping = {'a':self.context.display_fullname})

    @property
    def hasPassword(self):
        if self.context.password:
            return _('set')
        return _('unset')

    def update(self):
        if self.context.flash_notice:
            self.flash(self.context.flash_notice, type="warning")
        super(StudentBaseDisplayFormPage, self).update()
        return

class StudentBasePDFFormPage(KofaDisplayFormPage):
    """ Page to display student base data in pdf files.
    """

    def __init__(self, context, request, omit_fields=()):
        self.omit_fields = omit_fields
        super(StudentBasePDFFormPage, self).__init__(context, request)

    @property
    def form_fields(self):
        form_fields = grok.AutoFields(IStudentBase)
        for field in self.omit_fields:
            form_fields = form_fields.omit(field)
        return form_fields

class ContactStudentFormPage(ContactAdminFormPage):
    grok.context(IStudent)
    grok.name('contactstudent')
    grok.require('waeup.viewStudent')
    pnav = 4
    form_fields = grok.AutoFields(IContactForm).select('subject', 'body')

    def update(self, subject=u'', body=u''):
        super(ContactStudentFormPage, self).update()
        self.form_fields.get('subject').field.default = subject
        self.form_fields.get('body').field.default = body
        return

    def label(self):
        return _(u'Send message to ${a}',
            mapping = {'a':self.context.display_fullname})

    @action('Send message now', style='primary')
    def send(self, *args, **data):
        try:
            email = self.request.principal.email
        except AttributeError:
            email = self.config.email_admin
        usertype = getattr(self.request.principal,
                           'user_type', 'system').title()
        kofa_utils = getUtility(IKofaUtils)
        success = kofa_utils.sendContactForm(
                self.request.principal.title,email,
                self.context.display_fullname,self.context.email,
                self.request.principal.id,usertype,
                self.config.name,
                data['body'],data['subject'])
        if success:
            self.flash(_('Your message has been sent.'))
        else:
            self.flash(_('An smtp server error occurred.'), type="danger")
        return

class SendBulEmailsFormPage(ContactAdminFormPage):
    grok.context(IStudentsContainer)
    grok.name('send_bulk_email')
    grok.require('waeup.manageStudent')
    pnav = 4
    form_fields = grok.AutoFields(IContactForm).select('subject', 'body', 'bcc_to')
    label = _('Send bulk email')

    def update(self, bcc_to=u''):
        self.form_fields.get('bcc_to').field.default = bcc_to
        return

    @action('Send message now', style='primary')
    def send(self, *args, **data):
        try:
            email = self.request.principal.email
        except AttributeError:
            email = self.config.email_admin
        usertype = getattr(self.request.principal,
                           'user_type', 'system').title()
        kofa_utils = getUtility(IKofaUtils)
        success = kofa_utils.sendContactForm(
                self.request.principal.title,email,
                self.request.principal.title,email, # sent to the sender's address
                self.request.principal.id,usertype,
                self.config.name,
                data['body'],data['subject'],
                eval(data['bcc_to'])
                )
        if success:
            self.flash(_('Your message has been sent.'))
        else:
            self.flash(_('An smtp server error occurred.'), type="danger")
        return

class ExportPDFAdmissionSlip(UtilityView, grok.View):
    """Deliver a PDF Admission slip.
    """
    grok.context(IStudent)
    grok.name('admission_slip.pdf')
    grok.require('waeup.viewStudent')
    prefix = 'form'

    omit_fields = ('date_of_birth', 'current_level')

    form_fields = grok.AutoFields(IStudentBase).select('student_id', 'reg_number')


    # Can be used for testing. Just replace 'post_text=None'
    # by post_text=self.post_text'
    post_text = '''
Conratulations!


<img src="${test_signature_img_path}" valign="-20" height="38" width="86" />


John Tester
- Registrar -
'''

    @property
    def label(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Admission Letter of'),
            'waeup.kofa', target_language=portal_language) \
            + ' %s' % self.context.display_fullname

    def render(self):
        students_utils = getUtility(IStudentsUtils)
        letterhead_path = os.path.join(
            os.path.dirname(__file__), 'static', 'letterhead_admission.jpg')
        if not os.path.exists(letterhead_path):
            letterhead_path = None
        return students_utils.renderPDFAdmissionLetter(self,
            self.context.student, omit_fields=self.omit_fields,
            letterhead_path=letterhead_path, post_text=None)

class StudentBaseManageFormPage(KofaEditFormPage):
    """ View to manage student base data
    """
    grok.context(IStudent)
    grok.name('manage_base')
    grok.require('waeup.manageStudent')
    form_fields = grok.AutoFields(IStudentBase).omit(
        'student_id', 'adm_code', 'suspended')
    grok.template('basemanagepage')
    label = _('Manage base data')
    pnav = 4

    def update(self):
        super(StudentBaseManageFormPage, self).update()
        self.wf_info = IWorkflowInfo(self.context)
        return

    @action(_('Save'), style='primary')
    def save(self, **data):
        form = self.request.form
        password = form.get('password', None)
        password_ctl = form.get('control_password', None)
        if password:
            validator = getUtility(IPasswordValidator)
            errors = validator.validate_password(password, password_ctl)
            if errors:
                self.flash( ' '.join(errors), type="danger")
                return
        changed_fields = self.applyData(self.context, **data)
        # Turn list of lists into single list
        if changed_fields:
            changed_fields = reduce(lambda x,y: x+y, changed_fields.values())
        else:
            changed_fields = []
        if password:
            # Now we know that the form has no errors and can set password
            IUserAccount(self.context).setPassword(password)
            changed_fields.append('password')
        fields_string = ' + '.join(changed_fields)
        self.flash(_('Form has been saved.'))
        if fields_string:
            self.context.writeLogMessage(self, 'saved: % s' % fields_string)
        return

class StudentTriggerTransitionFormPage(KofaEditFormPage):
    """ View to trigger student workflow transitions
    """
    grok.context(IStudent)
    grok.name('trigtrans')
    grok.require('waeup.triggerTransition')
    grok.template('trigtrans')
    label = _('Trigger registration transition')
    pnav = 4

    def getTransitions(self):
        """Return a list of dicts of allowed transition ids and titles.

        Each list entry provides keys ``name`` and ``title`` for
        internal name and (human readable) title of a single
        transition.
        """
        wf_info = IWorkflowInfo(self.context)
        allowed_transitions = [t for t in wf_info.getManualTransitions()
            if not t[0].startswith('pay')]
        if self.context.is_postgrad and not self.context.is_special_postgrad:
            allowed_transitions = [t for t in allowed_transitions
                if not t[0] in FORBIDDEN_POSTGRAD_TRANS]
        return [dict(name='', title=_('No transition'))] +[
            dict(name=x, title=y) for x, y in allowed_transitions]

    @action(_('Save'), style='primary')
    def save(self, **data):
        form = self.request.form
        if 'transition' in form and form['transition']:
            transition_id = form['transition']
            wf_info = IWorkflowInfo(self.context)
            wf_info.fireTransition(transition_id)
        return

class StudentActivateView(UtilityView, grok.View):
    """ Activate student account
    """
    grok.context(IStudent)
    grok.name('activate')
    grok.require('waeup.manageStudent')

    def update(self):
        self.context.suspended = False
        self.context.writeLogMessage(self, 'account activated')
        history = IObjectHistory(self.context)
        history.addMessage('Student account activated')
        self.flash(_('Student account has been activated.'))
        self.redirect(self.url(self.context))
        return

    def render(self):
        return

class StudentDeactivateView(UtilityView, grok.View):
    """ Deactivate student account
    """
    grok.context(IStudent)
    grok.name('deactivate')
    grok.require('waeup.manageStudent')

    def update(self):
        self.context.suspended = True
        self.context.writeLogMessage(self, 'account deactivated')
        history = IObjectHistory(self.context)
        history.addMessage('Student account deactivated')
        self.flash(_('Student account has been deactivated.'))
        self.redirect(self.url(self.context))
        return

    def render(self):
        return

class StudentClearanceDisplayFormPage(KofaDisplayFormPage):
    """ Page to display student clearance data
    """
    grok.context(IStudent)
    grok.name('view_clearance')
    grok.require('waeup.viewStudent')
    pnav = 4

    @property
    def separators(self):
        return getUtility(IStudentsUtils).SEPARATORS_DICT

    @property
    def form_fields(self):
        if self.context.is_postgrad:
            form_fields = grok.AutoFields(IPGStudentClearance)
        else:
            form_fields = grok.AutoFields(IUGStudentClearance)
        if not getattr(self.context, 'officer_comment'):
            form_fields = form_fields.omit('officer_comment')
        else:
            form_fields['officer_comment'].custom_widget = BytesDisplayWidget
        return form_fields

    @property
    def label(self):
        return _('${a}: Clearance Data',
            mapping = {'a':self.context.display_fullname})

class ExportPDFStudyCourseBaseDataSlip(UtilityView, grok.View):
    """Deliver a PDF base and studycourse data slip.
    """
    grok.context(IStudentStudyCourse)
    grok.name('studycourse_slip.pdf')
    grok.require('waeup.viewStudent')
    prefix = 'form'

    omit_fields = (
        'suspended',
        'adm_code', 'suspended_comment',
        'current_level',
        'flash_notice', 'entry_session',
        'parents_email')

    form_fields = grok.AutoFields(IStudentStudyCourse).omit('certificate')

    @property
    def title(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Current Study Course Data'), 'waeup.kofa',
            target_language=portal_language)

    @property
    def label(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Study Course Data of'),
            'waeup.kofa', target_language=portal_language) \
            + ' %s' % self.context.student.display_fullname

    def render(self):
        studentview = StudentBasePDFFormPage(self.context.student,
            self.request, self.omit_fields)
        students_utils = getUtility(IStudentsUtils)
        return students_utils.renderPDF(
            self, 'basedata_slip.pdf',
            self.context.student, studentview, 
            omit_fields=self.omit_fields)

class ExportPDFPersonalDataSlip(UtilityView, grok.View):
    """Deliver a PDF base and personal data slip.
    """
    grok.context(IStudent)
    grok.name('personal_slip.pdf')
    grok.require('waeup.viewStudent')
    prefix = 'form'

    omit_fields = (
        'suspended',
        'adm_code', 'suspended_comment',
        'current_level',
        'flash_notice', 'entry_session',
        'parents_email')

    form_fields = grok.AutoFields(IStudentPersonal)

    @property
    def title(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Personal Data'), 'waeup.kofa',
            target_language=portal_language)

    @property
    def label(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Personal Data of'),
            'waeup.kofa', target_language=portal_language) \
            + ' %s' % self.context.student.display_fullname

    def render(self):
        studentview = StudentBasePDFFormPage(self.context.student,
            self.request, self.omit_fields)
        students_utils = getUtility(IStudentsUtils)
        return students_utils.renderPDF(
            self, 'personal_slip.pdf',
            self.context.student, studentview,
            omit_fields=self.omit_fields)


class ExportPDFClearanceSlip(grok.View):
    """Deliver a PDF slip of the context.
    """
    grok.context(IStudent)
    grok.name('clearance_slip.pdf')
    grok.require('waeup.viewStudent')
    prefix = 'form'
    omit_fields = (
        'suspended', 'phone',
        'adm_code', 'suspended_comment',
        'date_of_birth', 'current_level',
        'flash_notice')

    @property
    def form_fields(self):
        if self.context.is_postgrad:
            form_fields = grok.AutoFields(IPGStudentClearance)
        else:
            form_fields = grok.AutoFields(IUGStudentClearance)
        if not getattr(self.context, 'officer_comment'):
            form_fields = form_fields.omit('officer_comment')
        return form_fields

    @property
    def title(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Clearance Data'), 'waeup.kofa',
            target_language=portal_language)

    @property
    def label(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Clearance Slip of'),
            'waeup.kofa', target_language=portal_language) \
            + ' %s' % self.context.display_fullname

    # XXX: not used in waeup.kofa and thus not tested
    def _signatures(self):
        isStudent = getattr(
            self.request.principal, 'user_type', None) == 'student'
        if not isStudent and self.context.state in (CLEARED, ):
            return ([_('Student Signature')],
                    [_('Clearance Officer Signature')])
        return

    def _sigsInFooter(self):
        isStudent = getattr(
            self.request.principal, 'user_type', None) == 'student'
        if not isStudent and self.context.state in (CLEARED, ):
            return (_('Date, Student Signature'),
                    _('Date, Clearance Officer Signature'),
                    )
        return ()

    def render(self):
        studentview = StudentBasePDFFormPage(self.context.student,
            self.request, self.omit_fields)
        students_utils = getUtility(IStudentsUtils)
        return students_utils.renderPDF(
            self, 'clearance_slip.pdf',
            self.context.student, studentview, signatures=self._signatures(),
            sigs_in_footer=self._sigsInFooter(),
            omit_fields=self.omit_fields)

class StudentClearanceManageFormPage(KofaEditFormPage):
    """ Page to manage student clearance data
    """
    grok.context(IStudent)
    grok.name('manage_clearance')
    grok.require('waeup.manageStudent')
    grok.template('clearanceeditpage')
    label = _('Manage clearance data')
    deletion_warning = _('Are you sure?')
    pnav = 4

    @property
    def separators(self):
        return getUtility(IStudentsUtils).SEPARATORS_DICT

    @property
    def form_fields(self):
        if self.context.is_postgrad:
            form_fields = grok.AutoFields(IPGStudentClearance).omit('clr_code')
        else:
            form_fields = grok.AutoFields(IUGStudentClearance).omit('clr_code')
        return form_fields

    @property
    def do_not_render_buttons(self):
        if self.context.state != CLEARANCE:
            return ('Save and request clearance',)
        return ()

    @action(_('Save'), style='primary')
    def save(self, **data):
        msave(self, **data)
        return

class StudentClearView(UtilityView, grok.View):
    """ Clear student by clearance officer
    """
    grok.context(IStudent)
    grok.name('clear')
    grok.require('waeup.clearStudent')

    def update(self):
        cdm = getUtility(IStudentsUtils).clearance_disabled_message(
            self.context)
        if cdm:
            self.flash(cdm)
            self.redirect(self.url(self.context,'view_clearance'))
            return
        if self.context.state == REQUESTED:
            IWorkflowInfo(self.context).fireTransition('clear')
            self.flash(_('Student has been cleared.'))
        else:
            self.flash(_('Student is in wrong state.'), type="warning")
        self.redirect(self.url(self.context,'view_clearance'))
        return

    def render(self):
        return

class StudentTempClearancePage(KofaEditFormPage):
    """ Temporarily clearance by clearance officers.
    """
    grok.context(IStudent)
    grok.name('temp_clearance')
    label = _('Clear student temporarily')
    grok.require('waeup.clearStudent')
    form_fields = grok.AutoFields(
        IUGStudentClearance).select('officer_comment')

    def update(self):
        cdm = getUtility(IStudentsUtils).clearance_disabled_message(
            self.context)
        if cdm:
            self.flash(cdm, type="warning")
            self.redirect(self.url(self.context,'view_clearance'))
            return
        return super(StudentTempClearancePage, self).update()

    @action(_('Save comment and clear student temporarily now'), style='primary')
    def temp_clear(self, **data):
        if self.context.state == REQUESTED:
            if self.context.officer_comment \
                and self.context.officer_comment.startswith('Temporarily cleared'):
                self.flash(
                    _('Not allowed: student has already been '
                      'temporarily cleared.'),
                    type="warning")
                self.redirect(self.url(self.context,'view_clearance'))
                return
            if not data['officer_comment']:
                self.flash(_('Please write a comment.'), type="warning")
                self.redirect(self.url(self.context,'view_clearance'))
                return
            message = _('Student has been temporarily cleared.')
            self.flash(message)
        else:
            self.flash(_('Student is in wrong state.'), type="warning")
            self.redirect(self.url(self.context,'view_clearance'))
            return
        user = get_current_principal()
        if user is None:
            usertitle = 'system'
        else:
            usertitle = getattr(user, 'public_name', None)
            if not usertitle:
                usertitle = user.title
        comment = data['officer_comment']
        data['officer_comment'] = translate(
            _('Temporarily cleared by ${a}. Officer\'s comment:\n${b}',
            mapping = {'a':usertitle, 'b':comment}))
        self.applyData(self.context, **data)
        self.context.writeLogMessage(
            self, 'comment: %s' % comment.replace('\n', '<br>'))
        args = {'subject':'You have been temporarily cleared.', 'body':comment}
        self.redirect(self.url(self.context) +
            '/contactstudent?%s' % urlencode(args))
        return

class StudentRejectClearancePage(KofaEditFormPage):
    """ Reject clearance by clearance officers.
    """
    grok.context(IStudent)
    grok.name('reject_clearance')
    label = _('Reject clearance')
    grok.require('waeup.clearStudent')
    form_fields = grok.AutoFields(
        IUGStudentClearance).select('officer_comment')

    def update(self):
        cdm = getUtility(IStudentsUtils).clearance_disabled_message(
            self.context)
        if cdm:
            self.flash(cdm, type="warning")
            self.redirect(self.url(self.context,'view_clearance'))
            return
        return super(StudentRejectClearancePage, self).update()

    @action(_('Save comment and reject clearance now'), style='primary')
    def reject(self, **data):
        if self.context.state == CLEARED:
            IWorkflowInfo(self.context).fireTransition('reset4')
            message = _('Clearance has been annulled.')
            self.flash(message, type="warning")
        elif self.context.state == REQUESTED:
            IWorkflowInfo(self.context).fireTransition('reset3')
            message = _('Clearance request has been rejected.')
            self.flash(message, type="warning")
        else:
            self.flash(_('Student is in wrong state.'), type="warning")
            self.redirect(self.url(self.context,'view_clearance'))
            return
        self.applyData(self.context, **data)
        comment = data['officer_comment']
        if comment:
            self.context.writeLogMessage(
                self, 'comment: %s' % comment.replace('\n', '<br>'))
            args = {'subject':message, 'body':comment}
        else:
            args = {'subject':message,}
        self.redirect(self.url(self.context) +
            '/contactstudent?%s' % urlencode(args))
        return


class StudentPersonalDisplayFormPage(KofaDisplayFormPage):
    """ Page to display student personal data
    """
    grok.context(IStudent)
    grok.name('view_personal')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(IStudentPersonal)
    form_fields['perm_address'].custom_widget = BytesDisplayWidget
    form_fields[
        'personal_updated'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    pnav = 4

    @property
    def label(self):
        return _('${a}: Personal Data',
            mapping = {'a':self.context.display_fullname})

class StudentPersonalManageFormPage(KofaEditFormPage):
    """ Page to manage personal data
    """
    grok.context(IStudent)
    grok.name('manage_personal')
    grok.require('waeup.manageStudent')
    form_fields = grok.AutoFields(IStudentPersonal)
    form_fields['personal_updated'].for_display = True
    form_fields[
        'personal_updated'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    label = _('Manage personal data')
    pnav = 4

    @action(_('Save'), style='primary')
    def save(self, **data):
        msave(self, **data)
        return

class StudentPersonalEditFormPage(KofaEditFormPage):
    """ Page to edit personal data
    """
    grok.context(IStudent)
    grok.name('edit_personal')
    grok.require('waeup.handleStudent')
    form_fields = grok.AutoFields(IStudentPersonalEdit).omit('personal_updated')
    label = _('Edit personal data')
    pnav = 4

    @action(_('Save/Confirm'), style='primary')
    def save(self, **data):
        msave(self, **data)
        self.context.personal_updated = datetime.utcnow()
        return

class StudyCourseDisplayFormPage(KofaDisplayFormPage):
    """ Page to display the student study course data
    """
    grok.context(IStudentStudyCourse)
    grok.name('index')
    grok.require('waeup.viewStudent')
    grok.template('studycoursepage')
    pnav = 4

    @property
    def form_fields(self):
        if self.context.is_postgrad:
            form_fields = grok.AutoFields(IStudentStudyCourse).omit(
                'previous_verdict')
        else:
            form_fields = grok.AutoFields(IStudentStudyCourse)
        return form_fields

    @property
    def label(self):
        if self.context.is_current:
            return _('${a}: Study Course',
                mapping = {'a':self.context.__parent__.display_fullname})
        else:
            return _('${a}: Previous Study Course',
                mapping = {'a':self.context.__parent__.display_fullname})

    @property
    def current_mode(self):
        if self.context.certificate is not None:
            studymodes_dict = getUtility(IKofaUtils).STUDY_MODES_DICT
            return studymodes_dict[self.context.certificate.study_mode]
        return

    @property
    def department(self):
        try:
            if self.context.certificate is not None:
                return self.context.certificate.__parent__.__parent__
        except AttributeError:
            # handle_certificate_removed does only clear
            # studycourses with certificate code 'studycourse' but not
            # 'studycourse_1' or 'studycourse_2'. These certificates do
            # still exist but have no parents.
            pass
        return

    @property
    def faculty(self):
        try:
            if self.context.certificate is not None:
                return self.context.certificate.__parent__.__parent__.__parent__
        except AttributeError:
            # handle_certificate_removed does only clear
            # studycourses with certificate code 'studycourse' but not
            # 'studycourse_1' or 'studycourse_2'. These certificates do
            # still exist but have no parents.
            pass
        return

    @property
    def prev_studycourses(self):
        if self.context.is_current:
            if self.context.__parent__.get('studycourse_2', None) is not None:
                return (
                        {'href':self.url(self.context.student) + '/studycourse_1',
                        'title':_('First Study Course, ')},
                        {'href':self.url(self.context.student) + '/studycourse_2',
                        'title':_('Second Study Course')}
                        )
            if self.context.__parent__.get('studycourse_1', None) is not None:
                return (
                        {'href':self.url(self.context.student) + '/studycourse_1',
                        'title':_('First Study Course')},
                        )
        return

class StudyCourseManageFormPage(KofaEditFormPage):
    """ Page to edit the student study course data
    """
    grok.context(IStudentStudyCourse)
    grok.name('manage')
    grok.require('waeup.manageStudent')
    grok.template('studycoursemanagepage')
    label = _('Manage study course')
    pnav = 4
    taboneactions = [_('Save'),_('Cancel')]
    tabtwoactions = [_('Remove selected levels'),_('Cancel')]
    tabthreeactions = [_('Add study level')]

    @property
    def form_fields(self):
        if self.context.is_postgrad:
            form_fields = grok.AutoFields(IStudentStudyCourse).omit(
                'previous_verdict')
        else:
            form_fields = grok.AutoFields(IStudentStudyCourse)
        return form_fields

    def update(self):
        if not self.context.is_current \
            or self.context.student.studycourse_locked:
            emit_lock_message(self)
            return
        super(StudyCourseManageFormPage, self).update()
        return

    @action(_('Save'), style='primary')
    def save(self, **data):
        try:
            msave(self, **data)
        except ConstraintNotSatisfied:
            # The selected level might not exist in certificate
            self.flash(_('Current level not available for certificate.'),
                       type="warning")
            return
        notify(grok.ObjectModifiedEvent(self.context.__parent__))
        return

    @property
    def level_dicts(self):
        studylevelsource = StudyLevelSource().factory
        for code in studylevelsource.getValues(self.context):
            title = studylevelsource.getTitle(self.context, code)
            yield(dict(code=code, title=title))

    @property
    def session_dicts(self):
        yield(dict(code='', title='--'))
        for item in academic_sessions():
            code = item[1]
            title = item[0]
            yield(dict(code=code, title=title))

    @action(_('Add study level'), style='primary')
    def addStudyLevel(self, **data):
        level_code = self.request.form.get('addlevel', None)
        level_session = self.request.form.get('level_session', None)
        if not level_session and not level_code == '0':
            self.flash(_('You must select a session for the level.'),
                       type="warning")
            self.redirect(self.url(self.context, u'@@manage')+'#tab2')
            return
        if level_session and level_code == '0':
            self.flash(_('Level zero must not be assigned a session.'),
                       type="warning")
            self.redirect(self.url(self.context, u'@@manage')+'#tab2')
            return
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = int(level_code)
        if level_code != '0':
            studylevel.level_session = int(level_session)
        try:
            self.context.addStudentStudyLevel(
                self.context.certificate,studylevel)
            self.flash(_('Study level has been added.'))
        except KeyError:
            self.flash(_('This level exists.'), type="warning")
        self.redirect(self.url(self.context, u'@@manage')+'#tab2')
        return

    @jsaction(_('Remove selected levels'))
    def delStudyLevels(self, **data):
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No study level selected.'), type="warning")
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        deleted = []
        for id in child_id:
            del self.context[id]
            deleted.append(id)
        if len(deleted):
            self.flash(_('Successfully removed: ${a}',
                mapping = {'a':', '.join(deleted)}))
            self.context.writeLogMessage(
                self,'removed: %s' % ', '.join(deleted))
        self.redirect(self.url(self.context, u'@@manage')+'#tab2')
        return

class StudentTranscriptRequestPage(KofaPage):
    """ Page to request transcript by student
    """
    grok.context(IStudent)
    grok.name('request_transcript')
    grok.require('waeup.handleStudent')
    grok.template('transcriptrequest')
    label = _('Request transcript')
    ac_prefix = 'TSC'
    notice = ''
    pnav = 4
    buttonname = _('Request now')
    with_ac = True

    def update(self, SUBMIT=None):
        super(StudentTranscriptRequestPage, self).update()
        if not self.context.state == GRADUATED:
            self.flash(_("Wrong state"), type="danger")
            self.redirect(self.url(self.context))
            return
        if self.with_ac:
            self.ac_series = self.request.form.get('ac_series', None)
            self.ac_number = self.request.form.get('ac_number', None)
        if getattr(
            self.context['studycourse'], 'transcript_comment', None) is not None:
            self.correspondence = self.context[
                'studycourse'].transcript_comment.replace(
                    '\n', '<br>')
        else:
            self.correspondence = ''
        if SUBMIT is None:
            return
        if self.with_ac:
            pin = '%s-%s-%s' % (self.ac_prefix, self.ac_series, self.ac_number)
            code = get_access_code(pin)
            if not code:
                self.flash(_('Activation code is invalid.'), type="warning")
                return
            if code.state == USED:
                self.flash(_('Activation code has already been used.'),
                           type="warning")
                return
            # Mark pin as used (this also fires a pin related transition)
            # and fire transition request_transcript
            comment = _(u"invalidated")
            # Here we know that the ac is in state initialized so we do not
            # expect an exception, but the owner might be different
            if not invalidate_accesscode(pin, comment, self.context.student_id):
                self.flash(_('You are not the owner of this access code.'),
                           type="warning")
                return
            self.context.clr_code = pin
        IWorkflowInfo(self.context).fireTransition('request_transcript')
        comment = self.request.form.get('comment', '').replace('\r', '')
        address = self.request.form.get('address', '').replace('\r', '')
        tz = getattr(queryUtility(IKofaUtils), 'tzinfo', pytz.utc)
        today = now(tz).strftime('%d/%m/%Y %H:%M:%S %Z')
        old_transcript_comment = getattr(
            self.context['studycourse'], 'transcript_comment', None)
        if old_transcript_comment == None:
            old_transcript_comment = ''
        self.context['studycourse'].transcript_comment = '''On %s %s wrote:

%s

Dispatch Address:
%s

%s''' % (today, self.request.principal.id, comment, address,
         old_transcript_comment)
        self.context.writeLogMessage(
            self, 'comment: %s' % comment.replace('\n', '<br>'))
        self.flash(_('Transcript processing has been started.'))
        self.redirect(self.url(self.context))
        return

class TOStudentTranscriptRequestPage(StudentTranscriptRequestPage):
    """ Page to request transcript by student
    """
    grok.context(IStudent)
    grok.name('request_transcript_for_student')
    grok.require('waeup.processTranscript')
    grok.template('transcriptrequest')
    label = _('Request transcript for student')
    with_ac = False

class StudentTranscriptSignView(UtilityView, grok.View):
    """ View to sign transcript
    """
    grok.context(IStudentStudyCourse)
    grok.name('sign_transcript')
    grok.require('waeup.signTranscript')

    def update(self, SUBMIT=None):
        if self.context.student.state != TRANSVAL:
            self.flash(_('Student is in wrong state.'), type="warning")
            self.redirect(self.url(self.context))
            return
        prev_transcript_signees = getattr(
            self.context, 'transcript_signees', None)
        if prev_transcript_signees \
            and '(%s)' % self.request.principal.id in prev_transcript_signees:
            self.flash(_('You have already signed this transcript.'),
                type="warning")
            self.redirect(self.url(self.context) + '/transcript')
            return
        self.flash(_('Transcript signed.'))
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        self.context.student.__parent__.logger.info(
            '%s - %s - Transcript signed'
            % (ob_class, self.context.student.student_id))
        self.context.student.history.addMessage('Transcript signed')
        tz = getattr(queryUtility(IKofaUtils), 'tzinfo', pytz.utc)
        today = now(tz).strftime('%d/%m/%Y %H:%M:%S %Z')
        if prev_transcript_signees == None:
            prev_transcript_signees = ''
        self.context.transcript_signees = (
            u"Electronically signed by %s (%s) on %s\n%s"
            % (self.request.principal.title, self.request.principal.id, today,
            prev_transcript_signees))
        self.redirect(self.url(self.context) + '/transcript')
        return

    def render(self):
        return

class StudentTranscriptValidateFormPage(KofaEditFormPage):
    """ Page to validate transcript
    """
    grok.context(IStudentStudyCourse)
    grok.name('validate_transcript')
    grok.require('waeup.processTranscript')
    grok.template('transcriptprocess')
    label = _('Validate transcript')
    buttonname1 = _('Save comment')
    buttonname2 = _('Save comment and validate transcript')
    pnav = 4

    @property
    def remarks(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        levelremarks = ''
        studylevelsource = StudyLevelSource().factory
        for studylevel in self.context.values():
            leveltitle = studylevelsource.getTitle(
                self.context, studylevel.level)
            url = self.url(self.context) + '/%s/remark' % studylevel.level
            button_title = translate(
                _('Edit'), 'waeup.kofa', target_language=portal_language)
            levelremarks += (
                '<tr>'
                '<td>%s:</td>'
                '<td>%s</td> '
                '<td><a class="btn btn-primary btn-xs" href="%s">%s</a></td>'
                '</tr>'
                ) % (
                leveltitle, studylevel.transcript_remark, url, button_title)
        return levelremarks

    def update(self, SUBMIT=None, SAVE=None):
        super(StudentTranscriptValidateFormPage, self).update()
        if self.context.student.state != TRANSREQ:
            self.flash(_('Student is in wrong state.'), type="warning")
            self.redirect(self.url(self.context))
            return
        if getattr(self.context, 'transcript_comment', None) is not None:
            self.correspondence = self.context.transcript_comment.replace(
                '\n', '<br>')
        else:
            self.correspondence = ''
        if getattr(self.context, 'transcript_signees', None) is not None:
            self.signees = self.context.transcript_signees.replace(
                '\n', '<br><br>')
        else:
            self.signees = ''
        if SUBMIT is None and SAVE is None:
            return
        if SAVE or SUBMIT:
            # Save comment and append old comment
            comment = self.request.form.get('comment', '').replace('\r', '')
            tz = getattr(queryUtility(IKofaUtils), 'tzinfo', pytz.utc)
            today = now(tz).strftime('%d/%m/%Y %H:%M:%S %Z')
            old_transcript_comment = getattr(
                self.context, 'transcript_comment', None)
            if old_transcript_comment == None:
                old_transcript_comment = ''
            self.context.transcript_comment = '''On %s %s wrote:

%s

%s''' % (today, self.request.principal.id, comment, old_transcript_comment)
            self.context.writeLogMessage(
                self, 'comment: %s' % comment.replace('\n', '<br>'))
        if SUBMIT:
            # Fire transition
            IWorkflowInfo(self.context.student).fireTransition('validate_transcript')
            self.flash(_('Transcript validated.'))
        self.redirect(self.url(self.context) + '/transcript')
        return

class StudentTranscriptReleaseFormPage(KofaEditFormPage):
    """ Page to release transcript
    """
    grok.context(IStudentStudyCourse)
    grok.name('release_transcript')
    grok.require('waeup.processTranscript')
    grok.template('transcriptprocess')
    label = _('Release transcript')
    buttonname1 = None
    buttonname2 = _('Save comment and release transcript')
    pnav = 4

    @property
    def remarks(self):
        levelremarks = ''
        studylevelsource = StudyLevelSource().factory
        for studylevel in self.context.values():
            leveltitle = studylevelsource.getTitle(
                self.context, studylevel.level)
            levelremarks += "%s: %s <br><br>" % (
                leveltitle, studylevel.transcript_remark)
        return levelremarks

    def update(self, SUBMIT=None):
        super(StudentTranscriptReleaseFormPage, self).update()
        if self.context.student.state != TRANSVAL:
            self.flash(_('Student is in wrong state.'), type="warning")
            self.redirect(self.url(self.context))
            return
        if getattr(self.context, 'transcript_comment', None) is not None:
            self.correspondence = self.context.transcript_comment.replace(
                '\n', '<br>')
        else:
            self.correspondence = ''
        if getattr(self.context, 'transcript_signees', None) is not None:
            self.signees = self.context.transcript_signees.replace(
                '\n', '<br><br>')
        else:
            self.signees = ''
        if SUBMIT is None:
            return
        # Fire transition
        IWorkflowInfo(self.context.student).fireTransition('release_transcript')
        self.flash(_('Transcript released and final transcript file saved.'))
        comment = self.request.form.get('comment', '').replace('\r', '')
        tz = getattr(queryUtility(IKofaUtils), 'tzinfo', pytz.utc)
        today = now(tz).strftime('%d/%m/%Y %H:%M:%S %Z')
        old_transcript_comment = getattr(
            self.context, 'transcript_comment', None)
        if old_transcript_comment == None:
            old_transcript_comment = ''
        self.context.transcript_comment = '''On %s %s wrote:

%s

%s''' % (today, self.request.principal.id, comment,
         old_transcript_comment)
        self.context.writeLogMessage(
            self, 'comment: %s' % comment.replace('\n', '<br>'))
        # Produce transcript file
        self.redirect(self.url(self.context) + '/transcript.pdf')
        return

class StudyCourseTranscriptPage(KofaDisplayFormPage):
    """ Page to display the student's transcript.
    """
    grok.context(IStudentStudyCourse)
    grok.name('transcript')
    grok.require('waeup.viewTranscript')
    grok.template('transcript')
    pnav = 4

    def format_float(self, value, prec):
        format_float = getUtility(IKofaUtils).format_float
        return format_float(value, prec)

    def update(self):
        final_slip = getUtility(IExtFileStore).getFileByContext(
            self.context.student, attr='final_transcript')
        if not self.context.student.transcript_enabled or final_slip:
            self.flash(_('Forbidden!'), type="warning")
            self.redirect(self.url(self.context))
            return
        super(StudyCourseTranscriptPage, self).update()
        self.semester_dict = getUtility(IKofaUtils).SEMESTER_DICT
        self.level_dict = level_dict(self.context)
        self.session_dict = dict([(None, 'None'),] +
            [(item[1], item[0]) for item in academic_sessions()])
        self.studymode_dict = getUtility(IKofaUtils).STUDY_MODES_DICT
        return

    @property
    def label(self):
        # Here we know that the cookie has been set
        return _('${a}: Transcript Data', mapping = {
            'a':self.context.student.display_fullname})

class ExportPDFTranscriptSlip(UtilityView, grok.View):
    """Deliver a PDF slip of the context.
    """
    grok.context(IStudentStudyCourse)
    grok.name('transcript.pdf')
    grok.require('waeup.downloadTranscript')
    prefix = 'form'
    omit_fields = (
        'department', 'faculty', 'current_mode', 'entry_session', 'certificate',
        'password', 'suspended', 'phone', 'email', 'parents_email',
        'adm_code', 'suspended_comment', 'current_level', 'flash_notice')

    def update(self):
        final_slip = getUtility(IExtFileStore).getFileByContext(
            self.context.student, attr='final_transcript')
        if not self.context.student.transcript_enabled \
            or final_slip:
            self.flash(_('Forbidden!'), type="warning")
            self.redirect(self.url(self.context))
            return
        super(ExportPDFTranscriptSlip, self).update()
        self.semester_dict = getUtility(IKofaUtils).SEMESTER_DICT
        self.level_dict = level_dict(self.context)
        self.session_dict = dict([(None, 'None'),] +
            [(item[1], item[0]) for item in academic_sessions()])
        self.studymode_dict = getUtility(IKofaUtils).STUDY_MODES_DICT
        return

    @property
    def label(self):
        # Here we know that the cookie has been set
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Academic Transcript'),
            'waeup.kofa', target_language=portal_language)

    def _sigsInFooter(self):
        if getattr(
            self.context.student['studycourse'], 'transcript_signees', None):
            return ()
        return (_('CERTIFIED TRUE COPY'),)

    def _signatures(self):
        return ()

    def _digital_sigs(self):
        if getattr(
            self.context.student['studycourse'], 'transcript_signees', None):
            return self.context.student['studycourse'].transcript_signees 
        return ()

    def _save_file(self):
        if self.context.student.state == TRANSREL:
            return True
        return False

    def render(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        Term = translate(_('Term'), 'waeup.kofa', target_language=portal_language)
        Code = translate(_('Code'), 'waeup.kofa', target_language=portal_language)
        Title = translate(_('Title'), 'waeup.kofa', target_language=portal_language)
        Cred = translate(_('Credits'), 'waeup.kofa', target_language=portal_language)
        Score = translate(_('Score'), 'waeup.kofa', target_language=portal_language)
        Grade = translate(_('Grade'), 'waeup.kofa', target_language=portal_language)
        studentview = StudentBasePDFFormPage(self.context.student,
            self.request, self.omit_fields)
        students_utils = getUtility(IStudentsUtils)

        tableheader = [(Code,'code', 2.5),
                         (Title,'title', 7),
                         (Term, 'semester', 1.5),
                         (Cred, 'credits', 1.5),
                         (Score, 'total_score', 1.5),
                         (Grade, 'grade', 1.5),
                         ]

        pdfstream = students_utils.renderPDFTranscript(
            self, 'transcript.pdf',
            self.context.student, studentview,
            omit_fields=self.omit_fields,
            tableheader=tableheader,
            signatures=self._signatures(),
            sigs_in_footer=self._sigsInFooter(),
            digital_sigs=self._digital_sigs(),
            save_file=self._save_file(),
            )
        if not pdfstream:
            self.redirect(self.url(self.context.student))
            return
        return pdfstream

class StudentTransferFormPage(KofaAddFormPage):
    """Page to transfer the student.
    """
    grok.context(IStudent)
    grok.name('transfer')
    grok.require('waeup.manageStudent')
    label = _('Transfer student')
    form_fields = grok.AutoFields(IStudentStudyCourseTransfer).omit(
        'entry_mode', 'entry_session')
    pnav = 4

    @jsaction(_('Transfer'))
    def transferStudent(self, **data):
        error = self.context.transfer(**data)
        if error == -1:
            self.flash(_('Current level does not match certificate levels.'),
                       type="warning")
        elif error == -2:
            self.flash(_('Former study course record incomplete.'),
                       type="warning")
        elif error == -3:
            self.flash(_('Maximum number of transfers exceeded.'),
                       type="warning")
        else:
            self.flash(_('Successfully transferred.'))
        return

class RevertTransferFormPage(KofaEditFormPage):
    """View that reverts the previous transfer.
    """
    grok.context(IStudent)
    grok.name('revert_transfer')
    grok.require('waeup.manageStudent')
    grok.template('reverttransfer')
    label = _('Revert previous transfer')

    def update(self):
        if not self.context.has_key('studycourse_1'):
            self.flash(_('No previous transfer.'), type="warning")
            self.redirect(self.url(self.context))
            return
        return

    @jsaction(_('Revert now'))
    def transferStudent(self, **data):
        self.context.revert_transfer()
        self.flash(_('Previous transfer reverted.'))
        self.redirect(self.url(self.context, 'studycourse'))
        return

class StudyLevelDisplayFormPage(KofaDisplayFormPage):
    """ Page to display student study levels
    """
    grok.context(IStudentStudyLevel)
    grok.name('index')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(IStudentStudyLevel).omit('level')
    form_fields[
        'validation_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    grok.template('studylevelpage')
    pnav = 4

    def update(self):
        super(StudyLevelDisplayFormPage, self).update()
        if self.context.level == 0:
            self.form_fields = self.form_fields.omit('gpa')
        return

    @property
    def translated_values(self):
        return translated_values(self)

    @property
    def label(self):
        # Here we know that the cookie has been set
        lang = self.request.cookies.get('kofa.language')
        level_title = translate(self.context.level_title, 'waeup.kofa',
            target_language=lang)
        return _('${a}: ${b}', mapping = {
            'a':self.context.student.display_fullname,
            'b':level_title})

class ExportPDFCourseRegistrationSlip(UtilityView, grok.View):
    """Deliver a PDF slip of the context.
    """
    grok.context(IStudentStudyLevel)
    grok.name('course_registration_slip.pdf')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(IStudentStudyLevel).omit(
        'level', 'gpa', 'transcript_remark')
    form_fields[
        'validation_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    prefix = 'form'
    omit_fields = (
        'password', 'suspended', 'phone', 'date_of_birth',
        'adm_code', 'sex', 'suspended_comment', 'current_level',
        'flash_notice')

    @property
    def title(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Level Data'), 'waeup.kofa',
            target_language=portal_language)

    @property
    def label(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        lang = self.request.cookies.get('kofa.language', portal_language)
        level_title = translate(self.context.level_title, 'waeup.kofa',
            target_language=lang)
        return translate(_('Course Registration Slip'),
            'waeup.kofa', target_language=portal_language) \
            + ' %s' % level_title

    @property
    def tabletitle(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        tabletitle = []
        tabletitle.append(translate(_('1st Semester Courses'), 'waeup.kofa',
            target_language=portal_language))
        tabletitle.append(translate(_('2nd Semester Courses'), 'waeup.kofa',
            target_language=portal_language))
        tabletitle.append(translate(_('Level Courses'), 'waeup.kofa',
            target_language=portal_language))
        return tabletitle

    def _signatures(self):
        return ()

    def _sigsInFooter(self):
        return ()

    def render(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        Code = translate(_('Code'), 'waeup.kofa', target_language=portal_language)
        Title = translate(_('Title'), 'waeup.kofa', target_language=portal_language)
        Dept = translate(_('Dept.'), 'waeup.kofa', target_language=portal_language)
        Faculty = translate(_('Faculty'), 'waeup.kofa', target_language=portal_language)
        Cred = translate(_('Cred.'), 'waeup.kofa', target_language=portal_language)
        #Mand = translate(_('Requ.'), 'waeup.kofa', target_language=portal_language)
        Score = translate(_('Score'), 'waeup.kofa', target_language=portal_language)
        Grade = translate(_('Grade'), 'waeup.kofa', target_language=portal_language)
        studentview = StudentBasePDFFormPage(self.context.student,
            self.request, self.omit_fields)
        students_utils = getUtility(IStudentsUtils)

        tabledata = []
        tableheader = []
        for i in range(1,7):
            tabledata.append(sorted(
                [value for value in self.context.values() if value.semester == i],
                key=lambda value: str(value.semester) + value.code))
            tableheader.append([(Code,'code', 2.5),
                             (Title,'title', 5),
                             (Dept,'dcode', 1.5), (Faculty,'fcode', 1.5),
                             (Cred, 'credits', 1.5),
                             #(Mand, 'mandatory', 1.5),
                             (Score, 'score', 1.5),
                             (Grade, 'grade', 1.5),
                             #('Auto', 'automatic', 1.5)
                             ])
        return students_utils.renderPDF(
            self, 'course_registration_slip.pdf',
            self.context.student, studentview,
            tableheader=tableheader,
            tabledata=tabledata,
            omit_fields=self.omit_fields,
            signatures=self._signatures(),
            sigs_in_footer=self._sigsInFooter(),
            )

class StudyLevelManageFormPage(KofaEditFormPage):
    """ Page to edit the student study level data
    """
    grok.context(IStudentStudyLevel)
    grok.name('manage')
    grok.require('waeup.manageStudent')
    grok.template('studylevelmanagepage')
    form_fields = grok.AutoFields(IStudentStudyLevel).omit(
        'validation_date', 'validated_by', 'total_credits', 'gpa', 'level')
    pnav = 4
    taboneactions = [_('Save'),_('Cancel')]
    tabtwoactions = [_('Add course ticket'),
        _('Remove selected tickets'),_('Cancel')]
    placeholder = _('Enter valid course code')

    def update(self, ADD=None, course=None):
        if not self.context.__parent__.is_current \
            or self.context.student.studycourse_locked:
            emit_lock_message(self)
            return
        super(StudyLevelManageFormPage, self).update()
        if ADD is not None:
            if not course:
                self.flash(_('No valid course code entered.'), type="warning")
                self.redirect(self.url(self.context, u'@@manage')+'#tab2')
                return
            cat = queryUtility(ICatalog, name='courses_catalog')
            result = cat.searchResults(code=(course, course))
            if len(result) != 1:
                self.flash(_('Course not found.'), type="warning")
            else:
                course = list(result)[0]
                addCourseTicket(self, course)
            self.redirect(self.url(self.context, u'@@manage')+'#tab2')
        return

    @property
    def translated_values(self):
        return translated_values(self)

    @property
    def label(self):
        # Here we know that the cookie has been set
        lang = self.request.cookies.get('kofa.language')
        level_title = translate(self.context.level_title, 'waeup.kofa',
            target_language=lang)
        return _('Manage ${a}',
            mapping = {'a':level_title})

    @action(_('Save'), style='primary')
    def save(self, **data):
        msave(self, **data)
        return

    @jsaction(_('Remove selected tickets'))
    def delCourseTicket(self, **data):
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No ticket selected.'), type="warning")
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        deleted = []
        for id in child_id:
            del self.context[id]
            deleted.append(id)
        if len(deleted):
            self.flash(_('Successfully removed: ${a}',
                mapping = {'a':', '.join(deleted)}))
            self.context.writeLogMessage(
                self,'removed: %s' % (', '.join(deleted)))
        self.redirect(self.url(self.context, u'@@manage')+'#tab2')
        return

class StudyLevelRemarkFormPage(KofaEditFormPage):
    """ Page to edit the student study level transcript remark only
    """
    grok.context(IStudentStudyLevel)
    grok.name('remark')
    grok.require('waeup.processTranscript')
    grok.template('studylevelremarkpage')
    form_fields = grok.AutoFields(IStudentStudyLevel).omit('level')
    form_fields['level_session'].for_display = True
    form_fields['level_verdict'].for_display = True
    form_fields['validation_date'].for_display = True
    form_fields['validated_by'].for_display = True

    def update(self, ADD=None, course=None):
        if self.context.student.studycourse_locked:
            emit_lock_message(self)
            return
        super(StudyLevelRemarkFormPage, self).update()

    @property
    def label(self):
        lang = self.request.cookies.get('kofa.language')
        level_title = translate(self.context.level_title, 'waeup.kofa',
            target_language=lang)
        return _(
            'Edit transcript remark of level ${a}', mapping = {'a':level_title})

    @property
    def translated_values(self):
        return translated_values(self)

    @action(_('Save remark and go and back to transcript validation page'),
        style='primary')
    def save(self, **data):
        msave(self, **data)
        self.redirect(self.url(self.context.student)
            + '/studycourse/validate_transcript#tab4')
        return

class ValidateCoursesView(UtilityView, grok.View):
    """ Validate course list by course adviser
    """
    grok.context(IStudentStudyLevel)
    grok.name('validate_courses')
    grok.require('waeup.validateStudent')

    def update(self):
        if not self.context.__parent__.is_current:
            emit_lock_message(self)
            return
        if str(self.context.student.current_level) != self.context.__name__:
            self.flash(_('This is not the student\'s current level.'),
                       type="danger")
        elif self.context.student.state == REGISTERED:
            IWorkflowInfo(self.context.student).fireTransition(
                'validate_courses')
            self.flash(_('Course list has been validated.'))
        else:
            self.flash(_('Student is in the wrong state.'), type="warning")
        self.redirect(self.url(self.context))
        return

    def render(self):
        return

class RejectCoursesView(UtilityView, grok.View):
    """ Reject course list by course adviser
    """
    grok.context(IStudentStudyLevel)
    grok.name('reject_courses')
    grok.require('waeup.validateStudent')

    def update(self):
        if not self.context.__parent__.is_current:
            emit_lock_message(self)
            return
        if str(self.context.__parent__.current_level) != self.context.__name__:
            self.flash(_('This is not the student\'s current level.'),
                       type="danger")
            self.redirect(self.url(self.context))
            return
        elif self.context.student.state == VALIDATED:
            IWorkflowInfo(self.context.student).fireTransition('reset8')
            message = _('Course list request has been annulled.')
            self.flash(message)
        elif self.context.student.state == REGISTERED:
            IWorkflowInfo(self.context.student).fireTransition('reset7')
            message = _('Course list has been unregistered.')
            self.flash(message)
        else:
            self.flash(_('Student is in the wrong state.'), type="warning")
            self.redirect(self.url(self.context))
            return
        args = {'subject':message}
        self.redirect(self.url(self.context.student) +
            '/contactstudent?%s' % urlencode(args))
        return

    def render(self):
        return

class UnregisterCoursesView(UtilityView, grok.View):
    """Unregister course list by student
    """
    grok.context(IStudentStudyLevel)
    grok.name('unregister_courses')
    grok.require('waeup.handleStudent')

    def update(self):
        if not self.context.__parent__.is_current:
            emit_lock_message(self)
            return
        try:
            deadline = grok.getSite()['configuration'][
                str(self.context.level_session)].coursereg_deadline
        except (TypeError, KeyError):
            deadline = None
        if deadline and deadline < datetime.now(pytz.utc):
            self.flash(_(
                "Course registration has ended. "
                "Unregistration is disabled."), type="warning")
        elif str(self.context.__parent__.current_level) != self.context.__name__:
            self.flash(_('This is not your current level.'), type="danger")
        elif self.context.student.state == REGISTERED:
            IWorkflowInfo(self.context.student).fireTransition('reset7')
            message = _('Course list has been unregistered.')
            self.flash(message)
        else:
            self.flash(_('You are in the wrong state.'), type="warning")
        self.redirect(self.url(self.context))
        return

    def render(self):
        return

class CourseTicketAddFormPage(KofaAddFormPage):
    """Add a course ticket.
    """
    grok.context(IStudentStudyLevel)
    grok.name('add')
    grok.require('waeup.manageStudent')
    label = _('Add course ticket')
    form_fields = grok.AutoFields(ICourseTicketAdd)
    pnav = 4

    def update(self):
        if not self.context.__parent__.is_current \
            or self.context.student.studycourse_locked:
            emit_lock_message(self)
            return
        super(CourseTicketAddFormPage, self).update()
        return

    @action(_('Add course ticket'), style='primary')
    def addCourseTicket(self, **data):
        course = data['course']
        success = addCourseTicket(self, course)
        if success:
            self.redirect(self.url(self.context, u'@@manage')+'#tab2')
        return

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))

class CourseTicketDisplayFormPage(KofaDisplayFormPage):
    """ Page to display course tickets
    """
    grok.context(ICourseTicket)
    grok.name('index')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(ICourseTicket).omit('course_category',
        'ticket_session')
    grok.template('courseticketpage')
    pnav = 4

    @property
    def label(self):
        return _('${a}: Course Ticket ${b}', mapping = {
            'a':self.context.student.display_fullname,
            'b':self.context.code})

class CourseTicketManageFormPage(KofaEditFormPage):
    """ Page to manage course tickets
    """
    grok.context(ICourseTicket)
    grok.name('manage')
    grok.require('waeup.manageStudent')
    form_fields = grok.AutoFields(ICourseTicket).omit('course_category')
    form_fields['title'].for_display = True
    form_fields['fcode'].for_display = True
    form_fields['dcode'].for_display = True
    form_fields['semester'].for_display = True
    form_fields['passmark'].for_display = True
    form_fields['credits'].for_display = True
    form_fields['mandatory'].for_display = False
    form_fields['automatic'].for_display = True
    form_fields['carry_over'].for_display = True
    form_fields['ticket_session'].for_display = True
    pnav = 4
    grok.template('courseticketmanagepage')

    def update(self):
        if not self.context.__parent__.__parent__.is_current \
            or self.context.student.studycourse_locked:
            emit_lock_message(self)
            return
        super(CourseTicketManageFormPage, self).update()
        return

    @property
    def label(self):
        return _('Manage course ticket ${a}', mapping = {'a':self.context.code})

    @action('Save', style='primary')
    def save(self, **data):
        msave(self, **data)
        return

class PaymentsManageFormPage(KofaEditFormPage):
    """ Page to manage the student payments

    This manage form page is for both students and students officers.
    """
    grok.context(IStudentPaymentsContainer)
    grok.name('index')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(IStudentPaymentsContainer)
    grok.template('paymentsmanagepage')
    pnav = 4

    @property
    def manage_payments_allowed(self):
        return checkPermission('waeup.payStudent', self.context)

    def unremovable(self, ticket):
        usertype = getattr(self.request.principal, 'user_type', None)
        if not usertype:
            return False
        if not self.manage_payments_allowed:
            return True
        return (self.request.principal.user_type == 'student' and ticket.r_code)

    @property
    def label(self):
        return _('${a}: Payments',
            mapping = {'a':self.context.__parent__.display_fullname})

    @jsaction(_('Remove selected tickets'))
    def delPaymentTicket(self, **data):
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No payment selected.'), type="warning")
            self.redirect(self.url(self.context))
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        deleted = []
        for id in child_id:
            # Students are not allowed to remove used payment tickets
            ticket = self.context.get(id, None)
            if ticket is not None and not self.unremovable(ticket):
                del self.context[id]
                deleted.append(id)
        if len(deleted):
            self.flash(_('Successfully removed: ${a}',
                mapping = {'a': ', '.join(deleted)}))
            self.context.writeLogMessage(
                self,'removed: %s' % ', '.join(deleted))
        self.redirect(self.url(self.context))
        return

class OnlinePaymentAddFormPage(KofaAddFormPage):
    """ Page to add an online payment ticket
    """
    grok.context(IStudentPaymentsContainer)
    grok.name('addop')
    grok.template('onlinepaymentaddform')
    grok.require('waeup.payStudent')
    form_fields = grok.AutoFields(IStudentOnlinePayment).select('p_combi')
    label = _('Add online payment')
    pnav = 4

    @property
    def selectable_categories(self):
        student = self.context.__parent__
        categories = getUtility(
            IKofaUtils).selectable_payment_categories(student)
        return sorted(categories.items(), key=lambda value: value[1])

    @property
    def selectable_payment_options(self):
        student = self.context.__parent__
        options = getUtility(
            IKofaUtils).selectable_payment_options(student)
        return sorted(options.items(), key=lambda value: value[1])

    @action(_('Create ticket'), style='primary')
    def createTicket(self, **data):
        form = self.request.form
        p_category = form.get('form.p_category', None)
        p_option = form.get('form.p_option', None)
        p_combi = form.get('form.p_combi', [])
        if isinstance(form.get('form.p_combi', None), unicode):
            p_combi = [p_combi,]
        student = self.context.__parent__
        students_utils = getUtility(IStudentsUtils)
        # The hostel_application payment category is temporarily used
        # by Uniben.
        accommodation_session = grok.getSite()['hostels'].accommodation_session
        if p_category in ('bed_allocation', 'hostel_application') \
            and accommodation_session - student[
                'studycourse'].current_session > students_utils.ACCOMMODATION_SPAN:
                self.flash(
                    _('Your current session does not allow ' + \
                    'to book accommodation.'), type="danger")
                return
        if 'maintenance' in p_category:
            if str(accommodation_session) not in student['accommodation']:
                self.flash(_('You have not yet booked accommodation.'),
                           type="warning")
                return
        error, payment = students_utils.setPaymentDetails(
            p_category, student, None, None, p_combi)
        if error is not None:
            self.flash(error, type="danger")
            return
        if p_category == 'transfer':
            payment.p_item = form['new_programme']
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

class PreviousPaymentAddFormPage(KofaAddFormPage):
    """ Page to add an online payment ticket for previous sessions.
    """
    grok.context(IStudentPaymentsContainer)
    grok.name('addpp')
    grok.template('previouspaymentaddform')
    grok.require('waeup.payStudent')
    form_fields = grok.AutoFields(IStudentPreviousPayment)
    label = _('Add previous session online payment')
    pnav = 4

    def update(self):
        if self.context.student.before_payment:
            self.flash(_("No previous payment to be made."), type="warning")
            self.redirect(self.url(self.context))
        super(PreviousPaymentAddFormPage, self).update()
        return

    @property
    def selectable_payment_options(self):
        student = self.context.__parent__
        options = getUtility(
            IKofaUtils).selectable_payment_options(student)
        return sorted(options.items(), key=lambda value: value[1])

    @action(_('Create ticket'), style='primary')
    def createTicket(self, **data):
        p_category = data['p_category']
        form = self.request.form
        p_option = form.get('form.p_option', None)
        previous_session = data.get('p_session', None)
        previous_level = data.get('p_level', None)
        student = self.context.__parent__
        students_utils = getUtility(IStudentsUtils)
        error, payment = students_utils.setPaymentDetails(
            p_category, student, previous_session, previous_level, None)
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

class BalancePaymentAddFormPage(KofaAddFormPage):
    """ Page to add an online payment which can balance s previous session
    payment.
    """
    grok.context(IStudentPaymentsContainer)
    grok.name('addbp')
    grok.template('previouspaymentaddform')
    grok.require('waeup.manageStudent')
    form_fields = grok.AutoFields(IStudentBalancePayment)
    label = _('Add balance')
    pnav = 4

    @property
    def selectable_payment_options(self):
        student = self.context.__parent__
        options = getUtility(
            IKofaUtils).selectable_payment_options(student)
        return sorted(options.items(), key=lambda value: value[1])

    @action(_('Create ticket'), style='primary')
    def createTicket(self, **data):
        p_category = data['p_category']
        form = self.request.form
        p_option = form.get('form.p_option', None)
        balance_session = data.get('balance_session', None)
        balance_level = data.get('balance_level', None)
        balance_amount = data.get('balance_amount', None)
        student = self.context.__parent__
        students_utils = getUtility(IStudentsUtils)
        error, payment = students_utils.setBalanceDetails(
            p_category, student, balance_session,
            balance_level, balance_amount)
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
    grok.context(IStudentOnlinePayment)
    grok.name('index')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(IStudentOnlinePayment).omit(
        'p_item', 'p_combi')
    form_fields[
        'creation_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    form_fields[
        'payment_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    pnav = 4

    @property
    def label(self):
        return _('${a}: Online Payment Ticket ${b}', mapping = {
            'a':self.context.student.display_fullname,
            'b':self.context.p_id})

class OnlinePaymentApproveView(UtilityView, grok.View):
    """ Callback view
    """
    grok.context(IStudentOnlinePayment)
    grok.name('approve')
    grok.require('waeup.managePortal')

    def update(self):
        flashtype, msg, log = self.context.approveStudentPayment()
        if log is not None:
            # Add log message to students.log
            self.context.writeLogMessage(self,log)
            # Add log message to payments.log
            self.context.logger.info(
                '%s,%s,%s,%s,%s,,,,,,' % (
                self.context.student.student_id,
                self.context.p_id, self.context.p_category,
                self.context.amount_auth, self.context.r_code))
        self.flash(msg, type=flashtype)
        return

    def render(self):
        self.redirect(self.url(self.context, '@@index'))
        return

class OnlinePaymentFakeApproveView(OnlinePaymentApproveView):
    """ Approval view for students.

    This view is used for browser tests only and
    must be neutralized on custom pages!
    """
    grok.name('fake_approve')
    grok.require('waeup.payStudent')

class ExportPDFPaymentSlip(UtilityView, grok.View):
    """Deliver a PDF slip of the context.
    """
    grok.context(IStudentOnlinePayment)
    grok.name('payment_slip.pdf')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(IStudentOnlinePayment).omit(
        'p_item', 'p_combi')
    form_fields['creation_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    form_fields['payment_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    prefix = 'form'
    note = None
    omit_fields = (
        'password', 'suspended', 'phone', 'date_of_birth',
        'adm_code', 'sex', 'suspended_comment', 'current_level',
        'flash_notice')

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

    def render(self):
        #if self.context.p_state != 'paid':
        #    self.flash('Ticket not yet paid.')
        #    self.redirect(self.url(self.context))
        #    return
        studentview = StudentBasePDFFormPage(self.context.student,
            self.request, self.omit_fields)
        students_utils = getUtility(IStudentsUtils)
        return students_utils.renderPDF(self, 'payment_slip.pdf',
            self.context.student, studentview, note=self.note,
            omit_fields=self.omit_fields)

class AccommodationDisplayFormPage(KofaDisplayFormPage):
    """ Page to view bed tickets.
    This manage form page is for both students and students officers.
    """
    grok.context(IStudentAccommodation)
    grok.name('index')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(IStudentAccommodation)
    grok.template('accommodationpage')
    pnav = 4
    with_hostel_selection = True

    @property
    def label(self):
        return _('${a}: Accommodation',
            mapping = {'a':self.context.__parent__.display_fullname})

    @property
    def desired_hostel(self):
        if self.context.desired_hostel == 'no':
            return _('No favoured hostel')
        if self.context.desired_hostel:
            hostel = grok.getSite()['hostels'].get(self.context.desired_hostel)
            if hostel is not None:
                return hostel.hostel_name
        return

    def update(self):
        if checkPermission('waeup.handleAccommodation', self.context):
            self.redirect(self.url(self.context, 'manage'))

class AccommodationManageFormPage(KofaEditFormPage):
    """ Page to manage bed tickets.

    This manage form page is for both students and students officers.
    """
    grok.context(IStudentAccommodation)
    grok.name('manage')
    grok.require('waeup.handleAccommodation')
    form_fields = grok.AutoFields(IStudentAccommodation)
    grok.template('accommodationmanagepage')
    pnav = 4
    with_hostel_selection = True

    @property
    def booking_allowed(self):
        students_utils = getUtility(IStudentsUtils)
        acc_details  = students_utils.getAccommodationDetails(self.context.student)
        error_message = students_utils.checkAccommodationRequirements(
            self.context.student, acc_details)
        if error_message:
            return False
        return True

    @property
    def actionsgroup1(self):
        if not self.booking_allowed:
            return []
        if not self.with_hostel_selection:
            return []
        return [_('Save')]

    @property
    def actionsgroup2(self):
        if getattr(self.request.principal, 'user_type', None) == 'student':
            ## Book button can be disabled in custom packages by
            ## uncommenting the following lines.
            #if not self.booking_allowed:
            #    return []
            return [_('Book accommodation')]
        return [_('Book accommodation'), _('Remove selected')]

    @property
    def label(self):
        return _('${a}: Accommodation',
            mapping = {'a':self.context.__parent__.display_fullname})

    @property
    def desired_hostel(self):
        if self.context.desired_hostel == 'no':
            return _('No favoured hostel')
        if self.context.desired_hostel:
            hostel = grok.getSite()['hostels'].get(self.context.desired_hostel)
            if hostel is not None:
                return hostel.hostel_name
        return

    def getHostels(self):
        """Get a list of all stored hostels.
        """
        yield(dict(name=None, title='--', selected=''))
        selected = ''
        if self.context.desired_hostel == 'no':
          selected = 'selected'
        yield(dict(name='no', title=_('No favoured hostel'), selected=selected))
        for val in grok.getSite()['hostels'].values():
            selected = ''
            if val.hostel_id == self.context.desired_hostel:
                selected = 'selected'
            yield(dict(name=val.hostel_id, title=val.hostel_name,
                       selected=selected))

    @action(_('Save'), style='primary')
    def save(self):
        hostel = self.request.form.get('hostel', None)
        self.context.desired_hostel = hostel
        self.flash(_('Your selection has been saved.'))
        return

    @action(_('Book accommodation'), style='primary')
    def bookAccommodation(self, **data):
        self.redirect(self.url(self.context, 'add'))
        return

    @jsaction(_('Remove selected'))
    def delBedTickets(self, **data):
        if getattr(self.request.principal, 'user_type', None) == 'student':
            self.flash(_('You are not allowed to remove bed tickets.'),
                       type="warning")
            self.redirect(self.url(self.context))
            return
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No bed ticket selected.'), type="warning")
            self.redirect(self.url(self.context))
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        deleted = []
        for id in child_id:
            del self.context[id]
            deleted.append(id)
        if len(deleted):
            self.flash(_('Successfully removed: ${a}',
                mapping = {'a':', '.join(deleted)}))
            self.context.writeLogMessage(
                self,'removed: % s' % ', '.join(deleted))
        self.redirect(self.url(self.context))
        return

class BedTicketAddPage(KofaPage):
    """ Page to add a bed ticket
    """
    grok.context(IStudentAccommodation)
    grok.name('add')
    grok.require('waeup.handleAccommodation')
    #grok.template('enterpin')
    ac_prefix = 'HOS'
    label = _('Add bed ticket')
    pnav = 4
    buttonname = _('Create bed ticket')
    notice = ''
    with_ac = True
    with_bedselection = True

    @property
    def getAvailableBeds(self):
        """Get a list of all available beds.
        """
        cat = queryUtility(ICatalog, name='beds_catalog', default=None)
        entries = cat.searchResults(
            bed_type=(self.acc_details['bt'],self.acc_details['bt']))
        available_beds = [
            entry for entry in entries if entry.owner == NOT_OCCUPIED]
        desired_hostel = self.context.desired_hostel
        # Filter desired hostel beds
        if desired_hostel and desired_hostel != 'no':
            filtered_beds = [bed for bed in available_beds
                             if bed.bed_id.startswith(desired_hostel)]
            available_beds = filtered_beds
        # Add legible bed coordinates
        for bed in available_beds:
            hall_title = bed.__parent__.hostel_name
            coordinates = bed.coordinates[1:]
            block, room_nr, bed_nr = coordinates
            bed.temp_bed_coordinates = _(
                '${a}, Block ${b}, Room ${c}, Bed ${d}', mapping = {
                'a':hall_title, 'b':block,
                'c':room_nr, 'd':bed_nr})
        return available_beds

    def update(self, SUBMIT=None):
        student = self.context.student
        students_utils = getUtility(IStudentsUtils)
        self.acc_details  = students_utils.getAccommodationDetails(student)
        error_message = students_utils.checkAccommodationRequirements(
            student, self.acc_details)
        cat = queryUtility(ICatalog, name='beds_catalog', default=None)
        entries = cat.searchResults(
            owner=(student.student_id,student.student_id))
        self.show_available_beds = False
        if error_message:
            self.flash(error_message, type="warning")
            self.redirect(self.url(self.context))
            return
        if self.with_ac:
            self.ac_series = self.request.form.get('ac_series', None)
            self.ac_number = self.request.form.get('ac_number', None)
        available_beds = self.getAvailableBeds
        if SUBMIT is None:
            if self.with_bedselection and available_beds and not len(entries):
                self.show_available_beds = True
            return
        if self.with_ac:
            pin = '%s-%s-%s' % (self.ac_prefix, self.ac_series, self.ac_number)
            code = get_access_code(pin)
            if not code:
                self.flash(_('Activation code is invalid.'), type="warning")
                return
        # Search and book bed
        if len(entries):
            # If bed space has been manually allocated use this bed ...
            manual = True
            bed = list(entries)[0]
        else:
            # ... else search for available beds
            manual = False
            selected_bed = self.request.form.get('bed', None)
            if selected_bed:
                # Use selected bed
                beds = cat.searchResults(
                    bed_id=(selected_bed,selected_bed))
                bed = list(beds)[0]
                bed.bookBed(student.student_id)
            elif available_beds:
                # Select bed according to selectBed method
                students_utils = getUtility(IStudentsUtils)
                bed = students_utils.selectBed(available_beds)
                bed.bookBed(student.student_id)
            else:
                self.flash(_('There is no free bed in your category ${a}.',
                    mapping = {'a':self.acc_details['bt']}), type="warning")
                self.redirect(self.url(self.context))
                return
        if self.with_ac:
            # Mark pin as used (this also fires a pin related transition)
            if code.state == USED:
                self.flash(_('Activation code has already been used.'),
                           type="warning")
                if not manual:
                    # Release the previously booked bed
                    bed.owner = NOT_OCCUPIED
                    # Catalog must be informed
                    notify(grok.ObjectModifiedEvent(bed))
                return
            else:
                comment = _(u'invalidated')
                # Here we know that the ac is in state initialized so we do not
                # expect an exception, but the owner might be different
                success = invalidate_accesscode(
                    pin, comment, self.context.student.student_id)
                if not success:
                    self.flash(_('You are not the owner of this access code.'),
                               type="warning")
                    if not manual:
                        # Release the previously booked bed
                        bed.owner = NOT_OCCUPIED
                        # Catalog must be informed
                        notify(grok.ObjectModifiedEvent(bed))
                    return
        # Create bed ticket
        bedticket = createObject(u'waeup.BedTicket')
        if self.with_ac:
            bedticket.booking_code = pin
        bedticket.booking_session = self.acc_details['booking_session']
        bedticket.bed_type = self.acc_details['bt']
        bedticket.bed = bed
        hall_title = bed.__parent__.hostel_name
        coordinates = bed.coordinates[1:]
        block, room_nr, bed_nr = coordinates
        bc = _('${a}, Block ${b}, Room ${c}, Bed ${d} (${e})', mapping = {
            'a':hall_title, 'b':block,
            'c':room_nr, 'd':bed_nr,
            'e':bed.bed_type})
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        bedticket.bed_coordinates = translate(
            bc, 'waeup.kofa',target_language=portal_language)
        self.context.addBedTicket(bedticket)
        self.context.writeLogMessage(self, 'booked: %s' % bed.bed_id)
        self.flash(_('Bed ticket created and bed booked: ${a}',
            mapping = {'a':bedticket.display_coordinates}))
        self.redirect(self.url(self.context))
        return

class BedTicketDisplayFormPage(KofaDisplayFormPage):
    """ Page to display bed tickets
    """
    grok.context(IBedTicket)
    grok.name('index')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(IBedTicket).omit('bed_coordinates')
    form_fields['booking_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    pnav = 4

    @property
    def label(self):
        return _('Bed Ticket for Session ${a}',
            mapping = {'a':self.context.getSessionString()})

class ExportPDFBedTicketSlip(UtilityView, grok.View):
    """Deliver a PDF slip of the context.
    """
    grok.context(IBedTicket)
    grok.name('bed_allocation_slip.pdf')
    grok.require('waeup.viewStudent')
    form_fields = grok.AutoFields(IBedTicket).omit('bed_coordinates')
    form_fields['booking_date'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    prefix = 'form'
    omit_fields = (
        'password', 'suspended', 'phone', 'adm_code',
        'suspended_comment', 'date_of_birth', 'current_level',
        'flash_notice')

    @property
    def title(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return translate(_('Bed Allocation Data'), 'waeup.kofa',
            target_language=portal_language)

    @property
    def label(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        #return translate(_('Bed Allocation: '),
        #    'waeup.kofa', target_language=portal_language) \
        #    + ' %s' % self.context.bed_coordinates
        return translate(_('Bed Allocation Slip'),
            'waeup.kofa', target_language=portal_language) \
            + ' %s' % self.context.getSessionString()

    def render(self):
        studentview = StudentBasePDFFormPage(self.context.student,
            self.request, self.omit_fields)
        students_utils = getUtility(IStudentsUtils)
        note = None
        n = grok.getSite()['hostels'].allocation_expiration
        if n:
            note = _("""
<br /><br /><br /><br /><br /><font size="12">
Please endeavour to pay your hostel maintenance charge within ${a} days
 of being allocated a space or else you are deemed to have
 voluntarily forfeited it and it goes back into circulation to be
 available for booking afresh!</font>)
""")
            note = _(note, mapping={'a': n})
            portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
            note = translate(
                note, 'waeup.kofa', target_language=portal_language)
        return students_utils.renderPDF(
            self, 'bed_allocation_slip.pdf',
            self.context.student, studentview,
            omit_fields=self.omit_fields,
            note=note)

class BedTicketRelocationView(UtilityView, grok.View):
    """ Callback view
    """
    grok.context(IBedTicket)
    grok.name('relocate')
    grok.require('waeup.manageHostels')

    # Relocate student if student parameters have changed or the bed_type
    # of the bed has changed
    def update(self):
        success, msg = self.context.relocateStudent()
        if not success:
            self.flash(msg, type="warning")
        else:
            self.flash(msg)
        self.redirect(self.url(self.context))
        return

    def render(self):
        return

class StudentHistoryPage(KofaPage):
    """ Page to display student history
    """
    grok.context(IStudent)
    grok.name('history')
    grok.require('waeup.viewStudent')
    grok.template('studenthistory')
    pnav = 4

    @property
    def label(self):
        return _('${a}: History', mapping = {'a':self.context.display_fullname})

# Pages for students only

class StudentBaseEditFormPage(KofaEditFormPage):
    """ View to edit student base data
    """
    grok.context(IStudent)
    grok.name('edit_base')
    grok.require('waeup.handleStudent')
    form_fields = grok.AutoFields(IStudentBase).select(
        'email', 'phone', 'parents_email')
    label = _('Edit base data')
    pnav = 4

    @action(_('Save'), style='primary')
    def save(self, **data):
        msave(self, **data)
        return

class StudentChangePasswordPage(KofaEditFormPage):
    """ View to edit student passwords
    """
    grok.context(IStudent)
    grok.name('change_password')
    grok.require('waeup.handleStudent')
    grok.template('change_password')
    label = _('Change password')
    pnav = 4

    @action(_('Save'), style='primary')
    def save(self, **data):
        form = self.request.form
        password = form.get('change_password', None)
        password_ctl = form.get('change_password_repeat', None)
        if password:
            validator = getUtility(IPasswordValidator)
            errors = validator.validate_password(password, password_ctl)
            if not errors:
                IUserAccount(self.context).setPassword(password)
                # Unset temporary password
                self.context.temp_password = None
                self.context.writeLogMessage(self, 'saved: password')
                self.flash(_('Password changed.'))
            else:
                self.flash( ' '.join(errors), type="warning")
        return

class StudentFilesUploadPage(KofaPage):
    """ View to upload passport picture by student. The class name
    is historical. The page is only used for the student's portrait.
    """
    grok.context(IStudent)
    grok.name('change_portrait')
    grok.require('waeup.uploadStudentFile')
    grok.template('filesuploadpage')
    label = _('Upload portrait')
    pnav = 4

    def update(self):
        if not getUtility(IStudentsUtils).allowPortraitChange(self.context):
            emit_lock_message(self,
                _('This form is locked. You are in the wrong state.'))
            return
        super(StudentFilesUploadPage, self).update()
        return

class StudentSignatureUploadPage(KofaPage):
    """ View to upload scanned signature by student. Not active
    in base package.
    """
    grok.context(IStudent)
    grok.name('change_signature')
    grok.require('waeup.uploadStudentFile')
    grok.template('filesuploadpage')
    label = _('Upload signature')
    pnav = 4

    def update(self):
        SIGNATURE_CHANGE_STATES = getUtility(IStudentsUtils).SIGNATURE_CHANGE_STATES
        if self.context.student.state not in SIGNATURE_CHANGE_STATES:
            emit_lock_message(self,
                _('This form is locked. You are in the wrong state.'))
            return
        super(StudentSignatureUploadPage, self).update()
        return

class StartClearancePage(KofaPage):
    grok.context(IStudent)
    grok.name('start_clearance')
    grok.require('waeup.handleStudent')
    grok.template('enterpin')
    label = _('Start clearance')
    ac_prefix = 'CLR'
    notice = ''
    pnav = 4
    buttonname = _('Start clearance now')
    with_ac = True

    @property
    def all_required_fields_filled(self):
        if not self.context.email:
            return _("Email address is missing."), 'edit_base'
        if not self.context.phone:
            return _("Phone number is missing."), 'edit_base'
        return

    @property
    def portrait_uploaded(self):
        store = getUtility(IExtFileStore)
        if store.getFileByContext(self.context, attr=u'passport.jpg'):
            return True
        return False

    def update(self, SUBMIT=None):
        if not self.context.state == ADMITTED:
            self.flash(_("Wrong state"), type="warning")
            self.redirect(self.url(self.context))
            return
        if not self.portrait_uploaded:
            self.flash(_("No portrait uploaded."), type="warning")
            self.redirect(self.url(self.context, 'change_portrait'))
            return
        if self.all_required_fields_filled:
            arf_warning = self.all_required_fields_filled[0]
            arf_redirect = self.all_required_fields_filled[1]
            self.flash(arf_warning, type="warning")
            self.redirect(self.url(self.context, arf_redirect))
            return
        if self.with_ac:
            self.ac_series = self.request.form.get('ac_series', None)
            self.ac_number = self.request.form.get('ac_number', None)
        if SUBMIT is None:
            return
        if self.with_ac:
            pin = '%s-%s-%s' % (self.ac_prefix, self.ac_series, self.ac_number)
            code = get_access_code(pin)
            if not code:
                self.flash(_('Activation code is invalid.'), type="warning")
                return
            if code.state == USED:
                self.flash(_('Activation code has already been used.'),
                           type="warning")
                return
            # Mark pin as used (this also fires a pin related transition)
            # and fire transition start_clearance
            comment = _(u"invalidated")
            # Here we know that the ac is in state initialized so we do not
            # expect an exception, but the owner might be different
            if not invalidate_accesscode(pin, comment, self.context.student_id):
                self.flash(_('You are not the owner of this access code.'),
                           type="warning")
                return
            self.context.clr_code = pin
        IWorkflowInfo(self.context).fireTransition('start_clearance')
        self.flash(_('Clearance process has been started.'))
        self.redirect(self.url(self.context,'cedit'))
        return

class StudentClearanceEditFormPage(StudentClearanceManageFormPage):
    """ View to edit student clearance data by student
    """
    grok.context(IStudent)
    grok.name('cedit')
    grok.require('waeup.handleStudent')
    label = _('Edit clearance data')

    @property
    def form_fields(self):
        if self.context.is_postgrad:
            form_fields = grok.AutoFields(IPGStudentClearance).omit(
                'clr_code', 'officer_comment')
        else:
            form_fields = grok.AutoFields(IUGStudentClearance).omit(
                'clr_code', 'officer_comment')
        return form_fields

    def update(self):
        if self.context.clearance_locked:
            emit_lock_message(self)
            return
        return super(StudentClearanceEditFormPage, self).update()

    @action(_('Save'), style='primary')
    def save(self, **data):
        self.applyData(self.context, **data)
        self.flash(_('Clearance form has been saved.'))
        return

    def dataNotComplete(self):
        """To be implemented in the customization package.
        """
        return False

    @action(_('Save and request clearance'), style='primary',
            warning=_('You can not edit your data after '
            'requesting clearance. You really want to request clearance now?'))
    def requestClearance(self, **data):
        self.applyData(self.context, **data)
        if self.dataNotComplete():
            self.flash(self.dataNotComplete(), type="warning")
            return
        self.flash(_('Clearance form has been saved.'))
        if self.context.clr_code:
            self.redirect(self.url(self.context, 'request_clearance'))
        else:
            # We bypass the request_clearance page if student
            # has been imported in state 'clearance started' and
            # no clr_code was entered before.
            state = IWorkflowState(self.context).getState()
            if state != CLEARANCE:
                # This shouldn't happen, but the application officer
                # might have forgotten to lock the form after changing the state
                self.flash(_('This form cannot be submitted. Wrong state!'),
                           type="danger")
                return
            IWorkflowInfo(self.context).fireTransition('request_clearance')
            self.flash(_('Clearance has been requested.'))
            self.redirect(self.url(self.context))
        return

class RequestClearancePage(KofaPage):
    grok.context(IStudent)
    grok.name('request_clearance')
    grok.require('waeup.handleStudent')
    grok.template('enterpin')
    label = _('Request clearance')
    notice = _('Enter the CLR access code used for starting clearance.')
    ac_prefix = 'CLR'
    pnav = 4
    buttonname = _('Request clearance now')
    with_ac = True

    def update(self, SUBMIT=None):
        if self.with_ac:
            self.ac_series = self.request.form.get('ac_series', None)
            self.ac_number = self.request.form.get('ac_number', None)
        if SUBMIT is None:
            return
        if self.with_ac:
            pin = '%s-%s-%s' % (self.ac_prefix, self.ac_series, self.ac_number)
            if self.context.clr_code and self.context.clr_code != pin:
                self.flash(_("This isn't your CLR access code."), type="danger")
                return
        state = IWorkflowState(self.context).getState()
        if state != CLEARANCE:
            # This shouldn't happen, but the application officer
            # might have forgotten to lock the form after changing the state
            self.flash(_('This form cannot be submitted. Wrong state!'),
                       type="danger")
            return
        IWorkflowInfo(self.context).fireTransition('request_clearance')
        self.flash(_('Clearance has been requested.'))
        self.redirect(self.url(self.context))
        return

class StartSessionPage(KofaPage):
    grok.context(IStudentStudyCourse)
    grok.name('start_session')
    grok.require('waeup.handleStudent')
    grok.template('enterpin')
    label = _('Start session')
    ac_prefix = 'SFE'
    notice = ''
    pnav = 4
    buttonname = _('Start now')
    with_ac = True

    def update(self, SUBMIT=None):
        if not self.context.is_current:
            emit_lock_message(self)
            return
        super(StartSessionPage, self).update()
        if not self.context.next_session_allowed:
            self.flash(_("You are not entitled to start session."),
                       type="warning")
            self.redirect(self.url(self.context))
            return
        if self.with_ac:
            self.ac_series = self.request.form.get('ac_series', None)
            self.ac_number = self.request.form.get('ac_number', None)
        if SUBMIT is None:
            return
        if self.with_ac:
            pin = '%s-%s-%s' % (self.ac_prefix, self.ac_series, self.ac_number)
            code = get_access_code(pin)
            if not code:
                self.flash(_('Activation code is invalid.'), type="warning")
                return
            # Mark pin as used (this also fires a pin related transition)
            if code.state == USED:
                self.flash(_('Activation code has already been used.'),
                           type="warning")
                return
            else:
                comment = _(u"invalidated")
                # Here we know that the ac is in state initialized so we do not
                # expect an error, but the owner might be different
                if not invalidate_accesscode(
                    pin,comment,self.context.student.student_id):
                    self.flash(_('You are not the owner of this access code.'),
                               type="warning")
                    return
        try:
            if self.context.student.state == CLEARED:
                IWorkflowInfo(self.context.student).fireTransition(
                    'pay_first_school_fee')
            elif self.context.student.state == RETURNING:
                IWorkflowInfo(self.context.student).fireTransition(
                    'pay_school_fee')
            elif self.context.student.state == PAID:
                IWorkflowInfo(self.context.student).fireTransition(
                    'pay_pg_fee')
        except ConstraintNotSatisfied:
            self.flash(_('An error occurred, please contact the system administrator.'),
                       type="danger")
            return
        self.flash(_('Session started.'))
        self.redirect(self.url(self.context))
        return

class AddStudyLevelFormPage(KofaEditFormPage):
    """ Page for students to add current study levels
    """
    grok.context(IStudentStudyCourse)
    grok.name('add')
    grok.require('waeup.handleStudent')
    grok.template('studyleveladdpage')
    form_fields = grok.AutoFields(IStudentStudyCourse)
    pnav = 4

    @property
    def label(self):
        studylevelsource = StudyLevelSource().factory
        code = self.context.current_level
        title = studylevelsource.getTitle(self.context, code)
        return _('Add current level ${a}', mapping = {'a':title})

    def update(self):
        if not self.context.is_current \
            or self.context.student.studycourse_locked:
            emit_lock_message(self)
            return
        if self.context.student.state != PAID:
            emit_lock_message(self)
            return
        code = self.context.current_level
        if code is None:
            self.flash(_('Your data are incomplete'), type="danger")
            self.redirect(self.url(self.context))
            return
        super(AddStudyLevelFormPage, self).update()
        return

    @action(_('Create course list now'), style='primary')
    def addStudyLevel(self, **data):
        studylevel = createObject(u'waeup.StudentStudyLevel')
        studylevel.level = self.context.current_level
        studylevel.level_session = self.context.current_session
        try:
            self.context.addStudentStudyLevel(
                self.context.certificate,studylevel)
        except KeyError:
            self.flash(_('This level exists.'), type="warning")
            self.redirect(self.url(self.context))
            return
        except RequiredMissing:
            self.flash(_('Your data are incomplete.'), type="danger")
            self.redirect(self.url(self.context))
            return
        self.flash(_('You successfully created a new course list.'))
        self.redirect(self.url(self.context, str(studylevel.level)))
        return

class StudyLevelEditFormPage(KofaEditFormPage):
    """ Page to edit the student study level data by students
    """
    grok.context(IStudentStudyLevel)
    grok.name('edit')
    grok.require('waeup.editStudyLevel')
    grok.template('studyleveleditpage')
    pnav = 4
    placeholder = _('Enter valid course code')

    def update(self, ADD=None, course=None):
        if not self.context.__parent__.is_current:
            emit_lock_message(self)
            return
        if self.context.student.state != PAID or \
            not self.context.is_current_level:
            emit_lock_message(self)
            return
        super(StudyLevelEditFormPage, self).update()
        if ADD is not None:
            if not course:
                self.flash(_('No valid course code entered.'), type="warning")
                return
            cat = queryUtility(ICatalog, name='courses_catalog')
            result = cat.searchResults(code=(course, course))
            if len(result) != 1:
                self.flash(_('Course not found.'), type="warning")
                return
            course = list(result)[0]
            if course.former_course:
                self.flash(_('Former courses can\'t be added.'), type="warning")
                return
            addCourseTicket(self, course)
        return

    @property
    def label(self):
        # Here we know that the cookie has been set
        lang = self.request.cookies.get('kofa.language')
        level_title = translate(self.context.level_title, 'waeup.kofa',
            target_language=lang)
        return _('Edit course list of ${a}',
            mapping = {'a':level_title})

    @property
    def translated_values(self):
        return translated_values(self)

    def _delCourseTicket(self, **data):
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No ticket selected.'), type="warning")
            self.redirect(self.url(self.context, '@@edit'))
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        deleted = []
        for id in child_id:
            # Students are not allowed to remove core tickets
            if id in self.context and \
                self.context[id].removable_by_student:
                del self.context[id]
                deleted.append(id)
        if len(deleted):
            self.flash(_('Successfully removed: ${a}',
                mapping = {'a':', '.join(deleted)}))
            self.context.writeLogMessage(
                self,'removed: %s at %s' %
                (', '.join(deleted), self.context.level))
        self.redirect(self.url(self.context, u'@@edit'))
        return

    @jsaction(_('Remove selected tickets'))
    def delCourseTicket(self, **data):
        self._delCourseTicket(**data)
        return

    def _updateTickets(self, **data):
        cat = queryUtility(ICatalog, name='courses_catalog')
        invalidated = list()
        for value in self.context.values():
            result = cat.searchResults(code=(value.code, value.code))
            if len(result) != 1:
                course = None
            else:
                course = list(result)[0]
            invalid = self.context.updateCourseTicket(value, course)
            if invalid:
                invalidated.append(invalid)
        if invalidated:
            invalidated_string = ', '.join(invalidated)
            self.context.writeLogMessage(
                self, 'course tickets invalidated: %s' % invalidated_string)
        self.flash(_('All course tickets updated.'))
        return

    @action(_('Update all tickets'),
        tooltip=_('Update all course parameters including course titles.'))
    def updateTickets(self, **data):
        self._updateTickets(**data)
        return

    def _registerCourses(self, **data):
        if self.context.student.is_postgrad and \
            not self.context.student.is_special_postgrad:
            self.flash(_(
                "You are a postgraduate student, "
                "your course list can't bee registered."), type="warning")
            self.redirect(self.url(self.context))
            return
        students_utils = getUtility(IStudentsUtils)
        warning = students_utils.warnCreditsOOR(self.context)
        if warning:
            self.flash(warning, type="warning")
            return
        msg = self.context.course_registration_forbidden
        if msg:
            self.flash(msg, type="warning")
            return
        IWorkflowInfo(self.context.student).fireTransition(
            'register_courses')
        self.flash(_('Course list has been registered.'))
        self.redirect(self.url(self.context))
        return

    @action(_('Register course list'), style='primary',
        warning=_('You can not edit your course list after registration.'
            ' You really want to register?'))
    def registerCourses(self, **data):
        self._registerCourses(**data)
        return

class CourseTicketAddFormPage2(CourseTicketAddFormPage):
    """Add a course ticket by student.
    """
    grok.name('ctadd')
    grok.require('waeup.handleStudent')
    form_fields = grok.AutoFields(ICourseTicketAdd)

    def update(self):
        if self.context.student.state != PAID or \
            not self.context.is_current_level:
            emit_lock_message(self)
            return
        super(CourseTicketAddFormPage2, self).update()
        return

    @action(_('Add course ticket'))
    def addCourseTicket(self, **data):
        # Safety belt
        if self.context.student.state != PAID:
            return
        course = data['course']
        if course.former_course:
            self.flash(_('Former courses can\'t be added.'), type="warning")
            return
        success = addCourseTicket(self, course)
        if success:
            self.redirect(self.url(self.context, u'@@edit'))
        return

class SetPasswordPage(KofaPage):
    grok.context(IKofaObject)
    grok.name('setpassword')
    grok.require('waeup.Anonymous')
    grok.template('setpassword')
    label = _('Set password for first-time login')
    ac_prefix = 'PWD'
    pnav = 0
    set_button = _('Set')

    def update(self, SUBMIT=None):
        self.reg_number = self.request.form.get('reg_number', None)
        self.ac_series = self.request.form.get('ac_series', None)
        self.ac_number = self.request.form.get('ac_number', None)

        if SUBMIT is None:
            return
        hitlist = search(query=self.reg_number,
            searchtype='reg_number', view=self)
        if not hitlist:
            self.flash(_('No student found.'), type="warning")
            return
        if len(hitlist) != 1:   # Cannot happen but anyway
            self.flash(_('More than one student found.'), type="warning")
            return
        student = hitlist[0].context
        self.student_id = student.student_id
        student_pw = student.password
        pin = '%s-%s-%s' % (self.ac_prefix, self.ac_series, self.ac_number)
        code = get_access_code(pin)
        if not code:
            self.flash(_('Access code is invalid.'), type="warning")
            return
        if student_pw and pin == student.adm_code:
            self.flash(_(
                'Password has already been set. Your Student Id is ${a}',
                mapping = {'a':self.student_id}))
            return
        elif student_pw:
            self.flash(
                _('Password has already been set. You are using the ' +
                'wrong Access Code.'), type="warning")
            return
        # Mark pin as used (this also fires a pin related transition)
        # and set student password
        if code.state == USED:
            self.flash(_('Access code has already been used.'), type="warning")
            return
        else:
            comment = _(u"invalidated")
            # Here we know that the ac is in state initialized so we do not
            # expect an exception
            invalidate_accesscode(pin,comment)
            IUserAccount(student).setPassword(self.ac_number)
            student.adm_code = pin
        self.flash(_('Password has been set. Your Student Id is ${a}',
            mapping = {'a':self.student_id}))
        return

class StudentRequestPasswordPage(KofaAddFormPage):
    """Captcha'd request password page for students.
    """
    grok.name('requestpw')
    grok.require('waeup.Anonymous')
    grok.template('requestpw')
    form_fields = grok.AutoFields(IStudentRequestPW).select(
        'lastname','number','email')
    label = _('Request password for first-time login')

    def update(self):
        blocker = grok.getSite()['configuration'].maintmode_enabled_by
        if blocker:
            self.flash(_('The portal is in maintenance mode. '
                        'Password request forms are temporarily disabled.'),
                       type='warning')
            self.redirect(self.url(self.context))
            return
        # Handle captcha
        self.captcha = getUtility(ICaptchaManager).getCaptcha()
        self.captcha_result = self.captcha.verify(self.request)
        self.captcha_code = self.captcha.display(self.captcha_result.error_code)
        return

    def _redirect(self, email, password, student_id):
        # Forward only email to landing page in base package.
        self.redirect(self.url(self.context, 'requestpw_complete',
            data = dict(email=email)))
        return

    def _redirect_no_student(self):
        # No record found, this is the truth. We do not redirect here.
        # We are using this method in custom packages
        # for redirecting alumni to the application section.
        self.flash(_('No student record found.'), type="warning")
        return

    def _pw_used(self):
        # XXX: False if password has not been used. We need an extra
        #      attribute which remembers if student logged in.
        return True

    @action(_('Send login credentials to email address'), style='primary')
    def get_credentials(self, **data):
        if not self.captcha_result.is_valid:
            # Captcha will display error messages automatically.
            # No need to flash something.
            return
        number = data.get('number','')
        lastname = data.get('lastname','')
        cat = getUtility(ICatalog, name='students_catalog')
        results = list(
            cat.searchResults(reg_number=(number, number)))
        if not results:
            results = list(
                cat.searchResults(matric_number=(number, number)))
        if results:
            student = results[0]
            if getattr(student,'lastname',None) is None:
                self.flash(_('An error occurred.'), type="danger")
                return
            elif student.lastname.lower() != lastname.lower():
                # Don't tell the truth here. Anonymous must not
                # know that a record was found and only the lastname
                # verification failed.
                self.flash(_('No student record found.'), type="warning")
                return
            elif student.password is not None and self._pw_used:
                self.flash(_('Your password has already been set and used. '
                             'Please proceed to the login page.'),
                           type="warning")
                return
            # Store email address but nothing else.
            student.email = data['email']
            notify(grok.ObjectModifiedEvent(student))
        else:
            self._redirect_no_student()
            return

        kofa_utils = getUtility(IKofaUtils)
        password = kofa_utils.genPassword()
        mandate = PasswordMandate()
        mandate.params['password'] = password
        mandate.params['user'] = student
        site = grok.getSite()
        site['mandates'].addMandate(mandate)
        # Send email with credentials
        args = {'mandate_id':mandate.mandate_id}
        mandate_url = self.url(site) + '/mandate?%s' % urlencode(args)
        url_info = u'Confirmation link: %s' % mandate_url
        msg = _('You have successfully requested a password for the')
        if kofa_utils.sendCredentials(IUserAccount(student),
            password, url_info, msg):
            email_sent = student.email
        else:
            email_sent = None
        self._redirect(email=email_sent, password=password,
            student_id=student.student_id)
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        self.context.logger.info(
            '%s - %s (%s) - %s' % (ob_class, number, student.student_id, email_sent))
        return

class ParentsUser:
    pass

class RequestParentsPasswordPage(StudentRequestPasswordPage):
    """Captcha'd request password page for parents.
    """
    grok.name('requestppw')
    grok.template('requestppw')
    label = _('Request password for parents access')

    def update(self):
        super(RequestParentsPasswordPage, self).update()
        kofa_utils = getUtility(IKofaUtils)
        self.temp_password_minutes = kofa_utils.TEMP_PASSWORD_MINUTES
        return

    @action(_('Send temporary login credentials to email address'), style='primary')
    def get_credentials(self, **data):
        if not self.captcha_result.is_valid:
            # Captcha will display error messages automatically.
            # No need to flash something.
            return
        number = data.get('number','')
        lastname = data.get('lastname','')
        email = data['email']
        cat = getUtility(ICatalog, name='students_catalog')
        results = list(
            cat.searchResults(reg_number=(number, number)))
        if not results:
            results = list(
                cat.searchResults(matric_number=(number, number)))
        if results:
            student = results[0]
            if getattr(student,'lastname',None) is None:
                self.flash(_('An error occurred.'), type="danger")
                return
            elif student.lastname.lower() != lastname.lower():
                # Don't tell the truth here. Anonymous must not
                # know that a record was found and only the lastname
                # verification failed.
                self.flash(_('No student record found.'), type="warning")
                return
            elif email != student.parents_email:
                self.flash(_('Wrong email address.'), type="warning")
                return
        else:
            self._redirect_no_student()
            return
        kofa_utils = getUtility(IKofaUtils)
        password = kofa_utils.genPassword()
        mandate = ParentsPasswordMandate()
        mandate.params['password'] = password
        mandate.params['student'] = student
        site = grok.getSite()
        site['mandates'].addMandate(mandate)
        # Send email with credentials
        args = {'mandate_id':mandate.mandate_id}
        mandate_url = self.url(site) + '/mandate?%s' % urlencode(args)
        url_info = u'Confirmation link: %s' % mandate_url
        msg = _('You have successfully requested a parents password for the')
        # Create a fake user
        user = ParentsUser()
        user.name = student.student_id
        user.title = "Parents of %s" % student.display_fullname
        user.email = student.parents_email
        if kofa_utils.sendCredentials(user, password, url_info, msg):
            email_sent = user.email
        else:
            email_sent = None
        self._redirect(email=email_sent, password=password,
            student_id=student.student_id)
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        self.context.logger.info(
            '%s - %s (%s) - %s' % (ob_class, number, student.student_id, email_sent))
        return

class StudentRequestPasswordEmailSent(KofaPage):
    """Landing page after successful password request.

    """
    grok.name('requestpw_complete')
    grok.require('waeup.Public')
    grok.template('requestpwmailsent')
    label = _('Your password request was successful.')

    def update(self, email=None, student_id=None, password=None):
        self.email = email
        self.password = password
        self.student_id = student_id
        return

class FilterStudentsInDepartmentPage(KofaPage):
    """Page that filters and lists students.
    """
    grok.context(IDepartment)
    grok.require('waeup.showStudents')
    grok.name('students')
    grok.template('filterstudentspage')
    pnav = 1
    session_label = _('Current Session')
    level_label = _('Current Level')

    def label(self):
        return 'Students in %s' % self.context.longtitle

    def _set_session_values(self):
        vocab_terms = academic_sessions_vocab.by_value.values()
        self.sessions = sorted(
            [(x.title, x.token) for x in vocab_terms], reverse=True)
        self.sessions += [('All Sessions', 'all')]
        return

    def _set_level_values(self):
        vocab_terms = course_levels.by_value.values()
        self.levels = sorted(
            [(x.title, x.token) for x in vocab_terms])
        self.levels += [('All Levels', 'all')]
        return

    def _searchCatalog(self, session, level):
        if level not in (10, 999, 1000, None):
            start_level = 100 * (level // 100)
            end_level = start_level + 90
        else:
            start_level = end_level = level
        cat = queryUtility(ICatalog, name='students_catalog')
        students = cat.searchResults(
            current_session=(session, session),
            current_level=(start_level, end_level),
            depcode=(self.context.code, self.context.code)
            )
        hitlist = []
        for student in students:
            hitlist.append(StudentQueryResultItem(student, view=self))
        return hitlist

    def update(self, SHOW=None, session=None, level=None):
        self.parent_url = self.url(self.context.__parent__)
        self._set_session_values()
        self._set_level_values()
        self.hitlist = []
        self.session_default = session
        self.level_default = level
        if SHOW is not None:
            if session != 'all':
                self.session = int(session)
                self.session_string = '%s %s/%s' % (
                    self.session_label, self.session, self.session+1)
            else:
                self.session = None
                self.session_string = _('in any session')
            if level != 'all':
                self.level = int(level)
                self.level_string = '%s %s' % (self.level_label, self.level)
            else:
                self.level = None
                self.level_string = _('at any level')
            self.hitlist = self._searchCatalog(self.session, self.level)
            if not self.hitlist:
                self.flash(_('No student found.'), type="warning")
        return

class FilterStudentsInCertificatePage(FilterStudentsInDepartmentPage):
    """Page that filters and lists students.
    """
    grok.context(ICertificate)

    def label(self):
        return 'Students studying %s' % self.context.longtitle

    def _searchCatalog(self, session, level):
        if level not in (10, 999, 1000, None):
            start_level = 100 * (level // 100)
            end_level = start_level + 90
        else:
            start_level = end_level = level
        cat = queryUtility(ICatalog, name='students_catalog')
        students = cat.searchResults(
            current_session=(session, session),
            current_level=(start_level, end_level),
            certcode=(self.context.code, self.context.code)
            )
        hitlist = []
        for student in students:
            hitlist.append(StudentQueryResultItem(student, view=self))
        return hitlist

class FilterStudentsInCoursePage(FilterStudentsInDepartmentPage):
    """Page that filters and lists students.
    """
    grok.context(ICourse)
    grok.require('waeup.viewStudent')

    session_label = _('Session')
    level_label = _('Level')

    def label(self):
        return 'Students registered for %s' % self.context.longtitle

    def _searchCatalog(self, session, level):
        if level not in (10, 999, 1000, None):
            start_level = 100 * (level // 100)
            end_level = start_level + 90
        else:
            start_level = end_level = level
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        coursetickets = cat.searchResults(
            session=(session, session),
            level=(start_level, end_level),
            code=(self.context.code, self.context.code)
            )
        hitlist = []
        for ticket in coursetickets:
            hitlist.append(StudentQueryResultItem(ticket.student, view=self))
        return list(set(hitlist))

class ClearAllStudentsInDepartmentView(UtilityView, grok.View):
    """ Clear all students of a department in state 'clearance requested'.
    """
    grok.context(IDepartment)
    grok.name('clearallstudents')
    grok.require('waeup.clearAllStudents')

    def update(self):
        cat = queryUtility(ICatalog, name='students_catalog')
        students = cat.searchResults(
            depcode=(self.context.code, self.context.code),
            state=(REQUESTED, REQUESTED)
            )
        num = 0
        for student in students:
            if getUtility(IStudentsUtils).clearance_disabled_message(student):
                continue
            IWorkflowInfo(student).fireTransition('clear')
            num += 1
        self.flash(_('%d students have been cleared.' % num))
        self.redirect(self.url(self.context))
        return

    def render(self):
        return

#class RemoveFlashNoticeAllStudentsInDepartmentView(UtilityView, grok.View):
#    """ Remove flash notices of all students in a department.
#    """
#    grok.context(IDepartment)
#    grok.name('removeflash')
#    grok.require('waeup.manageStudent')

#    def update(self):
#        cat = queryUtility(ICatalog, name='students_catalog')
#        students = cat.searchResults(
#            depcode=(self.context.code, self.context.code),
#            )
#        num = 0
#        for student in students:
#            student.flash_notice = u''
#            num += 1
#        self.flash(_('%d flash notices have been removed.' % num))
#        self.redirect(self.url(self.context))
#        return

#    def render(self):
#        return

class EditFlashNoticesFormPage(KofaFormPage):
    """Edit all flash notices of students in a department.
    """
    grok.context(IDepartment)
    grok.name('edit_flash_notices')
    grok.template('editflashnotices')
    grok.require('waeup.manageStudent')
    form_fields = grok.AutoFields(IFlashNotice)
    pnav = 0

    def label(self):
        return _(u'Set flash notices for all students in ${a}',
            mapping = {'a':self.context.longtitle})

    @action('Save flash notices', style='primary')
    def save(self, *args, **data):
        cat = queryUtility(ICatalog, name='students_catalog')
        students = cat.searchResults(
            depcode=(self.context.code, self.context.code),
            )
        num = 0
        for student in students:
            student.flash_notice = data['flash_notice']
            num += 1
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        grok.getSite().logger.info(
            '%s - %s - saved flash notice: %s'
            % (ob_class, self.context.__name__, data['flash_notice']))
        self.flash(_('%d flash notices have been edited.' % num))
        self.redirect(self.url(self.context))
        return

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))

class EditScoresPage(KofaPage):
    """Page that allows to edit batches of scores.
    """
    grok.context(ICourse)
    grok.require('waeup.editScores')
    grok.name('edit_scores')
    grok.template('editscorespage')
    pnav = 1
    doclink = DOCLINK + '/students/browser.html#batch-editing-scores-by-lecturers'

    def label(self):
        return '%s tickets in academic session %s' % (
            self.context.code, self.session_title)

    def _searchCatalog(self, session):
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        # Attention: Also tickets of previous studycourses are found
        coursetickets = cat.searchResults(
            session=(session, session),
            code=(self.context.code, self.context.code)
            )
        return list(coursetickets)

    def _extract_uploadfile(self, uploadfile):
        """Get a mapping of student-ids to scores.

        The mapping is constructed by reading contents from `uploadfile`.

        We expect uploadfile to be a regular CSV file with columns
        ``student_id`` and ``score`` (other cols are ignored).
        """
        result = dict()
        data = StringIO(uploadfile.read())  # ensure we have something seekable
        reader = csv.DictReader(data)
        for row in reader:
            if not 'student_id' in row or not 'score' in row:
                continue
            result[row['student_id']] = row['score']
        return result

    def _update_scores(self, form):
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.', '')
        error = ''
        if 'UPDATE_FILE' in form:
            if form['uploadfile']:
                try:
                    formvals = self._extract_uploadfile(form['uploadfile'])
                except:
                    self.flash(
                        _('Uploaded file contains illegal data. Ignored'),
                        type="danger")
                    return False
            else:
                self.flash(
                    _('No file provided.'), type="danger")
                return False
        else:
            formvals = dict(zip(form['sids'], form['scores']))
        for ticket in self.editable_tickets:
            score = ticket.score
            sid = ticket.student.student_id
            if sid not in formvals:
                continue
            if formvals[sid] == '':
                score = None
            else:
                try:
                    score = int(formvals[sid])
                except ValueError:
                    error += '%s, ' % ticket.student.display_fullname
            if ticket.score != score:
                ticket.score = score
                ticket.student.__parent__.logger.info(
                    '%s - %s %s/%s score updated (%s)' % (
                        ob_class, ticket.student.student_id,
                        ticket.level, ticket.code, score)
                    )
        if error:
            self.flash(
                _('Error: Score(s) of following students have not been '
                    'updated (only integers are allowed): %s.' % error.strip(', ')),
                type="danger")
        return True

    def _validate_results(self, form):
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.', '')
        user = get_current_principal()
        if user is None:
            usertitle = 'system'
        else:
            usertitle = getattr(user, 'public_name', None)
            if not usertitle:
                usertitle = user.title
        self.context.results_validated_by = usertitle
        self.context.results_validation_date = datetime.utcnow()
        self.context.results_validation_session = self.current_academic_session
        return

    def _results_editable(self, results_validation_session,
                         current_academic_session):
        user = get_current_principal()
        prm = IPrincipalRoleManager(self.context)
        roles = [x[0] for x in prm.getRolesForPrincipal(user.id)]
        if 'waeup.local.LocalStudentsManager' in roles:
            return True
        if results_validation_session \
            and results_validation_session >= current_academic_session:
            return False
        return True

    def update(self,  *args, **kw):
        form = self.request.form
        self.current_academic_session = grok.getSite()[
            'configuration'].current_academic_session
        if self.context.__parent__.__parent__.score_editing_disabled \
            or self.context.score_editing_disabled:
            self.flash(_('Score editing disabled.'), type="warning")
            self.redirect(self.url(self.context))
            return
        if not self.current_academic_session:
            self.flash(_('Current academic session not set.'), type="warning")
            self.redirect(self.url(self.context))
            return
        vs = self.context.results_validation_session
        if not self._results_editable(vs, self.current_academic_session):
            self.flash(
                _('Course results have already been '
                  'validated and can no longer be changed.'),
                type="danger")
            self.redirect(self.url(self.context))
            return
        self.session_title = academic_sessions_vocab.getTerm(
            self.current_academic_session).title
        self.tickets = self._searchCatalog(self.current_academic_session)
        if not self.tickets:
            self.flash(_('No student found.'), type="warning")
            self.redirect(self.url(self.context))
            return
        self.editable_tickets = [
            ticket for ticket in self.tickets if ticket.editable_by_lecturer]
        if not 'UPDATE_TABLE' in form and not 'UPDATE_FILE' in form\
            and not 'VALIDATE_RESULTS' in form:
            return
        if 'VALIDATE_RESULTS' in form:
            if vs and vs >= self.current_academic_session:
                self.flash(
                    _('Course results have already been validated.'),
                    type="danger")
            for ticket in self.tickets:
                if ticket.total_score is not None:
                    break
                self.flash(
                    _('No score has been entered.'),
                    type="danger")
                return
            self._validate_results(form)
            self.flash(_('You successfully validated the course results.'))
            self.redirect(self.url(self.context))
            return
        if not self.editable_tickets:
            return
        success = self._update_scores(form)
        if success:
            self.flash(_('You successfully updated course results.'))
        return

class DownloadScoresView(UtilityView, grok.View):
    """View that exports scores.
    """
    grok.context(ICourse)
    grok.require('waeup.editScores')
    grok.name('download_scores')

    def _results_editable(self, results_validation_session,
                         current_academic_session):
        user = get_current_principal()
        prm = IPrincipalRoleManager(self.context)
        roles = [x[0] for x in prm.getRolesForPrincipal(user.id)]
        if 'waeup.local.LocalStudentsManager' in roles:
            return True
        if results_validation_session \
            and results_validation_session >= current_academic_session:
            return False
        return True

    def update(self):
        self.current_academic_session = grok.getSite()[
            'configuration'].current_academic_session
        if self.context.__parent__.__parent__.score_editing_disabled \
            or self.context.score_editing_disabled:
            self.flash(_('Score editing disabled.'), type="warning")
            self.redirect(self.url(self.context))
            return
        if not self.current_academic_session:
            self.flash(_('Current academic session not set.'), type="warning")
            self.redirect(self.url(self.context))
            return
        vs = self.context.results_validation_session
        if not self._results_editable(vs, self.current_academic_session):
            self.flash(
                _('Course results have already been '
                  'validated and can no longer be changed.'),
                type="danger")
            self.redirect(self.url(self.context))
            return
        site = grok.getSite()
        exporter = getUtility(ICSVExporter, name='lecturer')
        self.csv = exporter.export_filtered(site, filepath=None,
                                 catalog='coursetickets',
                                 session=self.current_academic_session,
                                 level=None,
                                 code=self.context.code)
        return

    def render(self):
        filename = 'results_%s_%s.csv' % (
            self.context.code, self.current_academic_session)
        self.response.setHeader(
            'Content-Type', 'text/csv; charset=UTF-8')
        self.response.setHeader(
            'Content-Disposition:', 'attachment; filename="%s' % filename)
        return self.csv

class ExportPDFScoresSlip(UtilityView, grok.View,
    LocalRoleAssignmentUtilityView):
    """Deliver a PDF slip of course tickets for a lecturer.
    """
    grok.context(ICourse)
    grok.name('coursetickets.pdf')
    grok.require('waeup.showStudents')

    def update(self):
        self.current_academic_session = grok.getSite()[
            'configuration'].current_academic_session
        if not self.current_academic_session:
            self.flash(_('Current academic session not set.'), type="danger")
            self.redirect(self.url(self.context))
            return

    @property
    def note(self):
        return

    def data(self, session):
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        # Attention: Also tickets of previous studycourses are found
        coursetickets = cat.searchResults(
            session=(session, session),
            code=(self.context.code, self.context.code)
            )
        header = [[_('S/N'),
                   _('Matric No.'),
                   _('Reg. No.'),
                   _('Fullname'),
                   _('Status'),
                   _('Course of Studies'),
                   _('Level'),
                   _('Score') ],]
        tickets = []
        for ticket in list(coursetickets):
            row = [ticket.student.matric_number,
                  ticket.student.reg_number,
                  ticket.student.display_fullname,
                  ticket.student.translated_state,
                  ticket.student.certcode,
                  ticket.level,
                  ticket.score,
                  ticket.student.lastname # for sorting only
                  ]
            tickets.append(row)
        data = sorted(tickets, key=lambda value: value[7])
        sn = 1
        for d in data:
            d.pop(7)
            d.insert(0, sn)
            sn += 1
        return header + data, None

    def render(self):
        lecturers = [i['user_title'] for i in self.getUsersWithLocalRoles()
                     if i['local_role'] == 'waeup.local.Lecturer']
        lecturers = sorted(lecturers)
        lecturers =  ', '.join(lecturers)
        students_utils = getUtility(IStudentsUtils)
        return students_utils.renderPDFCourseticketsOverview(
            self, 'coursetickets', self.current_academic_session,
            self.data(self.current_academic_session), lecturers,
            'landscape', 90, self.note)

class ExportAttendanceSlip(UtilityView, grok.View,
    LocalRoleAssignmentUtilityView):
    """Deliver a PDF slip of course tickets in attendance sheet format.
    """
    grok.context(ICourse)
    grok.name('attendance.pdf')
    grok.require('waeup.showStudents')

    def update(self):
        self.current_academic_session = grok.getSite()[
            'configuration'].current_academic_session
        if not self.current_academic_session:
            self.flash(_('Current academic session not set.'), type="danger")
            self.redirect(self.url(self.context))
            return

    @property
    def note(self):
        return

    def data(self, session):
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        # Attention: Also tickets of previous studycourses are found
        coursetickets = cat.searchResults(
            session=(session, session),
            code=(self.context.code, self.context.code)
            )
        header = [[_('S/N'),
                   _('Matric No.'),
                   _('Name'),
                   _('Level'),
                   _('Course of\nStudies'),
                   _('Booklet No.'),
                   _('Signature'),
                   ],]
        tickets = []
        sn = 1
        ctlist = sorted(list(coursetickets),
                        key=lambda value: str(value.student.faccode) +
                                          str(value.student.depcode) +
                                          str(value.student.certcode) +
                                          str(value.student.matric_number))
        # In AAUE only editable appear on the attendance sheet. Hopefully
        # this holds for other universities too.
        editable_tickets = [ticket for ticket in ctlist
            if ticket.editable_by_lecturer]
        for ticket in editable_tickets:
            name = textwrap.fill(ticket.student.display_fullname, 20)
            row = [sn,
                  ticket.student.matric_number,
                  name,
                  ticket.level,
                  ticket.student.certcode,
                  20 * ' ',
                  27 * ' ',
                  ]
            tickets.append(row)
            sn += 1
        return header + tickets, None

    def render(self):
        lecturers = [i['user_title'] for i in self.getUsersWithLocalRoles()
                     if i['local_role'] == 'waeup.local.Lecturer']
        lecturers =  ', '.join(lecturers)
        students_utils = getUtility(IStudentsUtils)
        return students_utils.renderPDFCourseticketsOverview(
            self, 'attendance', self.current_academic_session,
            self.data(self.current_academic_session),
            lecturers, '', 65, self.note)

class ExportJobContainerOverview(KofaPage):
    """Page that lists active student data export jobs and provides links
    to discard or download CSV files.

    """
    grok.context(VirtualExportJobContainer)
    grok.require('waeup.showStudents')
    grok.name('index.html')
    grok.template('exportjobsindex')
    label = _('Student Data Exports')
    pnav = 1
    doclink = DOCLINK + '/datacenter/export.html#student-data-exporters'

    def update(self, CREATE1=None, CREATE2=None, DISCARD=None, job_id=None):
        if CREATE1:
            self.redirect(self.url('@@exportconfig'))
            return
        if CREATE2:
            self.redirect(self.url('@@exportselected'))
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

class ExportJobContainerJobConfig(KofaPage):
    """Page that configures a students export job.

    This is a baseclass.
    """
    grok.baseclass()
    grok.require('waeup.showStudents')
    grok.template('exportconfig')
    label = _('Configure student data export')
    pnav = 1
    redirect_target = ''
    doclink = DOCLINK + '/datacenter/export.html#student-data-exporters'

    def _set_session_values(self):
        vocab_terms = academic_sessions_vocab.by_value.values()
        self.sessions = [(_('All Sessions'), 'all')]
        self.sessions += sorted(
            [(x.title, x.token) for x in vocab_terms], reverse=True)
        return

    def _set_level_values(self):
        vocab_terms = course_levels.by_value.values()
        self.levels = [(_('All Levels'), 'all')]
        self.levels += sorted(
            [(x.title, x.token) for x in vocab_terms])
        return

    def _set_semesters_values(self):
        utils = getUtility(IKofaUtils)
        self.semesters =[(_('All Semesters'), 'all')]
        self.semesters += sorted([(value, key) for key, value in
                      utils.SEMESTER_DICT.items()])
        return

    def _set_mode_values(self):
        utils = getUtility(IKofaUtils)
        self.modes =[(_('All Modes'), 'all')]
        self.modes += sorted([(value, key) for key, value in
                      utils.STUDY_MODES_DICT.items()])
        return

    def _set_paycat_values(self):
        utils = getUtility(IKofaUtils)
        self.paycats =[(_('All Payment Categories'), 'all')]
        self.paycats += sorted([(value, key) for key, value in
                      utils.PAYMENT_CATEGORIES.items()])
        return

    def _set_exporter_values(self):
        # We provide all student exporters, nothing else, yet.
        # Bursary, Department or Accommodation Officers don't
        # have the general exportData
        # permission and are only allowed to export bursary, payments
        # overview or accommodation data respectively.
        # This is the only place where waeup.exportAccommodationData,
        # waeup.exportBursaryData and waeup.exportPaymentsOverview
        # are used.
        exporters = []
        if not checkPermission('waeup.exportData', self.context):
            if checkPermission('waeup.exportBursaryData', self.context):
                exporters += [('Bursary Data', 'bursary')]
            if checkPermission('waeup.exportPaymentsOverview', self.context):
                exporters += [('School Fee Payments Overview',
                               'sfpaymentsoverview'),
                              ('Session Payments Overview',
                               'sessionpaymentsoverview')]
            if checkPermission('waeup.exportAccommodationData', self.context):
                exporters += [('Bed Tickets', 'bedtickets'),
                              ('Accommodation Payments',
                               'accommodationpayments')]
            self.exporters = exporters
            return
        STUDENT_EXPORTER_NAMES = getUtility(
            IStudentsUtils).STUDENT_EXPORTER_NAMES
        for name in STUDENT_EXPORTER_NAMES:
            util = getUtility(ICSVExporter, name=name)
            exporters.append((util.title, name),)
        self.exporters = exporters
        return

    @property
    def faccode(self):
        return None

    @property
    def depcode(self):
        return None

    @property
    def certcode(self):
        return None

    def update(self, START=None, session=None, level=None, mode=None,
               payments_start=None, payments_end=None, ct_level=None, 
               ct_session=None, ct_semester=None, paycat=None,
               paysession=None, level_session=None, exporter=None):
        self._set_session_values()
        self._set_level_values()
        self._set_mode_values()
        self._set_paycat_values()
        self._set_exporter_values()
        self._set_semesters_values()
        if START is None:
            return
        ena = exports_not_allowed(self)
        if ena:
            self.flash(ena, type='danger')
            return
        if payments_start or payments_end:
            date_format = '%d/%m/%Y'
            try:
                datetime.strptime(payments_start, date_format)
                datetime.strptime(payments_end, date_format)
            except ValueError:
                self.flash(_('Payment dates do not match format d/m/Y.'),
                           type="danger")
                return
        if session == 'all':
            session=None
        if level == 'all':
            level = None
        if mode == 'all':
            mode = None
        if (mode,
            level,
            session,
            self.faccode,
            self.depcode,
            self.certcode) == (None, None, None, None, None, None):
            # Export all students including those without certificate
            job_id = self.context.start_export_job(exporter,
                                          self.request.principal.id,
                                          payments_start = payments_start,
                                          payments_end = payments_end,
                                          paycat=paycat,
                                          paysession=paysession,
                                          ct_level = ct_level,
                                          ct_session = ct_session,
                                          ct_semester = ct_semester,
                                          level_session=level_session,
                                          )
        else:
            job_id = self.context.start_export_job(exporter,
                                          self.request.principal.id,
                                          current_session=session,
                                          current_level=level,
                                          current_mode=mode,
                                          faccode=self.faccode,
                                          depcode=self.depcode,
                                          certcode=self.certcode,
                                          payments_start = payments_start,
                                          payments_end = payments_end,
                                          paycat=paycat,
                                          paysession=paysession,
                                          ct_level = ct_level,
                                          ct_session = ct_session,
                                          ct_semester = ct_semester,
                                          level_session=level_session,)
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        self.context.logger.info(
            '%s - exported: %s (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s), job_id=%s'
            % (ob_class, exporter, session, level, mode, self.faccode,
            self.depcode, self.certcode, payments_start, payments_end,
            ct_level, ct_session, paycat, paysession, level_session, job_id))
        self.flash(_('Export started for students with') +
                   ' current_session=%s, current_level=%s, study_mode=%s' % (
                   session, level, mode))
        self.redirect(self.url(self.redirect_target))
        return

class ExportJobContainerDownload(ExportCSVView):
    """Page that downloads a students export csv file.

    """
    grok.context(VirtualExportJobContainer)
    grok.require('waeup.showStudents')

class DatacenterExportJobContainerJobConfig(ExportJobContainerJobConfig):
    """Page that configures a students export job in datacenter.

    """
    grok.name('exportconfig')
    grok.context(IDataCenter)
    redirect_target = '@@export'

class DatacenterExportJobContainerSelectStudents(ExportJobContainerJobConfig):
    """Page that configures a students export job in datacenter.

    """
    grok.name('exportselected')
    grok.context(IDataCenter)
    redirect_target = '@@export'
    grok.template('exportselected')

    def update(self, START=None, students=None, exporter=None):
        self._set_exporter_values()
        if START is None:
            return
        ena = exports_not_allowed(self)
        if ena:
            self.flash(ena, type='danger')
            return
        try:
            ids = students.replace(',', ' ').split()
        except:
            self.flash(sys.exc_info()[1])
            self.redirect(self.url(self.redirect_target))
            return
        job_id = self.context.start_export_job(
            exporter, self.request.principal.id, selected=ids)
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        self.context.logger.info(
            '%s - selected students exported: %s, job_id=%s' %
            (ob_class, exporter, job_id))
        self.flash(_('Export of selected students started.'))
        self.redirect(self.url(self.redirect_target))
        return

class FacultiesExportJobContainerJobConfig(
    DatacenterExportJobContainerJobConfig):
    """Page that configures a students export job in facultiescontainer.

    """
    grok.context(VirtualFacultiesExportJobContainer)
    redirect_target = ''

class FacultiesExportJobContainerSelectStudents(
    DatacenterExportJobContainerSelectStudents):
    """Page that configures a students export job in facultiescontainer.

    """
    grok.context(VirtualFacultiesExportJobContainer)
    redirect_target = ''

class FacultyExportJobContainerJobConfig(DatacenterExportJobContainerJobConfig):
    """Page that configures a students export job in faculties.

    """
    grok.context(VirtualFacultyExportJobContainer)
    redirect_target = ''

    @property
    def faccode(self):
        return self.context.__parent__.code

class DepartmentExportJobContainerJobConfig(
    DatacenterExportJobContainerJobConfig):
    """Page that configures a students export job in departments.

    """
    grok.context(VirtualDepartmentExportJobContainer)
    redirect_target = ''

    @property
    def depcode(self):
        return self.context.__parent__.code

class CertificateExportJobContainerJobConfig(
    DatacenterExportJobContainerJobConfig):
    """Page that configures a students export job for certificates.

    """
    grok.context(VirtualCertificateExportJobContainer)
    grok.template('exportconfig_certificate')
    redirect_target = ''

    @property
    def certcode(self):
        return self.context.__parent__.code

class CourseExportJobContainerJobConfig(
    DatacenterExportJobContainerJobConfig):
    """Page that configures a students export job for courses.

    In contrast to department or certificate student data exports the
    coursetickets_catalog is searched here. Therefore the update
    method from the base class is customized.
    """
    grok.context(VirtualCourseExportJobContainer)
    grok.template('exportconfig_course')
    redirect_target = ''

    def _set_exporter_values(self):
        # We provide only the 'coursetickets' and 'lecturer' exporter
        # but can add more.
        exporters = []
        for name in ('coursetickets', 'lecturer'):
            util = getUtility(ICSVExporter, name=name)
            exporters.append((util.title, name),)
        self.exporters = exporters
        return

    # Disabled on 10/03/21
    #def _set_session_values(self):
    #    # We allow only current academic session
    #    academic_session = grok.getSite()['configuration'].current_academic_session
    #    if not academic_session:
    #        self.sessions = []
    #        return
    #    x = academic_sessions_vocab.getTerm(academic_session)
    #    self.sessions = [(x.title, x.token)]
    #    return

    def _set_session_values(self):
        vocab_terms = academic_sessions_vocab.by_value.values()
        self.sessions = sorted(
            [(x.title, x.token) for x in vocab_terms], reverse=True)
        self.sessions += [('All Sessions', 'all')]
        return

    def update(self, START=None, session=None, level=None, mode=None,
               exporter=None):
        if not checkPermission('waeup.exportData', self.context):
            self.flash(_('Not permitted.'), type='danger')
            self.redirect(self.url(self.context))
            return
        self._set_session_values()
        self._set_level_values()
        self._set_mode_values()
        self._set_exporter_values()
        # Disabled on 10/03/21
        #if not self.sessions:
        #    self.flash(
        #        _('Academic session not set. '
        #          'Please contact the administrator.'),
        #        type='danger')
        #    self.redirect(self.url(self.context))
        #    return
        if START is None:
            return
        ena = exports_not_allowed(self)
        if ena:
            self.flash(ena, type='danger')
            return
        if session == 'all':
            session = None
        if level == 'all':
            level = None
        job_id = self.context.start_export_job(exporter,
                                      self.request.principal.id,
                                      # Use a different catalog and
                                      # pass different keywords than
                                      # for the (default) students_catalog
                                      catalog='coursetickets',
                                      session=session,
                                      level=level,
                                      code=self.context.__parent__.code)
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        self.context.logger.info(
            '%s - exported: %s (%s, %s, %s), job_id=%s'
            % (ob_class, exporter, session, level,
            self.context.__parent__.code, job_id))
        self.flash(_('Export started for course tickets with') +
                   ' level_session=%s, level=%s' % (
                   session, level))
        self.redirect(self.url(self.redirect_target))
        return
