## $Id: utils.py 17211 2022-12-09 10:03:28Z henrik $
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
"""General helper utilities for Kofa.
"""
import grok
import psutil
import string
import pytz
import decimal
from copy import deepcopy
from random import SystemRandom as r
from zope.i18n import translate
from waeup.kofa.interfaces import IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.smtp import send_mail as send_mail_internally
from waeup.kofa.utils.helpers import get_sorted_preferred
from waeup.kofa.utils.degrees import DEGREES_DICT


def send_mail(from_name, from_addr,
              rcpt_name, rcpt_addr,
              subject, body, config,
              cc=None, bcc=None):
    """Wrapper for the real SMTP functionality in :mod:`waeup.kofa.smtp`.

    Merely here to stay compatible with lots of calls to this place.
    """
    mail_id = send_mail_internally(
        from_name, from_addr, rcpt_name, rcpt_addr,
        subject, body, config, cc, bcc)
    return True


#: A list of phone prefixes (order num, country, prefix).
#: Items with same order num will be sorted alphabetically.
#: The lower the order num, the higher the precedence.
INT_PHONE_PREFIXES = [
    (99, _('Germany'), '49'),
    (1, _('Nigeria'), '234'),
    (99, _('U.S.'), '1'),
    ]


def sorted_phone_prefixes(data=INT_PHONE_PREFIXES, request=None):
    """Sorted tuples of phone prefixes.

    Ordered as shown above and formatted for use in select boxes.

    If request is given, we'll try to translate all country names in
    order to sort alphabetically correctly.

    XXX: This is a function (and not a constant) as different
    languages might give different orders. This is not tested yet.

    XXX: If we really want to use alphabetic ordering here, we might
    think about caching results of translations.
    """
    if request is not None:
        data = [
            (x, translate(y, context=request), z)
            for x, y, z in data]
    return tuple([
        ('%s (+%s)' % (x[1], x[2]), '+%s' % x[2])
        for x in sorted(data)
        ])


