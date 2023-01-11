## $Id: interfaces.py 17214 2022-12-09 10:20:52Z henrik $
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
import os
import re
import codecs
import zc.async.interfaces
import zope.i18nmessageid
from datetime import datetime
from hurry.file.interfaces import IFileRetrieval
from hurry.workflow.interfaces import IWorkflowInfo
from zc.sourcefactory.basic import BasicSourceFactory
from zope import schema
from zope.pluggableauth.interfaces import IPrincipalInfo
from zope.security.interfaces import IGroupClosureAwarePrincipal as IPrincipal
from zope.component import getUtility
from zope.component.interfaces import IObjectEvent
from zope.configuration.fields import Path
from zope.container.interfaces import INameChooser, IContainer
from zope.interface import Interface, Attribute
from zope.schema.interfaces import IObject
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from waeup.kofa.schema import PhoneNumber
from waeup.kofa.sourcefactory import SmartBasicContextualSourceFactory

_ = MessageFactory = zope.i18nmessageid.MessageFactory('waeup.kofa')

DELETION_MARKER = 'XXX'
IGNORE_MARKER = '<IGNORE>'
WAEUP_KEY = 'waeup.kofa'
VIRT_JOBS_CONTAINER_NAME = 'jobs'
DOCLINK = 'http://kofa-doc.waeup.org/userdocs'

CREATED = 'created'
ADMITTED = 'admitted'
CLEARANCE = 'clearance started'
REQUESTED = 'clearance requested'
CLEARED = 'cleared'
PAID = 'school fee paid'
RETURNING = 'returning'
REGISTERED = 'courses registered'
VALIDATED = 'courses validated'
GRADUATED = 'graduated'
TRANSREQ = 'transcript requested'
TRANSVAL = 'transcript validated'
TRANSREL = 'transcript released'


#: A dict giving job status as tuple (<STRING>, <TRANSLATED_STRING>),
#: the latter for UI purposes.
JOB_STATUS_MAP = {
    zc.async.interfaces.NEW: ('new', _('new')),
    zc.async.interfaces.COMPLETED: ('completed', _('completed')),
    zc.async.interfaces.PENDING: ('pending', _('pending')),
    zc.async.interfaces.ACTIVE: ('active', _('active')),
    zc.async.interfaces.ASSIGNED: ('assigned', _('assigned')),
    zc.async.interfaces.CALLBACKS: ('callbacks', _('callbacks')),
    }

#default_rest_frontpage = u'' + codecs.open(os.path.join(
#        os.path.dirname(__file__), 'frontpage.rst'),
#        encoding='utf-8', mode='rb').read()

default_html_frontpage = u'' + codecs.open(os.path.join(
        os.path.dirname(__file__), 'frontpage.html'),
        encoding='utf-8', mode='rb').read()

def SimpleKofaVocabulary(*terms):
    """A well-buildt vocabulary provides terms with a value, token and
       title for each term
    """
    return SimpleVocabulary([
            SimpleTerm(value, value, title) for title, value in terms])

def academic_sessions():
    curr_year = datetime.now().year
    year_range = range(1970, curr_year + 2)
    return [('%s/%s' % (year,year+1), year) for year in year_range]

academic_sessions_vocab = SimpleKofaVocabulary(*academic_sessions())

registration_states_vocab = SimpleKofaVocabulary(
    (_('created'), CREATED),
    (_('admitted'), ADMITTED),
    (_('clearance started'), CLEARANCE),
    (_('clearance requested'), REQUESTED),
    (_('cleared'), CLEARED),
    (_('school fee paid'), PAID),
    (_('courses registered'), REGISTERED),
    (_('courses validated'), VALIDATED),
    (_('returning'), RETURNING),
    (_('graduated'), GRADUATED),
    (_('transcript requested'), TRANSREQ),
    (_('transcript validated'), TRANSVAL),
    (_('transcript released'), TRANSREL),
    )

class ContextualDictSourceFactoryBase(SmartBasicContextualSourceFactory):
    """A base for contextual sources based on KofaUtils dicts.

    To create a real source, you have to set the `DICT_NAME` attribute
    which should be the name of a dictionary in KofaUtils.
    """
    def getValues(self, context):
        utils = getUtility(IKofaUtils)
        sorted_items = sorted(getattr(utils, self.DICT_NAME).items(),
                              key=lambda item: item[1])
        return [item[0] for item in sorted_items]

    def getToken(self, context, value):
        return str(value)

    def getTitle(self, context, value):
        utils = getUtility(IKofaUtils)
        return getattr(utils, self.DICT_NAME)[value]

class SubjectSource(BasicSourceFactory):
    """A source for school subjects used in exam documentation.
    """
    def getValues(self):
        subjects_dict = getUtility(IKofaUtils).EXAM_SUBJECTS_DICT
        return sorted(subjects_dict.keys())

    def getTitle(self, value):
        subjects_dict = getUtility(IKofaUtils).EXAM_SUBJECTS_DICT
        return "%s:" % subjects_dict[value]