class KofaUtils(grok.GlobalUtility):
    """A collection of parameters and methods subject to customization.
    """
    grok.implements(IKofaUtils)

    #: This the only place where we define the portal language
    #: which is used for the translation of system messages
    #: (e.g. object histories) pdf slips.
    PORTAL_LANGUAGE = 'en'

    DEGREES_DICT = DEGREES_DICT

    PREFERRED_LANGUAGES_DICT = {
        'en': (1, u'English'),
        'fr': (2, u'Fran&ccedil;ais'),
        'de': (3, u'Deutsch'),
        'ha': (4, u'Hausa'),
        'yo': (5, u'Yoruba'),
        'ig': (6, u'Igbo'),
        }

    MONTHS_DICT = {
        '1': _('January'),
        '2': _('February'),
        '3': _('March'),
        '4': _('April'),
        '5': _('May'),
        '6': _('June'),
        '7': _('July'),
        '8': _('August'),
        '9': _('September'),
        '10': _('October'),
        '11': _('November'),
        '12': _('December'),
        }

    #: A function to return
    @classmethod
    def sorted_phone_prefixes(cls, data=INT_PHONE_PREFIXES, request=None):
        return sorted_phone_prefixes(data, request)

    EXAM_SUBJECTS_DICT = {
        'math': 'Mathematics',
        'computer_science': 'Computer Science',
        }

    #: Exam grades. The tuple is sorted as it should be displayed in
    #: select boxes.
    EXAM_GRADES = (
        ('A', 'Best'),
        ('B', 'Better'),
        ('C', 'Good'),
        )

    INST_TYPES_DICT = {
        'none': '',
        'faculty': 'Faculty of',
        'department': 'Department of',
        'school': 'School of',
        'office': 'Office for',
        'centre': 'Centre for',
        'centre_of': 'Centre of',
        'institute': 'Institute of',
        'school_for': 'School for',
        'college': 'College of',
        'directorate': 'Directorate of',
        }

    STUDY_MODES_DICT = {
        'transfer': 'Transfer',
        'transferred': 'Transferred',
        'ug_ft': 'Undergraduate Full-Time',
        'ug_pt': 'Undergraduate Part-Time',
        'pg_ft': 'Postgraduate Full-Time',
        'pg_pt': 'Postgraduate Part-Time',
        }

    DISABLE_PAYMENT_GROUP_DICT = {
        'sf_all': 'School Fee - All Students',
        }

    APP_CATS_DICT = {
        'basic': 'Basic Application',
        'no': 'no application',
        'pg': 'Postgraduate',
        'sandwich': 'Sandwich',
        'cest': 'Part-Time, Diploma, Certificate'
        }

    SEMESTER_DICT = {
        1: '1st Semester',
        2: '2nd Semester',
        3: 'Combined',
        4: '1st Term',
        5: '2nd Term',
        6: '3rd Term',
        9: 'N/A',
        11: 'Module I',
        12: 'Module II',
        13: 'Module III',
        }

    COURSE_CATEGORY_DICT = {
        }

    SPECIAL_HANDLING_DICT = {
        'regular': 'Regular Hostel',
        'blocked': 'Blocked Hostel',
        'pg': 'Postgraduate Hostel'
        }

    SPECIAL_APP_DICT = {
        'transcript': 'Transcript Fee Payment',
        'clearance': 'Acceptance Fee',
        }

    PAYMENT_CATEGORIES = {
        'schoolfee': 'School Fee',
        'clearance': 'Acceptance Fee',
        'bed_allocation': 'Bed Allocation Fee',
        'hostel_maintenance': 'Hostel Maintenance Fee',
        'transfer': 'Transfer Fee',
        'gown': 'Gown Hire Fee',
        'application': 'Application Fee',
        'app_balance': 'Application Fee Balance',
        'transcript': 'Transcript Fee',
        'late_registration': 'Late Course Registration Fee',
        'combi': 'Combi Payment',
        'donation': 'Donation',
        }

    #: If PAYMENT_OPTIONS is empty, payment option fields won't show up.
    PAYMENT_OPTIONS = {
        #'credit_card': 'Credit Card',
        #'debit_card': 'Debit Card',
        }

    def selectable_payment_categories(self, student):
        return self.PAYMENT_CATEGORIES

    def selectable_payment_options(self, student):
        return self.PAYMENT_OPTIONS

    PREVIOUS_PAYMENT_CATEGORIES = deepcopy(PAYMENT_CATEGORIES)

    REPORTABLE_PAYMENT_CATEGORIES = {
        'schoolfee': 'School Fee',
        'clearance': 'Acceptance Fee',
        'hostel_maintenance': 'Hostel Maintenance Fee',
        'gown': 'Gown Hire Fee',
        }

    BALANCE_PAYMENT_CATEGORIES = {
        'schoolfee': 'School Fee',
        }

    APPLICANT_BALANCE_PAYMENT_CATEGORIES = {
        'donation': 'Donation',
        }

    COMBI_PAYMENT_CATEGORIES = {
        'gown': 'Gown Hire Fee',
        'transcript': 'Transcript Fee',
        'late_registration': 'Late Course Registration Fee',
        }

    MODE_GROUPS = {
        'All': ('all',),
        'Undergraduate Full-Time': ('ug_ft',),
        'Undergraduate Part-Time': ('ug_pt',),
        'Postgraduate Full-Time': ('pg_ft',),
        'Postgraduate Part-Time': ('pg_pt',),
        }

    VERDICTS_DICT = {
        '0': _('(not yet)'),
        'A': 'Successful student',
        'B': 'Student with carryover courses',
        'C': 'Student on probation',
        }

    #: Set positive number for allowed max, negative for required min
    #: avail.
    #: Use integer for bytes value, float for percent
    #: value. `cpu-load`, of course, accepts float values only.
    #: `swap-mem` = Swap Memory, `virt-mem` = Virtual Memory,
    #: `cpu-load` = CPU load in percent.
    SYSTEM_MAX_LOAD = {
        'swap-mem': None,
        'virt-mem': None,
        'cpu-load': 100.0,
        }

    #: Maximum number of files listed in `finished` subfolder
    MAX_FILES = 100

    #: Maximum size in Bytes of passport images in the applicants and
    #: students section
    MAX_PASSPORT_SIZE = 50 * 1024

    #: Temporary passwords and parents password validity period
    TEMP_PASSWORD_MINUTES = 10

    def sendContactForm(self, from_name, from_addr, rcpt_name, rcpt_addr,
                        from_username, usertype, portal, body, subject,
                        bcc_to=None):
        """Send an email with data provided by forms.
        """
        config = grok.getSite()['configuration']
        text = _(u"""${e}

---
${a} (id: ${b})
${d}
""")
        text = _(text, mapping={
            'a': from_name,
            'b': from_username,
            'c': usertype,
            'd': portal,
            'e': body})
        body = translate(text, 'waeup.kofa',
            target_language=self.PORTAL_LANGUAGE)
        if not (from_addr and rcpt_addr):
            return False
        return send_mail(
            from_name, from_addr, rcpt_name, rcpt_addr,
            subject, body, config, None, bcc_to)

    def getUsers(self):
        users = sorted(
            grok.getSite()['users'].items(), key=lambda x: x[1].title)
        for key, val in users:
            yield(dict(name=key, val="%s (%s)" % (val.title, val.name)))

    @property
    def tzinfo(self):
        """Time zone of the university.
        """
        # For Nigeria: pytz.timezone('Africa/Lagos')
        # For Germany: pytz.timezone('Europe/Berlin')
        return pytz.utc

    def fullname(self, firstname, lastname, middlename=None):
        """Construct fullname.
        """
        # We do not necessarily have the middlename attribute
        if middlename:
            name = '%s %s %s' % (firstname, middlename, lastname)
        else:
            name = '%s %s' % (firstname, lastname)
        if '<' in name:
            return 'XXX'
        return string.capwords(
            name.replace('-', ' - ')).replace(' - ', '-')

    def genPassword(self, length=4, chars=string.letters + string.digits):
        """Generate a random password.
        """
        return ''.join([
            r().choice(string.uppercase) +
            r().choice(string.lowercase) +
            r().choice(string.digits) for i in range(length)])

    def sendCredentials(self, user, password=None, url_info=None, msg=None):
        """Send credentials as email. Input is the user for which credentials
        are sent and the password. Method returns True or False to indicate
        successful operation.
        """
        subject = _('Your Kofa credentials')
        text = _(u"""Dear ${a},

${b}
Student Registration and Information Portal of
${c}.

Your user name: ${d}
Your password: ${e}
${f}

Please remember your user name and keep
your password secret!

Please also note that passwords are case-sensitive.

Regards
""")
        config = grok.getSite()['configuration']
        from_name = config.name_admin
        from_addr = config.email_admin
        rcpt_name = user.title
        rcpt_addr = user.email
        text = _(text, mapping={
            'a': rcpt_name,
            'b': msg,
            'c': config.name,
            'd': user.name,
            'e': password,
            'f': url_info})

        body = translate(text, 'waeup.kofa',
            target_language=self.PORTAL_LANGUAGE)
        return send_mail(
            from_name, from_addr, rcpt_name, rcpt_addr,
            subject, body, config)

    def informNewStudent(self, user, pw, login_url, rpw_url):
        """Inform student that a new student account has been created.
        """
        subject = _('Your new Kofa student account')
        text = _(u"""Dear ${a},

Your student record of the Student Registration and Information Portal of
${b} has been created for you.

Your user name: ${c}
Your password: ${d}
Login: ${e}

Or request a new secure password here: ${f}

Regards
""")
        config = grok.getSite()['configuration']
        from_name = config.name_admin
        from_addr = config.email_admin
        rcpt_name = user.title
        rcpt_addr = user.email

        text = _(text, mapping={
            'a': rcpt_name,
            'b': config.name,
            'c': user.name,
            'd': pw,
            'e': login_url,
            'f': rpw_url
            })
        body = translate(text, 'waeup.kofa',
            target_language=self.PORTAL_LANGUAGE)
        return send_mail(
            from_name, from_addr, rcpt_name, rcpt_addr,
            subject, body, config)


    def informApplicant(self, applicant):
        """Inform applicant that the application form was successfully
        submitted.
        """
        if not getattr(applicant.__parent__, 'send_email', False):
            return
        subject = 'Your application form was successfully submitted'
        text = _(u"""Dear ${a},

Your application ${b} has been successfully submitted to ${c}.

Regards
""")
        config = grok.getSite()['configuration']
        from_name = config.name_admin
        from_addr = config.email_admin
        rcpt_name = applicant.display_fullname
        rcpt_addr = applicant.email
        session = '%s/%s' % (
            applicant.__parent__.year, applicant.__parent__.year+1)
        text = _(text, mapping={
            'a': rcpt_name,
            'b': applicant.applicant_id,
            'c': config.name,
            })
        body = translate(text, 'waeup.kofa',
            target_language=self.PORTAL_LANGUAGE)
        return send_mail(
            from_name, from_addr, rcpt_name, rcpt_addr,
            subject, body, config)

    def inviteReferee(self, referee, applicant, url_info=None):
        """Send invitation email to referee.
        """
        config = grok.getSite()['configuration']
        subject = 'Request for referee report from %s' % config.name
        text = _(u"""Dear ${a},

The candidate with Id ${b} and name ${c} applied to
the ${d} to study ${e} for the ${f} session.
The candidate has listed you as referee. You are, therefore, required to,
kindly, provide your referral remarks on or before ${g}. Please use the
following form:

${h}

Thank You

The Secretary
School of Postgraduate Studies
${d}
""")
        from_name = config.name_admin
        from_addr = config.email_admin
        rcpt_name = referee.name
        rcpt_addr = referee.email
        session = '%s/%s' % (
            applicant.__parent__.year, applicant.__parent__.year+1)
        text = _(text, mapping={
            'a': rcpt_name,
            'b': applicant.applicant_id,
            'c': applicant.display_fullname,
            'd': config.name,
            'e': applicant.course1.title,
            'f': session,
            'g': applicant.__parent__.enddate,
            'h': url_info,
            })

        body = translate(text, 'waeup.kofa',
            target_language=self.PORTAL_LANGUAGE)
        return send_mail(
            from_name, from_addr, rcpt_name, rcpt_addr,
            subject, body, config)

    def getPaymentItem(self, payment):
        """Return payment item. This method can be used to customize the
        `display_item` property attribute, e.g. in order to hide bed coordinates
        if maintenance fee is not paid.
        """
        return payment.p_item

    def expensive_actions_allowed(self, type=None, request=None):
        """Tell, whether expensive actions are currently allowed.
        Check system load/health (or other external circumstances) and
        locally set values to see, whether expensive actions should be
        allowed (`True`) or better avoided (`False`).
        Use this to allow or forbid exports, report generations, or
        similar actions.
        """
        max_values = self.SYSTEM_MAX_LOAD
        for (key, func) in (
            ('swap-mem', psutil.swap_memory),
            ('virt-mem', psutil.virtual_memory),
            ):
            max_val = max_values.get(key, None)
            if max_val is None:
                continue
            mem_val = func()
            if isinstance(max_val, float):
                # percents
                if max_val < 0.0:
                    max_val = 100.0 + max_val
                if mem_val.percent > max_val:
                    return False
            else:
                # number of bytes
                if max_val < 0:
                    max_val = mem_val.total + max_val
                if mem_val.used > max_val:
                    return False
        return True

    def export_disabled_message(self):
        export_disabled_message = grok.getSite()[
            'configuration'].export_disabled_message
        if export_disabled_message:
            return export_disabled_message
        return None

    def format_float(self, value, prec):
        # >>> 4.6 * 100
        # 459.99999999999994
        value = decimal.Decimal(str(value))
        # cut floating point value
        value = int(pow(10, prec)*value) / (1.0*pow(10, prec))
        return '{:{width}.{prec}f}'.format(value, width=0, prec=prec)