class GradeSource(BasicSourceFactory):
    """A source for exam grades.
    """
    def getValues(self):
        for entry in getUtility(IKofaUtils).EXAM_GRADES:
            yield entry[0]

    def getTitle(self, value):
        return dict(getUtility(IKofaUtils).EXAM_GRADES)[value]

class DisablePaymentGroupSource(ContextualDictSourceFactoryBase):
    """A source for filtering groups of students
    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'DISABLE_PAYMENT_GROUP_DICT'

class MonthSource(BasicSourceFactory):
    """A months source delivers all months of the year.
    """
    def getValues(self):
        months_dict = getUtility(IKofaUtils).MONTHS_DICT
        return sorted(months_dict.keys(), key=lambda x: int(x))

    def getToken(self, value):
        return value

    def getTitle(self, value):
        months_dict = getUtility(IKofaUtils).MONTHS_DICT
        return months_dict[value]

# Define a validation method for email addresses
class NotAnEmailAddress(schema.ValidationError):
    __doc__ = u"Invalid email address"

#: Regular expression to check email-address formats. As these can
#: become rather complex (nearly everything is allowed by RFCs), we only
#: forbid whitespaces, commas and dots following onto each other.
check_email = re.compile(
    r"^[^@\s,]+@[^@\.\s,]+(\.[^@\.\s,]+)*$").match

def validate_email(value):
    if not check_email(value):
        raise NotAnEmailAddress(value)
    return True

# Define a validation method for ids
class NotIdValue(schema.ValidationError):
    __doc__ = u"Invalid id"

#: Regular expressions to check id formats.
check_id = re.compile(r"^[a-zA-Z0-9_-]{2,11}$").match

def validate_id(value):
    if not check_id(value):
        raise NotIdValue(value)
    return True

# Define a validation method for HTML fields
class NotHTMLValue(schema.ValidationError):
    __doc__ = u"Style or script elements not allowed"

def validate_html(value):
    if '<style' in value or '<script' in value:
        raise NotHTMLValue(value)
    return True

# Define a validation method for international phone numbers
class InvalidPhoneNumber(schema.ValidationError):
    __doc__ = u"Invalid phone number"

# represent format +NNN-NNNN-NNNN
RE_INT_PHONE = re.compile(r"^\+?\d+\-\d+\-[\d\-]+$")

def validate_phone(value):
    if not RE_INT_PHONE.match(value):
        raise InvalidPhoneNumber(value)
    return True

class FatalCSVError(Exception):
    """Some row could not be processed.
    """
    pass

class DuplicationError(Exception):
    """An exception that can be raised when duplicates are found.

    When raising :exc:`DuplicationError` you can, beside the usual
    message, specify a list of objects which are duplicates. These
    values can be used by catching code to print something helpful or
    similar.
    """
    def __init__(self, msg, entries=[]):
        self.msg = msg
        self.entries = entries

    def __str__(self):
        return '%r' % self.msg

class RoleSource(BasicSourceFactory):
    """A source for site roles.
    """
    def getValues(self):
        # late import: in interfaces we should not import local modules
        from waeup.kofa.permissions import get_waeup_role_names
        return get_waeup_role_names()

    def getTitle(self, value):
        # late import: in interfaces we should not import local modules
        from waeup.kofa.permissions import get_all_roles
        roles = dict(get_all_roles())
        if value in roles.keys():
            title = roles[value].title
            if '.' in title:
                title = title.split('.', 2)[1]
        return title

class CaptchaSource(BasicSourceFactory):
    """A source for captchas.
    """
    def getValues(self):
        captchas = ['No captcha', 'Testing captcha', 'ReCaptcha']
        try:
            # we have to 'try' because IConfiguration can only handle
            # interfaces from w.k.interface.
            from waeup.kofa.browser.interfaces import ICaptchaManager
        except:
            return captchas
        return sorted(getUtility(ICaptchaManager).getAvailCaptchas().keys())

    def getTitle(self, value):
        return value

class IResultEntry(Interface):
    """A school grade entry.
    """

    subject = schema.Choice(
        title = _(u'Subject'),
        source = SubjectSource(),
        )

    grade = schema.Choice(
        title = _(u'Grade'),
        source = GradeSource(),
        )

class IResultEntryField(IObject):
    """A zope.schema-like field for usage in interfaces.

    Marker interface to distuingish result entries from ordinary
    object fields. Needed for registration of widgets.
    """

class IRefereeEntry(Interface):
    """A referee entry.
    """
    email_sent = Attribute('True if email has been sent')

    name = schema.TextLine(
        title = _(u'Name'),
        required = True,
        description = _(u'Name'),
        )

    email = schema.ASCIILine(
        title = _(u'Email Address'),
        default = None,
        required = True,
        constraint=validate_email,
        description = _(
            u'Email Address'),
        )

class IRefereeEntryField(IObject):
    """A zope.schema-like field for usage in interfaces.

    Marker interface to distuingish referee entries from ordinary
    object fields. Needed for registration of widgets.
    """

class IKofaUtils(Interface):
    """A collection of methods which are subject to customization.
    """

    PORTAL_LANGUAGE = Attribute("Dict of global language setting")
    MONTHS_DICT = Attribute("Dict of months of the year")
    PREFERRED_LANGUAGES_DICT = Attribute("Dict of preferred languages")
    EXAM_SUBJECTS_DICT = Attribute("Dict of examination subjects")
    EXAM_GRADES = Attribute("Dict of examination grades")
    INST_TYPES_DICT = Attribute("Dict if institution types")
    STUDY_MODES_DICT = Attribute("Dict of study modes")
    APP_CATS_DICT = Attribute("Dict of application categories")
    SEMESTER_DICT = Attribute("Dict of semesters or trimesters")
    SYSTEM_MAX_LOAD = Attribute("Dict of maximum system loads.")
    TEMP_PASSWORD_MINUTES = Attribute(
        "Temporary passwords and parents password validity period")

    def sendContactForm(
          from_name,from_addr,rcpt_name,rcpt_addr,
          from_username,usertype,portal,body,subject):
        """Send an email with data provided by forms.
        """

    def fullname(firstname,lastname,middlename):
        """Full name constructor.
        """

    def sendCredentials(user, password, url_info, msg):
        """Send credentials as email.

        Input is the applicant for which credentials are sent and the
        password.

        Returns True or False to indicate successful operation.
        """

    def genPassword(length, chars):
        """Generate a random password.
        """

class IKofaObject(Interface):
    """A Kofa object.

    This is merely a marker interface.
    """

class IUniversity(IKofaObject):
    """Representation of a university.
    """


class IKofaContainer(IKofaObject):
    """A container for Kofa objects.
    """

class IKofaContained(IKofaObject):
    """An item contained in an IKofaContainer.
    """

class ICSVExporter(Interface):
    """A CSV file exporter for objects.
    """
    fields = Attribute("""List of fieldnames in resulting CSV""")

    title = schema.TextLine(
        title = u'Title',
        description = u'Description to be displayed in selections.',
        )
    def mangle_value(value, name, obj):
        """Mangle `value` extracted from `obj` or suobjects thereof.

        This is called by export before actually writing to the result
        file.
        """

    def get_filtered(site, **kw):
        """Get datasets in `site` to be exported.

        The set of data is specified by keywords, which might be
        different for any implementaion of exporter.

        Returns an iterable.
        """

    def get_selected(site, selected):
        """Get datasets in `site` to be exported.

        The set of data is specified by a list of identifiers.

        Returns an iterable.
        """

    def export(iterable, filepath=None):
        """Export iterables as rows in a CSV file.

        If `filepath` is not given, a string with the data should be
        returned.

        What kind of iterables are acceptable depends on the specific
        exporter implementation.
        """

    def export_all(site, filepath=None):
        """Export all items in `site` as CSV file.

        if `filepath` is not given, a string with the data should be
        returned.
        """

    def export_filtered(site, filepath=None, **kw):
        """Export those items in `site` specified by `args` and `kw`.

        If `filepath` is not given, a string with the data should be
        returned.

        Which special keywords are supported is up to the respective
        exporter.
        """

    def export_selected(site, filepath=None, **kw):
        """Export items in `site` specified by a list of identifiers
        called `selected`.

        If `filepath` is not given, a string with the data should be
        returned.
        """

class IKofaExporter(Interface):
    """An exporter for objects.
    """
    def export(obj, filepath=None):
        """Export by pickling.

        Returns a file-like object containing a representation of `obj`.

        This is done using `pickle`. If `filepath` is ``None``, a
        `cStringIO` object is returned, that contains the saved data.
        """

class IKofaXMLExporter(Interface):
    """An XML exporter for objects.
    """
    def export(obj, filepath=None):
        """Export as XML.

        Returns an XML representation of `obj`.

        If `filepath` is ``None``, a StringIO` object is returned,
        that contains the transformed data.
        """

class IKofaXMLImporter(Interface):
    """An XML import for objects.
    """
    def doImport(filepath):
        """Create Python object from XML.

        Returns a Python object.
        """

class IBatchProcessor(Interface):
    """A batch processor that handles mass-operations.
    """
    name = schema.TextLine(
        title = _(u'Processor name')
        )

    def doImport(path, headerfields, mode='create', user='Unknown',
                 logger=None, ignore_empty=True):
        """Read data from ``path`` and update connected object.

        `headerfields` is a list of headerfields as read from the file
        to import.

        `mode` gives the import mode to use (``'create'``,
        ``'update'``, or ``'remove'``.

        `user` is a string describing the user performing the
        import. Normally fetched from current principal.

        `logger` is the logger to use during import.

        `ignore_emtpy` in update mode ignores empty fields if true.
        """

class IContactForm(IKofaObject):
    """A contact form.
    """

    email_from = schema.ASCIILine(
        title = _(u'Email Address:'),
        default = None,
        required = True,
        constraint=validate_email,
        )

    email_to = schema.ASCIILine(
        title = _(u'Email to:'),
        default = None,
        required = True,
        constraint=validate_email,
        )

    bcc_to = schema.Text(
        title = _(u'Bcc to:'),
        required = True,
        #readonly = True,
        )

    subject = schema.TextLine(
        title = _(u'Subject:'),
        required = True,)

    fullname = schema.TextLine(
        title = _(u'Full Name:'),
        required = True,)

    body = schema.Text(
        title = _(u'Text:'),
        required = True,)


class IKofaPrincipalInfo(IPrincipalInfo):
    """Infos about principals that are users of Kofa Kofa.
    """
    email = Attribute("The email address of a user")
    phone = Attribute("The phone number of a user")
    public_name = Attribute("The public name of a user")
    user_type = Attribute("The type of a user")


class IKofaPrincipal(IPrincipal):
    """A principle for Kofa Kofa.

    This interface extends zope.security.interfaces.IPrincipal and
    requires also an `id` and other attributes defined there.
    """

    email = schema.TextLine(
        title = _(u'Email Address'),
        description = u'',
        required=False,)

    phone = PhoneNumber(
        title = _(u'Phone'),
        description = u'',
        required=False,)

    public_name = schema.TextLine(
        title = _(u'Public Name'),
        required = False,)

    user_type = Attribute('The user type of the principal')

class IFailedLoginInfo(IKofaObject):
    """Info about failed logins.

    Timestamps are supposed to be stored as floats using time.time()
    or similar.
    """
    num = schema.Int(
        title = _(u'Number of failed logins'),
        description = _(u'Number of failed logins'),
        required = True,
        default = 0,
        )

    last = schema.Float(
        title = _(u'Timestamp'),
        description = _(u'Timestamp of last failed login or `None`'),
        required = False,
        default = None,
        )

    def as_tuple():
        """Get login info as tuple ``<NUM>, <TIMESTAMP>``.
        """

    def set_values(num=0, last=None):
        """Set number of failed logins and timestamp of last one.
        """

    def increase():
        """Increase the current number of failed logins and set timestamp.
        """

    def reset():
        """Set failed login counters back to zero.
        """


class IUserAccount(IKofaObject):
    """A user account.
    """

    failed_logins = Attribute('FailedLoginInfo for this account')

    name = schema.TextLine(
        title = _(u'User Id'),
        description = _(u'Login name of user'),
        required = True,)

    title = schema.TextLine(
        title = _(u'Full Name'),
        required = True,)

    public_name = schema.TextLine(
        title = _(u'Public Name'),
        description = _(u"Substitute for officer's real name "
                       "in student object histories "
                       "and in local roles tables."),
        required = False,)

    description = schema.Text(
        title = _(u'Description/Notice'),
        required = False,)

    email = schema.ASCIILine(
        title = _(u'Email Address'),
        default = None,
        required = True,
        constraint=validate_email,
        )

    phone = PhoneNumber(
        title = _(u'Phone'),
        default = None,
        required = False,
        )

    roles = schema.List(
        title = _(u'Portal Roles'),
        value_type = schema.Choice(source=RoleSource()),
        required = False,
        )

    suspended = schema.Bool(
        title = _(u'Account suspended'),
        description = _(u'If set, the account is immediately blocked.'),
        default = False,
        required = False,
        )


class IPasswordValidator(Interface):
    """A password validator utility.
    """

    def validate_password(password, password_repeat):
        """Validates a password by comparing it with
        control password and checking some other requirements.
        """

    def validate_secure_password(self, pw, pw_repeat):
        """ Validates a password by comparing it with
        control password and checks password strength by
        matching with the regular expression:

        ^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$

        ^              Start anchor
        (?=.*[A-Z])    Ensure password has one uppercase letters.
        (?=.*[0-9])    Ensure password has one digit.
        (?=.*[a-z])    Ensure password has one lowercase letter.
        .{8,}          Ensure password is of length 8.
        $              End anchor.
        """


class IUsersContainer(IKofaObject):
    """A container for officers.
    """

    def addUser(name, password, title=None, description=None):
        """Add a user.
        """

    def delUser(name):
        """Delete a user if it exists.
        """

class ILocalRolesAssignable(Interface):
    """The local roles assignable to an object.
    """
    def __call__():
        """Returns a list of dicts.

        Each dict contains a ``name`` referring to the role assignable
        for the specified object and a `title` to describe the range
        of users to which this role can be assigned.
        """

class IConfigurationContainer(IKofaObject):
    """A container for session configuration objects.
    """

    name = schema.TextLine(
        title = _(u'Name of University'),
        default = _(u'Sample University'),
        required = True,
        )

    acronym = schema.TextLine(
        title = _(u'Abbreviated Title of University'),
        default = u'WAeUP.Kofa',
        required = True,
        )

    frontpage = schema.Text(
        title = _(u'Content in HTML format'),
        required = False,
        default = default_html_frontpage,
        constraint=validate_html,
        )

    frontpage_dict = schema.Dict(
        title = u'Content as language dictionary with values in html format',
        required = False,
        default = {},
        )

    name_admin = schema.TextLine(
        title = _(u'Name of Administrator'),
        default = u'Administrator',
        required = True,
        )

    email_admin = schema.ASCIILine(
        title = _(u'Email Address of Administrator'),
        default = 'contact@waeup.org',
        required = True,
        #constraint=validate_email,
        )

    email_subject = schema.TextLine(
        title = _(u'Subject of Email to Administrator'),
        default = _(u'Kofa Contact'),
        required = True,
        )

    smtp_mailer = schema.Choice(
        title = _(u'SMTP mailer to use when sending mail'),
        vocabulary = 'Mail Delivery Names',
        default = 'No email service',
        required = True,
        )

    captcha = schema.Choice(
        title = _(u'Captcha used for public registration pages'),
        source = CaptchaSource(),
        default = u'No captcha',
        required = True,
        )

    carry_over = schema.Bool(
        title = _(u'Carry-over Course Registration'),
        default = False,
        )

    current_academic_session = schema.Choice(
        title = _(u'Current Academic Session'),
        description = _(u'Session for which score editing is allowed'),
        source = academic_sessions_vocab,
        default = None,
        required = False,
        readonly = False,
        )

    next_matric_integer = schema.Int(
        title = _(u'Next Matriculation Number Integer'),
        description = _(u'Integer used for constructing the next '
                         'matriculation number'),
        default = 0,
        readonly = False,
        required = False,
        )

    next_matric_integer_2 = schema.Int(
        title = _(u'Next Matriculation Number Integer 2'),
        description = _(u'2nd integer used for constructing the next '
                         'matriculation number'),
        default = 0,
        readonly = False,
        required = False,
        )

    next_matric_integer_3 = schema.Int(
        title = _(u'Next Matriculation Number Integer 3'),
        description = _(u'3rd integer used for constructing the next '
                         'matriculation number'),
        default = 0,
        readonly = False,
        required = False,
        )

    next_matric_integer_4 = schema.Int(
        title = _(u'Next Matriculation Number Integer 4'),
        description = _(u'4th integer used for constructing the next '
                         'matriculation number'),
        default = 0,
        readonly = False,
        required = False,
        )

    export_disabled_message = schema.Text(
        title = _(u'Export-disabled message'),
        description = _(u'Message which will show up if an officer tries '
                         'to export data. All exporters are automatcally '
                         'disabled if this field is set.'),
        required = False,
        )

    maintmode_enabled_by = schema.TextLine(
        title = _(u'Maintenance Mode enabled by'),
        default = None,
        required = False,
        )

    def addSessionConfiguration(sessionconfiguration):
        """Add a session configuration object.
        """

class ISessionConfiguration(IKofaObject):
    """A session configuration object.
    """

    academic_session = schema.Choice(
        title = _(u'Academic Session'),
        source = academic_sessions_vocab,
        default = None,
        required = True,
        readonly = True,
        )

    clearance_enabled = schema.Bool(
        title = _(u'Clearance enabled'),
        default = False,
        )

    payment_disabled = schema.List(
        title = _(u'Payment disabled'),
        value_type = schema.Choice(
            source = DisablePaymentGroupSource(),
            ),
        required = False,
        defaultFactory=list,
        )

    coursereg_deadline = schema.Datetime(
        title = _(u'Course Reg. Deadline'),
        required = False,
        description = _('Example: ') + u'2011-12-31 23:59:59+01:00',
        )

    clearance_fee = schema.Float(
        title = _(u'Acceptance Fee'),
        default = 0.0,
        required = False,
        )

    booking_fee = schema.Float(
        title = _(u'Bed Booking Fee'),
        default = 0.0,
        required = False,
        )

    maint_fee = schema.Float(
        title = _(u'Rent (fallback)'),
        default = 0.0,
        required = False,
        )

    late_registration_fee = schema.Float(
        title = _(u'Late Course Reg. Fee'),
        default = 0.0,
        required = False,
        )

    transcript_fee = schema.Float(
        title = _(u'Transcript Fee'),
        default = 0.0,
        required = False,
        )

    transfer_fee = schema.Float(
        title = _(u'Transfer Fee'),
        default = 0.0,
        required = False,
        )

    def getSessionString():
        """Return the session string from the vocabulary.
        """


class ISessionConfigurationAdd(ISessionConfiguration):
    """A session configuration object in add mode.
    """

    academic_session = schema.Choice(
        title = _(u'Academic Session'),
        source = academic_sessions_vocab,
        default = None,
        required = True,
        readonly = False,
        )

ISessionConfigurationAdd['academic_session'].order =  ISessionConfiguration[
    'academic_session'].order

class IDataCenter(IKofaObject):
    """A data center.

    A data center manages files (uploads, downloads, etc.).

    Beside providing the bare paths needed to keep files, it also
    provides some helpers to put results of batch processing into
    well-defined final locations (with well-defined filenames).

    The main use-case is managing of site-related files, i.e. files
    for import, export etc.

    DataCenters are _not_ meant as storages for object-specific files
    like passport photographs and similar.

    It is up to the datacenter implementation how to organize data
    (paths) inside its storage path.
    """
    storage = schema.Bytes(
        title = u'Path to directory where everything is kept.'
        )

    deleted_path = schema.Bytes(
        title = u'Path for deleted student data.'
        )

    graduated_path = schema.Bytes(
        title = u'Path for deleted graduated student data.'
        )

    def getPendingFiles(sort='name'):
        """Get a list of files stored in `storage` sorted by basename.
        """

    def getFinishedFiles():
        """Get a list of files stored in `finished` subfolder of `storage`.
        """

    def setStoragePath(path, move=False, overwrite=False):
        """Set the path where to store files.

        If `move` is True, move over files from the current location
        to the new one.

        If `overwrite` is also True, overwrite any already existing
        files of same name in target location.

        Triggers a DataCenterStorageMovedEvent.
        """

    def distProcessedFiles(successful, source_path, finished_file,
                           pending_file, mode='create', move_orig=True):
        """Distribute processed files over final locations.
        """


class IDataCenterFile(Interface):
    """A data center file.
    """

    name = schema.TextLine(
        title = u'Filename')

    size = schema.TextLine(
        title = u'Human readable file size')

    uploaddate = schema.TextLine(
        title = u'Human readable upload datetime')

    lines = schema.Int(
        title = u'Number of lines in file')

    def getDate():
        """Get creation timestamp from file in human readable form.
        """

    def getSize():
        """Get human readable size of file.
        """

    def getLinesNumber():
        """Get number of lines of file.
        """

class IDataCenterStorageMovedEvent(IObjectEvent):
    """Emitted, when the storage of a datacenter changes.
    """

class IObjectUpgradeEvent(IObjectEvent):
    """Can be fired, when an object shall be upgraded.
    """

class ILocalRoleSetEvent(IObjectEvent):
    """A local role was granted/revoked for a principal on an object.
    """
    role_id = Attribute(
        "The role id that was set.")
    principal_id = Attribute(
        "The principal id for which the role was granted/revoked.")
    granted = Attribute(
        "Boolean. If false, then the role was revoked.")

class IQueryResultItem(Interface):
    """An item in a search result.
    """
    url = schema.TextLine(
        title = u'URL that links to the found item')
    title = schema.TextLine(
        title = u'Title displayed in search results.')
    description = schema.Text(
        title = u'Longer description of the item found.')

class IKofaPluggable(Interface):
    """A component that might be plugged into a Kofa Kofa app.

    Components implementing this interface are referred to as
    'plugins'. They are normally called when a new
    :class:`waeup.kofa.app.University` instance is created.

    Plugins can setup and update parts of the central site without the
    site object (normally a :class:`waeup.kofa.app.University` object)
    needing to know about that parts. The site simply collects all
    available plugins, calls them and the plugins care for their
    respective subarea like the applicants area or the datacenter
    area.

    Currently we have no mechanism to define an order of plugins. A
    plugin should therefore make no assumptions about the state of the
    site or other plugins being run before and instead do appropriate
    checks if necessary.

    Updates can be triggered for instance by the respective form in
    the site configuration. You normally do updates when the
    underlying software changed.
    """
    def setup(site, name, logger):
        """Create an instance of the plugin.

        The method is meant to be called by the central app (site)
        when it is created.

        `site`:
           The site that requests a setup.

        `name`:
           The name under which the plugin was registered (utility name).

        `logger`:
           A standard Python logger for the plugins use.
        """

    def update(site, name, logger):
        """Method to update an already existing plugin.

        This might be called by a site when something serious
        changes. It is a poor-man replacement for Zope generations
        (but probably more comprehensive and better understandable).

        `site`:
           The site that requests an update.

        `name`:
           The name under which the plugin was registered (utility name).

        `logger`:
           A standard Python logger for the plugins use.
        """

class IAuthPluginUtility(Interface):
    """A component that cares for authentication setup at site creation.

    Utilities providing this interface are looked up when a Pluggable
    Authentication Utility (PAU) for any
    :class:`waeup.kofa.app.University` instance is created and put
    into ZODB.

    The setup-code then calls the `register` method of the utility and
    expects a modified (or unmodified) version of the PAU back.

    This allows to define any authentication setup modifications by
    submodules or third-party modules/packages.
    """

    def register(pau):
        """Register any plugins wanted to be in the PAU.
        """

    def unregister(pau):
        """Unregister any plugins not wanted to be in the PAU.
        """

class IObjectConverter(Interface):
    """Object converters are available as simple adapters, adapting
       interfaces (not regular instances).

    """

    def fromStringDict(self, data_dict, context, form_fields=None):
        """Convert values in `data_dict`.

        Converts data in `data_dict` into real values based on
        `context` and `form_fields`.

        `data_dict` is a mapping (dict) from field names to values
        represented as strings.

        The fields (keys) to convert can be given in optional
        `form_fields`. If given, form_fields should be an instance of
        :class:`zope.formlib.form.Fields`. Suitable instances are for
        example created by :class:`grok.AutoFields`.

        If no `form_fields` are given, a default is computed from the
        associated interface.

        The `context` can be an existing object (implementing the
        associated interface) or a factory name. If it is a string, we
        try to create an object using
        :func:`zope.component.createObject`.

        Returns a tuple ``(<FIELD_ERRORS>, <INVARIANT_ERRORS>,
        <DATA_DICT>)`` where

        ``<FIELD_ERRORS>``
           is a list of tuples ``(<FIELD_NAME>, <ERROR>)`` for each
           error that happened when validating the input data in
           `data_dict`

        ``<INVARIANT_ERRORS>``
           is a list of invariant errors concerning several fields

        ``<DATA_DICT>``
           is a dict with the values from input dict converted.

        If errors happen, i.e. the error lists are not empty, always
        an empty ``<DATA_DICT>`` is returned.

        If ``<DATA_DICT>`` is non-empty, there were no errors.
        """

class IFieldConverter(Interface):
    def request_data(name, value, schema_field, prefix='', mode='create'):
        """Create a dict with key-value mapping as created by a request.

        `name` and `value` are expected to be parsed from CSV or a
        similar input and represent an attribute to be set to a
        representation of value.

        `mode` gives the mode of import.

        :meth:`update_request_data` is then requested to turn this
        name and value into vars as they would be sent by a regular
        form submit. This means we do not create the real values to be
        set but we only define the values that would be sent in a
        browser request to request the creation of those values.

        The returned dict should contain names and values of a faked
        browser request for the given `schema_field`.

        Field converters are normally registered as adapters to some
        specific zope.schema field.
        """

class IObjectHistory(Interface):

    messages = schema.List(
        title = u'List of messages stored',
        required = True,
        )

    def addMessage(message):
        """Add a message.
        """

class IKofaWorkflowInfo(IWorkflowInfo):
    """A :class:`hurry.workflow.workflow.WorkflowInfo` with additional
       methods for convenience.
    """
    def getManualTransitions():
        """Get allowed manual transitions.

        Get a sorted list of tuples containing the `transition_id` and
        `title` of each allowed transition.
        """

class ISiteLoggers(Interface):

    loggers = Attribute("A list or generator of registered KofaLoggers")

    def register(name, filename=None, site=None, **options):
        """Register a logger `name` which logs to `filename`.

        If `filename` is not given, logfile will be `name` with
        ``.log`` as filename extension.
        """

    def unregister(name):
        """Unregister a once registered logger.
        """

class ILogger(Interface):
    """A logger cares for setup, update and restarting of a Python logger.
    """

    logger = Attribute("""A :class:`logging.Logger` instance""")


    def __init__(name, filename=None, site=None, **options):
        """Create a Kofa logger instance.
        """

    def setup():
        """Create a Python :class:`logging.Logger` instance.

        The created logger is based on the params given by constructor.
        """

    def update(**options):
        """Update the logger.

        Updates the logger respecting modified `options` and changed
        paths.
        """

class ILoggerCollector(Interface):

    def getLoggers(site):
        """Return all loggers registered for `site`.
        """

    def registerLogger(site, logging_component):
        """Register a logging component residing in `site`.
        """

    def unregisterLogger(site, logging_component):
        """Unregister a logger.
        """

#
# External File Storage and relatives
#
class IFileStoreNameChooser(INameChooser):
    """See zope.container.interfaces.INameChooser for base methods.
    """
    def checkName(name, attr=None):
        """Check whether an object name is valid.

        Raises a user error if the name is not valid.
        """

    def chooseName(name, attr=None):
        """Choose a unique valid file id for the object.

        The given name may be taken into account when choosing the
        name (file id).

        chooseName is expected to always choose a valid file id (that
        would pass the checkName test) and never raise an error.

        If `attr` is not ``None`` it might been taken into account as
        well when generating the file id. Usual behaviour is to
        interpret `attr` as a hint for what type of file for a given
        context should be stored if there are several types
        possible. For instance for a certain student some file could
        be the connected passport photograph or some certificate scan
        or whatever. Each of them has to be stored in a different
        location so setting `attr` to a sensible value should give
        different file ids returned.
        """

class IExtFileStore(IFileRetrieval):
    """A file storage that stores files in filesystem (not as blobs).
    """
    root = schema.TextLine(
        title = u'Root path of file store.',
        )

    def getFile(file_id):
        """Get raw file data stored under file with `file_id`.

        Returns a file descriptor open for reading or ``None`` if the
        file cannot be found.
        """

    def getFileByContext(context, attr=None):
        """Get raw file data stored for the given context.

        Returns a file descriptor open for reading or ``None`` if no
        such file can be found.

        Both, `context` and `attr` might be used to find (`context`)
        and feed (`attr`) an appropriate file name chooser.

        This is a convenience method.
        """

    def deleteFile(file_id):
        """Delete file stored under `file_id`.

        Remove file from filestore so, that it is not available
        anymore on next call to getFile for the same file_id.

        Should not complain if no such file exists.
        """

    def deleteFileByContext(context, attr=None):
        """Delete file for given `context` and `attr`.

        Both, `context` and `attr` might be used to find (`context`)
        and feed (`attr`) an appropriate file name chooser.

        This is a convenience method.
        """

    def createFile(filename, f):
        """Create file given by f with filename `filename`

        Returns a hurry.file.File-based object.
        """

class IFileStoreHandler(Interface):
    """Filestore handlers handle specific files for file stores.

    If a file to store/get provides a specific filename, a file store
    looks up special handlers for that type of file.

    """
    def pathFromFileID(store, root, filename):
        """Turn file id into path to store.

        Returned path should be absolute.
        """

    def createFile(store, root, filename, file_id, file):
        """Return some hurry.file based on `store` and `file_id`.

        Some kind of callback method called by file stores to create
        file objects from file_id.

        Returns a tuple ``(raw_file, path, file_like_obj)`` where the
        ``file_like_obj`` should be a HurryFile, a KofaImageFile or
        similar. ``raw_file`` is the (maybe changed) input file and
        ``path`` the relative internal path to store the file at.

        Please make sure the ``raw_file`` is opened for reading and
        the file descriptor set at position 0 when returned.

        This method also gets the raw input file object that is about
        to be stored and is expected to raise any exceptions if some
        kind of validation or similar fails.
        """

class IPDF(Interface):
    """A PDF representation of some context.
    """

    def __call__(view=None, note=None):
        """Create a bytestream representing a PDF from context.

        If `view` is passed in additional infos might be rendered into
        the document.

        `note` is optional HTML rendered at bottom of the created
        PDF. Please consider the limited reportlab support for HTML,
        but using font-tags and friends you certainly can get the
        desired look.
        """

class IMailService(Interface):
    """A mail service.
    """

    def __call__():
        """Get the default mail delivery.
        """


class IDataCenterConfig(Interface):
    path = Path(
        title = u'Path',
        description = u"Directory where the datacenter should store "
                      u"files by default (adjustable in web UI).",
        required = True,
        )

#
# Asynchronous job handling and related
#
class IJobManager(IKofaObject):
    """A manager for asynchronous running jobs (tasks).
    """
    def put(job, site=None):
        """Put a job into task queue.

        If no `site` is given, queue job in context of current local
        site.

        Returns a job_id to identify the put job. This job_id is
        needed for further references to the job.
        """

    def jobs(site=None):
        """Get an iterable of jobs stored.
        """

    def get(job_id, site=None):
        """Get the job with id `job_id`.

        For the `site` parameter see :meth:`put`.
        """

    def remove(job_id, site=None):
        """Remove job with `job_id` from stored jobs.
        """

    def start_test_job(site=None):
        """Start a test job.
        """

class IProgressable(Interface):
    """A component that can indicate its progress status.
    """
    percent = schema.Float(
        title = u'Percent of job done already.',
        )

class IJobContainer(IContainer):
    """A job container contains IJob objects.
    """

class IExportJob(zc.async.interfaces.IJob):
    def __init__(site, exporter_name):
        pass

    finished = schema.Bool(
        title = u'`True` if the job finished.`',
        default = False,
        )

    failed = schema.Bool(
        title = u"`True` iff the job finished and didn't provide a file.",
        default = None,
        )

class IExportJobContainer(IKofaObject):
    """A component that contains (maybe virtually) export jobs.
    """
    def start_export_job(exporter_name, user_id, *args, **kwargs):
        """Start asynchronous export job.

        `exporter_name` is the name of an exporter utility to be used.

        `user_id` is the ID of the user that triggers the export.

        `args` positional arguments passed to the export job created.

        `kwargs` keyword arguments passed to the export job.

        The job_id is stored along with exporter name and user id in a
        persistent list.

        Returns the job ID of the job started.
        """

    def get_running_export_jobs(user_id=None):
        """Get export jobs for user with `user_id` as list of tuples.

        Each tuples holds ``<job_id>, <exporter_name>, <user_id>`` in
        that order. The ``<exporter_name>`` is the utility name of the
        used exporter.

        If `user_id` is ``None``, all running jobs are returned.
        """

    def get_export_jobs_status(user_id=None):
        """Get running/completed export jobs for `user_id` as list of tuples.

        Each tuple holds ``<raw status>, <status translated>,
        <exporter title>`` in that order, where ``<status
        translated>`` and ``<exporter title>`` are translated strings
        representing the status of the job and the human readable
        title of the exporter used.
        """

    def delete_export_entry(entry):
        """Delete the export denoted by `entry`.

        Removes `entry` from the local `running_exports` list and also
        removes the regarding job via the local job manager.

        `entry` is a tuple ``(<job id>, <exporter name>, <user id>)``
        as created by :meth:`start_export_job` or returned by
        :meth:`get_running_export_jobs`.
        """

    def entry_from_job_id(job_id):
        """Get entry tuple for `job_id`.

        Returns ``None`` if no such entry can be found.
        """

class IExportContainerFinder(Interface):
    """A finder for the central export container.
    """
    def __call__():
        """Return the currently used global or site-wide IExportContainer.
        """

class IFilteredQuery(IKofaObject):
    """A query for objects.
    """

    defaults = schema.Dict(
        title = u'Default Parameters',
        required = True,
        )

    def __init__(**parameters):
        """Instantiate a filtered query by passing in parameters.
        """

    def query():
        """Get an iterable of objects denoted by the set parameters.

        The search should be applied to objects inside current
        site. It's the caller's duty to set the correct site before.

        Result can be any iterable like a catalog result set, a list,
        or similar.
        """

class IFilteredCatalogQuery(IFilteredQuery):
    """A catalog-based query for objects.
    """

    cat_name = schema.TextLine(
        title = u'Registered name of the catalog to search.',
        required = True,
        )

    def query_catalog(catalog):
        """Query catalog with the parameters passed to constructor.
        """
