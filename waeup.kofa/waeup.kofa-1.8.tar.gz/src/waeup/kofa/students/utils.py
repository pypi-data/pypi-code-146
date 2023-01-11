## $Id: utils.py 17182 2022-11-30 14:09:18Z henrik $
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
"""General helper functions and utilities for the students section.
"""
import grok
import textwrap
from copy import deepcopy
from cgi import escape
from time import time
from cStringIO import StringIO
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Image, Table, Spacer
from reportlab.platypus.doctemplate import LayoutError
from reportlab.platypus.flowables import PageBreak
from zope.event import notify
from zope.schema.interfaces import ConstraintNotSatisfied
from zope.component import getUtility, createObject, queryUtility
from zope.catalog.interfaces import ICatalog
from zope.formlib.form import setUpEditWidgets
from zope.i18n import translate
from waeup.kofa.interfaces import (
    IExtFileStore, IKofaUtils, RETURNING, PAID, CLEARED, GRADUATED,
    academic_sessions_vocab, IFileStoreNameChooser)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.students.interfaces import IStudentsUtils
from waeup.kofa.students.workflow import ADMITTED
from waeup.kofa.students.vocabularies import StudyLevelSource, MatNumNotInSource
from waeup.kofa.browser.pdf import (
    ENTRY1_STYLE, format_html, NOTE_STYLE, HEADING_STYLE, 
    get_signature_tables, get_qrcode)
from waeup.kofa.browser.interfaces import IPDFCreator
from waeup.kofa.utils.helpers import to_timezone

SLIP_STYLE = [
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    #('FONT', (0,0), (-1,-1), 'Helvetica', 11),
    ]

CONTENT_STYLE = [
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    #('FONT', (0,0), (-1,-1), 'Helvetica', 8),
    #('TEXTCOLOR',(0,0),(-1,0),colors.white),
    #('BACKGROUND',(0,0),(-1,0),colors.black),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 1, colors.black),
    ]

FONT_SIZE = 10
FONT_COLOR = 'black'

def trans(text, lang):
    # shortcut
    return translate(text, 'waeup.kofa', target_language=lang)

def formatted_text(text, color=FONT_COLOR, lang='en'):
    """Turn `text`, `color` and `size` into an HTML snippet.

    The snippet is suitable for use with reportlab and generating PDFs.
    Wraps the `text` into a ``<font>`` tag with passed attributes.

    Also non-strings are converted. Raw strings are expected to be
    utf-8 encoded (usually the case for widgets etc.).

    Finally, a br tag is added if widgets contain div tags
    which are not supported by reportlab.

    The returned snippet is unicode type.
    """
    if not isinstance(text, unicode):
        if isinstance(text, basestring):
            text = text.decode('utf-8')
        else:
            text = unicode(text)
    if text == 'None':
        text = ''
    # Very long matriculation numbers need to be wrapped
    if text.find(' ') == -1 and len(text.split('/')) > 6:
        text = '/'.join(text.split('/')[:5]) + \
            '/ ' + '/'.join(text.split('/')[5:])
    # Mainly for boolean values we need our customized
    # localisation of the zope domain
    text = translate(text, 'zope', target_language=lang)
    text = text.replace('</div>', '<br /></div>')
    tag1 = u'<font color="%s">' % (color)
    return tag1 + u'%s</font>' % text

def generate_student_id():
    students = grok.getSite()['students']
    new_id = students.unique_student_id
    return new_id

def set_up_widgets(view, ignore_request=False):
    view.adapters = {}
    view.widgets = setUpEditWidgets(
        view.form_fields, view.prefix, view.context, view.request,
        adapters=view.adapters, for_display=True,
        ignore_request=ignore_request
        )

def render_student_data(studentview, context, omit_fields=(),
                        lang='en', slipname=None, no_passport=False):
    """Render student table for an existing frame.
    """
    width, height = A4
    set_up_widgets(studentview, ignore_request=True)
    data_left = []
    data_middle = []
    style = getSampleStyleSheet()
    img = getUtility(IExtFileStore).getFileByContext(
        studentview.context, attr='passport.jpg')
    if img is None:
        from waeup.kofa.browser import DEFAULT_PASSPORT_IMAGE_PATH
        img = open(DEFAULT_PASSPORT_IMAGE_PATH, 'rb')
    doc_img = Image(img.name, width=4*cm, height=4*cm, kind='bound')
    data_left.append([doc_img])
    # Uniben wants a second picture. We add this picture here.
    img2 = getUtility(IExtFileStore).getFileByContext(
        studentview.context, attr='passport2.jpg')
    if img2 is not None:
        doc_img2 = Image(img2.name, width=4*cm, height=4*cm, kind='bound')
        data_left.append([doc_img2])
    #data.append([Spacer(1, 12)])

    f_label = trans(_('Name:'), lang)
    f_label = Paragraph(f_label, ENTRY1_STYLE)
    f_text = formatted_text(studentview.context.display_fullname)
    f_text = Paragraph(f_text, ENTRY1_STYLE)
    data_middle.append([f_label,f_text])

    for widget in studentview.widgets:
        if 'name' in widget.name:
            continue
        f_label = translate(
            widget.label.strip(), 'waeup.kofa',
            target_language=lang)
        f_label = Paragraph('%s:' % f_label, ENTRY1_STYLE)
        f_text = formatted_text(widget(), lang=lang)
        f_text = Paragraph(f_text, ENTRY1_STYLE)
        data_middle.append([f_label,f_text])
    if not 'date_of_birth' in omit_fields:
        f_label = trans(_('Date of Birth:'), lang)
        f_label = Paragraph(f_label, ENTRY1_STYLE)
        date_of_birth = studentview.context.date_of_birth
        tz = getUtility(IKofaUtils).tzinfo
        date_of_birth = to_timezone(date_of_birth, tz)
        if date_of_birth is not None:
            date_of_birth = date_of_birth.strftime("%d/%m/%Y")
        f_text = formatted_text(date_of_birth)
        f_text = Paragraph(f_text, ENTRY1_STYLE)
        data_middle.append([f_label,f_text])
    if getattr(studentview.context, 'certcode', None):
        if not 'certificate' in omit_fields:
            f_label = trans(_('Study Course:'), lang)
            f_label = Paragraph(f_label, ENTRY1_STYLE)
            f_text = formatted_text(
                studentview.context['studycourse'].certificate.longtitle)
            f_text = Paragraph(f_text, ENTRY1_STYLE)
            data_middle.append([f_label,f_text])
        if not 'department' in omit_fields:
            f_label = trans(_('Department:'), lang)
            f_label = Paragraph(f_label, ENTRY1_STYLE)
            f_text = formatted_text(
                studentview.context[
                'studycourse'].certificate.__parent__.__parent__.longtitle,
                )
            f_text = Paragraph(f_text, ENTRY1_STYLE)
            data_middle.append([f_label,f_text])
        if not 'faculty' in omit_fields:
            f_label = trans(_('Faculty:'), lang)
            f_label = Paragraph(f_label, ENTRY1_STYLE)
            f_text = formatted_text(
                studentview.context[
                'studycourse'].certificate.__parent__.__parent__.__parent__.longtitle,
                )
            f_text = Paragraph(f_text, ENTRY1_STYLE)
            data_middle.append([f_label,f_text])
        if not 'current_mode' in omit_fields:
            studymodes_dict = getUtility(IKofaUtils).STUDY_MODES_DICT
            sm = studymodes_dict[studentview.context.current_mode]
            f_label = trans(_('Study Mode:'), lang)
            f_label = Paragraph(f_label, ENTRY1_STYLE)
            f_text = formatted_text(sm)
            f_text = Paragraph(f_text, ENTRY1_STYLE)
            data_middle.append([f_label,f_text])
        if not 'entry_session' in omit_fields:
            f_label = trans(_('Entry Session:'), lang)
            f_label = Paragraph(f_label, ENTRY1_STYLE)
            entry_session = studentview.context.entry_session
            try:
                entry_session = academic_sessions_vocab.getTerm(
                    entry_session).title
            except LookupError:
                entry_session = _('void')
            f_text = formatted_text(entry_session)
            f_text = Paragraph(f_text, ENTRY1_STYLE)
            data_middle.append([f_label,f_text])
        # Requested by Uniben, does not really make sense
        if not 'current_level' in omit_fields:
            f_label = trans(_('Current Level:'), lang)
            f_label = Paragraph(f_label, ENTRY1_STYLE)
            current_level = studentview.context['studycourse'].current_level
            studylevelsource = StudyLevelSource().factory
            current_level = studylevelsource.getTitle(
                studentview.context, current_level)
            f_text = formatted_text(current_level)
            f_text = Paragraph(f_text, ENTRY1_STYLE)
            data_middle.append([f_label,f_text])

    if no_passport:
        table = Table(data_middle,style=SLIP_STYLE)
        table.hAlign = 'LEFT'
        return table

    # append QR code to the right
    if slipname:
        url = studentview.url(context, slipname)
        data_right = [[get_qrcode(url, width=70.0)]]
        table_right = Table(data_right,style=SLIP_STYLE)
    else:
        table_right = None

    table_left = Table(data_left,style=SLIP_STYLE)
    table_middle = Table(data_middle,style=SLIP_STYLE, colWidths=[5*cm, 5*cm])
    table = Table([[table_left, table_middle, table_right],],style=SLIP_STYLE)
    return table

def render_table_data(tableheader, tabledata, lang='en'):
    """Render children table for an existing frame.
    """
    data = []
    #data.append([Spacer(1, 12)])
    line = []
    style = getSampleStyleSheet()
    for element in tableheader:
        field = '<strong>%s</strong>' % formatted_text(element[0], lang=lang)
        field = Paragraph(field, style["Normal"])
        line.append(field)
    data.append(line)
    for ticket in tabledata:
        line = []
        for element in tableheader:
              field = formatted_text(getattr(ticket,element[1],u' '))
              field = Paragraph(field, style["Normal"])
              line.append(field)
        data.append(line)
    table = Table(data,colWidths=[
        element[2]*cm for element in tableheader], style=CONTENT_STYLE)
    return table

def render_transcript_data(view, tableheader, levels_data, lang='en'):
    """Render children table for an existing frame.
    """
    data = []
    style = getSampleStyleSheet()
    format_float = getUtility(IKofaUtils).format_float
    for level in levels_data:
        level_obj = level['level']
        tickets = level['tickets_1'] + level['tickets_2'] + level['tickets_3']
        if not tickets:
            continue
        headerline = []
        tabledata = []
        if 'evel' in view.level_dict.get('ticket.level', str(level_obj.level)):
            subheader = '%s %s, %s' % (
                trans(_('Session'), lang),
                view.session_dict[level_obj.level_session],
                view.level_dict.get('ticket.level', str(level_obj.level)))
        else:
            subheader = '%s %s, %s %s' % (
                trans(_('Session'), lang),
                view.session_dict[level_obj.level_session],
                trans(_('Level'), lang),
                view.level_dict.get(level_obj.level, str(level_obj.level)))
        data.append(Paragraph(subheader, HEADING_STYLE))
        for element in tableheader:
            field = '<strong>%s</strong>' % formatted_text(element[0])
            field = Paragraph(field, style["Normal"])
            headerline.append(field)
        tabledata.append(headerline)
        for ticket in tickets:
            ticketline = []
            for element in tableheader:
                  field = formatted_text(getattr(ticket,element[1],u' '))
                  field = Paragraph(field, style["Normal"])
                  ticketline.append(field)
            tabledata.append(ticketline)
        table = Table(tabledata,colWidths=[
            element[2]*cm for element in tableheader], style=CONTENT_STYLE)
        data.append(table)
        sgpa = format_float(level['sgpa'], 2)
        sgpa = '%s: %s' % (trans('Sessional GPA (rectified)', lang), sgpa)
        #sgpa = '%s: %.2f' % (trans('Sessional GPA (rectified)', lang), level['sgpa'])
        data.append(Paragraph(sgpa, style["Normal"]))
        if getattr(level_obj, 'transcript_remark', None):
            remark = '%s: %s' % (
                trans('Transcript Remark', lang),
                getattr(level_obj, 'transcript_remark'))
            data.append(Paragraph(remark, style["Normal"]))
    return data

def docs_as_flowables(view, lang='en'):
    """Create reportlab flowables out of scanned docs.
    """
    # XXX: fix circular import problem
    from waeup.kofa.browser.fileviewlets import FileManager
    from waeup.kofa.browser import DEFAULT_IMAGE_PATH
    style = getSampleStyleSheet()
    data = []

    # Collect viewlets
    fm = FileManager(view.context, view.request, view)
    fm.update()
    if fm.viewlets:
        sc_translation = trans(_('Scanned Documents'), lang)
        data.append(Paragraph(sc_translation, HEADING_STYLE))
        # Insert list of scanned documents
        table_data = []
        for viewlet in fm.viewlets:
            if viewlet.file_exists:
                # Show viewlet only if file exists
                f_label = Paragraph(trans(viewlet.label, lang), ENTRY1_STYLE)
                img_path = getattr(getUtility(IExtFileStore).getFileByContext(
                    view.context, attr=viewlet.download_name), 'name', None)
                #f_text = Paragraph(trans(_('(not provided)'),lang), ENTRY1_STYLE)
                if img_path is None:
                    pass
                elif not img_path[-4:] in ('.jpg', '.JPG'):
                    # reportlab requires jpg images, I think.
                    f_text = Paragraph('%s (not displayable)' % (
                        viewlet.title,), ENTRY1_STYLE)
                else:
                    f_text = Image(img_path, width=2*cm, height=1*cm, kind='bound')
                table_data.append([f_label, f_text])
        if table_data:
            # safety belt; empty tables lead to problems.
            data.append(Table(table_data, style=SLIP_STYLE))
    return data

class StudentsUtils(grok.GlobalUtility):
    """A collection of methods subject to customization.
    """
    grok.implements(IStudentsUtils)

    def getReturningData(self, student):
        """ Define what happens after school fee payment
        depending on the student's senate verdict.
        In the base configuration current level is always increased
        by 100 no matter which verdict has been assigned.
        """
        new_level = student['studycourse'].current_level + 100
        new_session = student['studycourse'].current_session + 1
        return new_session, new_level

    def setReturningData(self, student):
        """ Define what happens after school fee payment
        depending on the student's senate verdict.
        This method follows the same algorithm as `getReturningData` but
        it also sets the new values.
        """
        new_session, new_level = self.getReturningData(student)
        try:
            student['studycourse'].current_level = new_level
        except ConstraintNotSatisfied:
            # Do not change level if level exceeds the
            # certificate's end_level.
            pass
        student['studycourse'].current_session = new_session
        verdict = student['studycourse'].current_verdict
        student['studycourse'].current_verdict = '0'
        student['studycourse'].previous_verdict = verdict
        return

    def _getSessionConfiguration(self, session):
        try:
            return grok.getSite()['configuration'][str(session)]
        except KeyError:
            return None

    def _isPaymentDisabled(self, p_session, category, student):
        academic_session = self._getSessionConfiguration(p_session)
        if category == 'schoolfee' and \
            'sf_all' in academic_session.payment_disabled:
            return True
        return False

    def samePaymentMade(self, student, category, p_item, p_session):
        for key in student['payments'].keys():
            ticket = student['payments'][key]
            if ticket.p_state == 'paid' and\
               ticket.p_category == category and \
               ticket.p_item != 'Balance' and \
               ticket.p_item == p_item and \
               ticket.p_session == p_session:
                  return True
        return False

    def setPaymentDetails(self, category, student,
            previous_session=None, previous_level=None, combi=[]):
        """Create a payment ticket and set the payment data of a
        student for the payment category specified.
        """
        p_item = u''
        amount = 0.0
        if previous_session:
            if previous_session < student['studycourse'].entry_session:
                return _('The previous session must not fall below '
                         'your entry session.'), None
            if category == 'schoolfee':
                # School fee is always paid for the following session
                if previous_session > student['studycourse'].current_session:
                    return _('This is not a previous session.'), None
            else:
                if previous_session > student['studycourse'].current_session - 1:
                    return _('This is not a previous session.'), None
            p_session = previous_session
            p_level = previous_level
            p_current = False
        else:
            p_session = student['studycourse'].current_session
            p_level = student['studycourse'].current_level
            p_current = True
        academic_session = self._getSessionConfiguration(p_session)
        if academic_session == None:
            return _(u'Session configuration object is not available.'), None
        # Determine fee.
        if category == 'schoolfee':
            try:
                certificate = student['studycourse'].certificate
                p_item = certificate.code
            except (AttributeError, TypeError):
                return _('Study course data are incomplete.'), None
            if previous_session:
                # Students can pay for previous sessions in all
                # workflow states.  Fresh students are excluded by the
                # update method of the PreviousPaymentAddFormPage.
                if previous_level == 100:
                    amount = getattr(certificate, 'school_fee_1', 0.0)
                else:
                    amount = getattr(certificate, 'school_fee_2', 0.0)
            else:
                if student.state == CLEARED:
                    amount = getattr(certificate, 'school_fee_1', 0.0)
                elif student.state == RETURNING:
                    # In case of returning school fee payment the
                    # payment session and level contain the values of
                    # the session the student has paid for. Payment
                    # session is always next session.
                    p_session, p_level = self.getReturningData(student)
                    academic_session = self._getSessionConfiguration(p_session)
                    if academic_session == None:
                        return _(
                            u'Session configuration object is not available.'
                            ), None
                    amount = getattr(certificate, 'school_fee_2', 0.0)
                elif student.is_postgrad and student.state == PAID:
                    # Returning postgraduate students also pay for the
                    # next session but their level always remains the
                    # same.
                    p_session += 1
                    academic_session = self._getSessionConfiguration(p_session)
                    if academic_session == None:
                        return _(
                            u'Session configuration object is not available.'
                            ), None
                    amount = getattr(certificate, 'school_fee_2', 0.0)
        elif category == 'clearance':
            try:
                p_item = student['studycourse'].certificate.code
            except (AttributeError, TypeError):
                return _('Study course data are incomplete.'), None
            amount = academic_session.clearance_fee
        elif category == 'bed_allocation':
            acco_details = self.getAccommodationDetails(student)
            p_session = acco_details['booking_session']
            p_item = acco_details['bt']
            amount = academic_session.booking_fee
        elif category == 'hostel_maintenance':
            amount = 0.0
            booking_session = grok.getSite()['hostels'].accommodation_session
            bedticket = student['accommodation'].get(str(booking_session), None)
            if bedticket is not None and bedticket.bed is not None:
                p_session = booking_session
                p_item = bedticket.bed_coordinates
                if bedticket.bed.__parent__.maint_fee > 0:
                    amount = bedticket.bed.__parent__.maint_fee
                else:
                    # fallback
                    amount = academic_session.maint_fee
            else:
                return _(u'No bed allocated.'), None
        elif category == 'combi' and combi:
            categories = getUtility(IKofaUtils).COMBI_PAYMENT_CATEGORIES
            for cat in combi:
                fee_name = cat + '_fee'
                cat_amount = getattr(academic_session, fee_name, 0.0)
                if not cat_amount:
                    return _('%s undefined.' % categories[cat]), None
                amount += cat_amount
                p_item += u'%s + ' % categories[cat]
            p_item = p_item.strip(' + ')
        else:
            fee_name = category + '_fee'
            amount = getattr(academic_session, fee_name, 0.0)
        if amount in (0.0, None):
            return _('Amount could not be determined.'), None
        if self.samePaymentMade(student, category, p_item, p_session):
            return _('This type of payment has already been made.'), None
        if self._isPaymentDisabled(p_session, category, student):
            return _('This category of payments has been disabled.'), None
        payment = createObject(u'waeup.StudentOnlinePayment')
        timestamp = ("%d" % int(time()*10000))[1:]
        payment.p_id = "p%s" % timestamp
        payment.p_category = category
        payment.p_item = p_item
        payment.p_session = p_session
        payment.p_level = p_level
        payment.p_current = p_current
        payment.amount_auth = amount
        payment.p_combi = combi
        return None, payment

    def setBalanceDetails(self, category, student,
            balance_session, balance_level, balance_amount):
        """Create a balance payment ticket and set the payment data
        as selected by the student.
        """
        p_item = u'Balance'
        p_session = balance_session
        p_level = balance_level
        p_current = False
        amount = balance_amount
        academic_session = self._getSessionConfiguration(p_session)
        if academic_session == None:
            return _(u'Session configuration object is not available.'), None
        if amount in (0.0, None) or amount < 0:
            return _('Amount must be greater than 0.'), None
        payment = createObject(u'waeup.StudentOnlinePayment')
        timestamp = ("%d" % int(time()*10000))[1:]
        payment.p_id = "p%s" % timestamp
        payment.p_category = category
        payment.p_item = p_item
        payment.p_session = p_session
        payment.p_level = p_level
        payment.p_current = p_current
        payment.amount_auth = amount
        return None, payment

    def increaseMatricInteger(self, student):
        """Increase counter for matric numbers.
        This counter can be a centrally stored attribute or an attribute of 
        faculties, departments or certificates. In the base package the counter
        is as an attribute of the site configuration container.
        """
        grok.getSite()['configuration'].next_matric_integer += 1
        return

    def constructMatricNumber(self, student):
        """Fetch the matric number counter which fits the student and
        construct the new matric number of the student.
        In the base package the counter is returned which is as an attribute
        of the site configuration container.
        """
        next_integer = grok.getSite()['configuration'].next_matric_integer
        if next_integer == 0:
            return _('Matriculation number cannot be set.'), None
        return None, unicode(next_integer)

    def setMatricNumber(self, student):
        """Set matriculation number of student. If the student's matric number
        is unset a new matric number is
        constructed according to the matriculation number construction rules
        defined in the `constructMatricNumber` method. The new matric number is
        set, the students catalog updated. The corresponding matric number
        counter is increased by one.

        This method is tested but not used in the base package. It can
        be used in custom packages by adding respective views
        and by customizing `increaseMatricInteger` and `constructMatricNumber`
        according to the university's matriculation number construction rules.

        The method can be disabled by setting the counter to zero.
        """
        if student.matric_number is not None:
            return _('Matriculation number already set.'), None
        if student.certcode is None:
            return _('No certificate assigned.'), None
        error, matric_number = self.constructMatricNumber(student)
        if error:
            return error, None
        try:
            student.matric_number = matric_number
        except MatNumNotInSource:
            return _('Matriculation number %s exists.' % matric_number), None
        notify(grok.ObjectModifiedEvent(student))
        self.increaseMatricInteger(student)
        return None, matric_number

    def allowPortraitChange(self, student):
        """Check if student is allowed to change the portrait file.
        """
        if student.state not in self.PORTRAIT_CHANGE_STATES:
            return False
        return True

    def getAccommodationDetails(self, student):
        """Determine the accommodation data of a student.
        """
        d = {}
        d['error'] = u''
        hostels = grok.getSite()['hostels']
        d['booking_session'] = hostels.accommodation_session
        d['allowed_states'] = hostels.accommodation_states
        d['startdate'] = hostels.startdate
        d['enddate'] = hostels.enddate
        d['expired'] = hostels.expired
        # Determine bed type
        studycourse = student['studycourse']
        certificate = getattr(studycourse,'certificate',None)
        entry_session = studycourse.entry_session
        current_level = studycourse.current_level
        if None in (entry_session, current_level, certificate):
            return d
        end_level = certificate.end_level
        if current_level == 10:
            bt = 'pr'
        elif entry_session == grok.getSite()['hostels'].accommodation_session:
            bt = 'fr'
        elif current_level >= end_level:
            bt = 'fi'
        else:
            bt = 're'
        if student.sex == 'f':
            sex = 'female'
        else:
            sex = 'male'
        special_handling = 'regular'
        d['bt'] = u'%s_%s_%s' % (special_handling,sex,bt)
        return d

    ACCOMMODATION_SPAN = 0

    def checkAccommodationRequirements(self, student, acc_details):
        if acc_details.get('expired', False):
            startdate = acc_details.get('startdate')
            enddate = acc_details.get('enddate')
            if startdate and enddate:
                tz = getUtility(IKofaUtils).tzinfo
                startdate = to_timezone(
                    startdate, tz).strftime("%d/%m/%Y %H:%M:%S")
                enddate = to_timezone(
                    enddate, tz).strftime("%d/%m/%Y %H:%M:%S")
                return _("Outside booking period: ${a} - ${b}",
                         mapping = {'a': startdate, 'b': enddate})
            else:
                return _("Outside booking period.")
        if not acc_details.get('bt'):
            return _("Your data are incomplete.")
        if not student.state in acc_details['allowed_states']:
            return _("You are in the wrong registration state.")
        if  acc_details['booking_session'] - student[
            'studycourse'].current_session > self.ACCOMMODATION_SPAN:
            return _('Your current session does not allow ' + \
                    'to book accommodation.')
        bsession = str(acc_details['booking_session'])
        if bsession in student['accommodation'].keys() \
            and not 'booking expired' in \
            student['accommodation'][bsession].bed_coordinates:
            return _('You already booked a bed space in '
                     'current accommodation session.')
        return

    def selectBed(self, available_beds):
        """Select a bed from a filtered list of available beds.
        In the base configuration beds are sorted by the sort id
        of the hostel and the bed number. The first bed found in
        this sorted list is taken.
        """
        sorted_beds = sorted(available_beds,
                key=lambda bed: 1000 * bed.__parent__.sort_id + bed.bed_number)
        return sorted_beds[0]

    def GPABoundaries(self, faccode=None, depcode=None, certcode=None):
        return ((1, 'Fail'),
               (1.5, 'Pass'),
               (2.4, '3rd Class'),
               (3.5, '2nd Class Lower'),
               (4.5, '2nd Class Upper'),
               (5, '1st Class'))

    def getClassFromCGPA(self, gpa, student):
        """Determine the class of degree. In some custom packages
        this class depends on e.g. the entry session of the student. In the
        base package, it does not.
        """
        if gpa < self.GPABoundaries()[0][0]:
            return 0, self.GPABoundaries()[0][1]
        if gpa < self.GPABoundaries()[1][0]:
            return 1, self.GPABoundaries()[1][1]
        if gpa < self.GPABoundaries()[2][0]:
            return 2, self.GPABoundaries()[2][1]
        if gpa < self.GPABoundaries()[3][0]:
            return 3, self.GPABoundaries()[3][1]
        if gpa < self.GPABoundaries()[4][0]:
            return 4, self.GPABoundaries()[4][1]
        if gpa <= self.GPABoundaries()[5][0]:
            return 5, self.GPABoundaries()[5][1]
        return

    def getDegreeClassNumber(self, level_obj):
        """Get degree class number (used for SessionResultsPresentation
        reports).
        """
        if level_obj.gpa_params[1] == 0:
            # No credits weighted
            return 6
        return self.getClassFromCGPA(
            level_obj.cumulative_params[0], level_obj.student)[0]

    def _saveTranscriptPDF(self, student, transcript):
        """Create a transcript PDF file and store it in student folder.
        """
        file_store = getUtility(IExtFileStore)
        file_id = IFileStoreNameChooser(student).chooseName(
            attr="final_transcript.pdf")
        file_store.createFile(file_id, StringIO(transcript))
        return

    def warnCreditsOOR(self, studylevel, course=None):
        """Return message if credits are out of range. In the base
        package only maximum credits is set.
        """
        if course and studylevel.total_credits + course.credits > 50:
            return _('Maximum credits exceeded.')
        elif studylevel.total_credits > 50:
            return _('Maximum credits exceeded.')
        return

    def warnCourseAlreadyPassed(self, studylevel, course):
        """Return message if course has already been passed at
        previous levels.
        """
        for slevel in studylevel.__parent__.values():
            for cticket in slevel.values():
                if cticket.code == course.code \
                    and cticket.total_score >= cticket.passmark:
                    return _('Course has already been passed at previous level.')
        return False

    def getBedCoordinates(self, bedticket):
        """Return descriptive bed coordinates.
        This method can be used to customize the `display_coordinates`
        property method in order to  display a
        customary description of the bed space.
        """
        return bedticket.bed_coordinates

    def clearance_disabled_message(self, student):
        """Render message if clearance is disabled.
        """
        try:
            session_config = grok.getSite()[
                'configuration'][str(student.current_session)]
        except KeyError:
            return _('Session configuration object is not available.')
        if not session_config.clearance_enabled:
            return _('Clearance is disabled for this session.')
        return None

    def getPDFCreator(self, context):
        """Get a pdf creator suitable for `context`.
        The default implementation always returns the default creator.
        """
        return getUtility(IPDFCreator)

    def _mergeFiles(self, mergefiles, watermark, pdf_stream):
        merger = PdfFileMerger()
        merger.append(StringIO(pdf_stream))
        for file in mergefiles:
            if watermark:
                # Pass through all pages of each file
                # and merge with watermark page. Paint
                # watermark first to make it transparent.
                marked_file = PdfFileWriter()
                orig_file = PdfFileReader(file)
                num_pages = orig_file.getNumPages()
                for num in range(num_pages):
                    watermark_file = PdfFileReader(watermark)
                    page = watermark_file.getPage(0)
                    page.mergePage(orig_file.getPage(num))
                    marked_file.addPage(page)
                # Save into a file-like object
                tmp1 = StringIO()
                marked_file.write(tmp1)
                # Append the file-like object
                merger.append(tmp1)
            else:
                # Just append the file object
                merger.append(file)
        # Save into a file-like object
        tmp2 = StringIO()
        merger.write(tmp2)
        return tmp2.getvalue()

    def renderPDF(self, view, filename='slip.pdf', student=None,
                  studentview=None,
                  tableheader=[], tabledata=[],
                  note=None, signatures=None, sigs_in_footer=(),
                  show_scans=True, topMargin=1.5,
                  omit_fields=(),
                  mergefiles=None, watermark=None,
                  pagebreak=False):
        """Render pdf slips for various pages (also some pages
        in the applicants module).
        """
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        # XXX: tell what the different parameters mean
        style = getSampleStyleSheet()
        creator = self.getPDFCreator(student)
        data = []
        doc_title = view.label
        author = '%s (%s)' % (view.request.principal.title,
                              view.request.principal.id)
        footer_text = view.label.split('\n')
        if len(footer_text) > 2:
            # We can add a department in first line, second line is used
            footer_text = footer_text[1]
        else:
            # Only the first line is used for the footer
            footer_text = footer_text[0]
        if getattr(student, 'student_id', None) is not None:
            footer_text = "%s - %s - " % (student.student_id, footer_text)

        # Insert student data table
        if student is not None:
            if view.form_fields:
                bd_translation = trans(_('Base Data'), portal_language)
                data.append(Paragraph(bd_translation, HEADING_STYLE))
            data.append(render_student_data(
                studentview, view.context, omit_fields, lang=portal_language,
                slipname=filename))

        # Insert widgets
        if view.form_fields:
            data.append(Paragraph(view.title, HEADING_STYLE))
            separators = getattr(self, 'SEPARATORS_DICT', {})
            table = creator.getWidgetsTable(
                view.form_fields, view.context, None, lang=portal_language,
                separators=separators)
            data.append(table)

        # Insert scanned docs
        if show_scans:
            data.extend(docs_as_flowables(view, portal_language))

        # Insert history
        if filename == 'clearance_slip.pdf':
            hist_translation = trans(_('Workflow History'), portal_language)
            data.append(Paragraph(hist_translation, HEADING_STYLE))
            data.extend(creator.fromStringList(student.history.messages))

        # Insert content tables (optionally on second page)
        if hasattr(view, 'tabletitle'):
            for i in range(len(view.tabletitle)):
                if tabledata[i] and tableheader[i]:
                    tabletitle = view.tabletitle[i]
                    if tabletitle.startswith('_PB_'):
                        data.append(PageBreak())
                        tabletitle = view.tabletitle[i].strip('_PB_')
                    #data.append(Spacer(1, 20))
                    data.append(Paragraph(tabletitle, HEADING_STYLE))
                    data.append(Spacer(1, 8))
                    contenttable = render_table_data(tableheader[i],tabledata[i])
                    data.append(contenttable)

        # Insert signatures
        # XXX: We are using only sigs_in_footer in waeup.kofa, so we
        # do not have a test for the following lines.
        if signatures and not sigs_in_footer:
            # Insert page break if necessary, else some space
            if pagebreak:
                data.append(PageBreak())
            else:
                data.append(Spacer(1, 20))
            # Render one signature table per signature to
            # get date and signature in line.
            for signature in signatures:
                signaturetables = get_signature_tables(signature)
                data.append(signaturetables[0])

        view.response.setHeader(
            'Content-Type', 'application/pdf')
        try:
            pdf_stream = creator.create_pdf(
                data, None, doc_title, author=author, footer=footer_text,
                note=note, sigs_in_footer=sigs_in_footer, topMargin=topMargin)
        except IOError:
            view.flash('Error in image file.')
            return view.redirect(view.url(view.context))
        except LayoutError, err:
            view.flash(
                'PDF file could not be created. Reportlab error message: %s'
                % escape(err.message),
                type="danger")
            return view.redirect(view.url(view.context))
        if mergefiles:
            return self._mergeFiles(mergefiles, watermark, pdf_stream)
        return pdf_stream

    def _admissionText(self, student, portal_language):
        inst_name = grok.getSite()['configuration'].name
        text = trans(_(
            'This is to inform you that you have been provisionally'
            ' admitted into ${a} as follows:', mapping = {'a': inst_name}),
            portal_language)
        return text

    def renderPDFAdmissionLetter(self, view, student=None, omit_fields=(),
                                 pre_text=None, post_text=None,
                                 topMargin = 1.5,
                                 letterhead_path=None,
                                 mergefiles=None, watermark=None):
        """Render pdf admission letter.
        """
        if student is None:
            return
        style = getSampleStyleSheet()
        if letterhead_path:
            creator = getUtility(IPDFCreator, name='letter')
        else:
            creator = self.getPDFCreator(student)
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        data = []
        doc_title = view.label
        author = '%s (%s)' % (view.request.principal.title,
                              view.request.principal.id)
        footer_text = view.label.split('\n')
        if len(footer_text) > 2:
            # We can add a department in first line
            footer_text = footer_text[1]
        else:
            # Only the first line is used for the footer
            footer_text = footer_text[0]
        if getattr(student, 'student_id', None) is not None:
            footer_text = "%s - %s - " % (student.student_id, footer_text)

        # Text before student data
        if pre_text is None:
            html = format_html(self._admissionText(student, portal_language))
        else:
            html = format_html(pre_text)
        if html:
            data.append(Paragraph(html, NOTE_STYLE))
            data.append(Spacer(1, 20))

        # Student data
        data.append(render_student_data(view, student,
                    omit_fields, lang=portal_language,
                    slipname='admission_slip.pdf'))

        # Text after student data
        data.append(Spacer(1, 20))
        if post_text is None:
            datelist = student.history.messages[0].split()[0].split('-')
            creation_date = u'%s/%s/%s' % (datelist[2], datelist[1], datelist[0])
            post_text = trans(_(
                'Your Kofa student record was created on ${a}.',
                mapping = {'a': creation_date}),
                portal_language)
        #html = format_html(post_text)
        #data.append(Paragraph(html, NOTE_STYLE))

        # Create pdf stream
        view.response.setHeader(
            'Content-Type', 'application/pdf')
        pdf_stream = creator.create_pdf(
            data, None, doc_title, author=author, footer=footer_text,
            note=post_text, topMargin=topMargin,
            letterhead_path=letterhead_path)
        if mergefiles:
            return self._mergeFiles(mergefiles, watermark, pdf_stream)
        return pdf_stream

    def renderPDFTranscript(self, view, filename='transcript.pdf',
                  student=None,
                  studentview=None,
                  note=None,
                  signatures=(),
                  sigs_in_footer=(),
                  digital_sigs=(),
                  show_scans=True, topMargin=1.5,
                  omit_fields=(),
                  tableheader=None,
                  no_passport=False,
                  save_file=False):
        """Render pdf slip of a transcripts.
        """
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        # XXX: tell what the different parameters mean
        style = getSampleStyleSheet()
        creator = self.getPDFCreator(student)
        data = []
        doc_title = view.label
        author = '%s (%s)' % (view.request.principal.title,
                              view.request.principal.id)
        footer_text = view.label.split('\n')
        if len(footer_text) > 2:
            # We can add a department in first line
            footer_text = footer_text[1]
        else:
            # Only the first line is used for the footer
            footer_text = footer_text[0]
        if getattr(student, 'student_id', None) is not None:
            footer_text = "%s - %s - " % (student.student_id, footer_text)

        # Insert student data table
        if student is not None:
            #bd_translation = trans(_('Base Data'), portal_language)
            #data.append(Paragraph(bd_translation, HEADING_STYLE))
            data.append(render_student_data(
                studentview, view.context,
                omit_fields, lang=portal_language,
                slipname=filename,
                no_passport=no_passport))

        transcript_data = view.context.getTranscriptData()
        levels_data = transcript_data[0]

        contextdata = []
        f_label = trans(_('Course of Study:'), portal_language)
        f_label = Paragraph(f_label, ENTRY1_STYLE)
        f_text = formatted_text(view.context.certificate.longtitle)
        f_text = Paragraph(f_text, ENTRY1_STYLE)
        contextdata.append([f_label,f_text])

        f_label = trans(_('Faculty:'), portal_language)
        f_label = Paragraph(f_label, ENTRY1_STYLE)
        f_text = formatted_text(
            view.context.certificate.__parent__.__parent__.__parent__.longtitle)
        f_text = Paragraph(f_text, ENTRY1_STYLE)
        contextdata.append([f_label,f_text])

        f_label = trans(_('Department:'), portal_language)
        f_label = Paragraph(f_label, ENTRY1_STYLE)
        f_text = formatted_text(
            view.context.certificate.__parent__.__parent__.longtitle)
        f_text = Paragraph(f_text, ENTRY1_STYLE)
        contextdata.append([f_label,f_text])

        f_label = trans(_('Entry Session:'), portal_language)
        f_label = Paragraph(f_label, ENTRY1_STYLE)
        f_text = formatted_text(
            view.session_dict.get(view.context.entry_session))
        f_text = Paragraph(f_text, ENTRY1_STYLE)
        contextdata.append([f_label,f_text])

        f_label = trans(_('Entry Mode:'), portal_language)
        f_label = Paragraph(f_label, ENTRY1_STYLE)
        f_text = formatted_text(view.studymode_dict.get(
            view.context.entry_mode))
        f_text = Paragraph(f_text, ENTRY1_STYLE)
        contextdata.append([f_label,f_text])

        f_label = trans(_('Cumulative GPA:'), portal_language)
        f_label = Paragraph(f_label, ENTRY1_STYLE)
        format_float = getUtility(IKofaUtils).format_float
        cgpa = format_float(transcript_data[1], 3)
        if student.state == GRADUATED:
            f_text = formatted_text('%s (%s)' % (
                cgpa, self.getClassFromCGPA(transcript_data[1], student)[1]))
        else:
            f_text = formatted_text('%s' % cgpa)
        f_text = Paragraph(f_text, ENTRY1_STYLE)
        contextdata.append([f_label,f_text])

        contexttable = Table(contextdata,style=SLIP_STYLE)
        data.append(contexttable)

        transcripttables = render_transcript_data(
            view, tableheader, levels_data, lang=portal_language)
        data.extend(transcripttables)

        # Insert signatures
        # XXX: We are using only sigs_in_footer in waeup.kofa, so we
        # do not have a test for the following lines.
        if signatures and not sigs_in_footer:
            data.append(Spacer(1, 20))
            # Render one signature table per signature to
            # get date and signature in line.
            for signature in signatures:
                signaturetables = get_signature_tables(signature)
                data.append(signaturetables[0])

        # Insert digital signatures
        if digital_sigs:
            data.append(Spacer(1, 20))
            sigs = digital_sigs.split('\n')
            for sig in sigs:
                data.append(Paragraph(sig, NOTE_STYLE))

        view.response.setHeader(
            'Content-Type', 'application/pdf')
        try:
            pdf_stream = creator.create_pdf(
                data, None, doc_title, author=author, footer=footer_text,
                note=note, sigs_in_footer=sigs_in_footer, topMargin=topMargin,
                view=view)
        except IOError:
            view.flash(_('Error in image file.'))
            return view.redirect(view.url(view.context))
        if save_file:
            self._saveTranscriptPDF(student, pdf_stream)
            return
        return pdf_stream

    def renderPDFCourseticketsOverview(
            self, view, name, session, data, lecturers, orientation,
            title_length, note):
        """Render pdf slip of course tickets for a lecturer.
        """
        filename = '%s_%s_%s_%s.pdf' % (
            name, view.context.code, session, view.request.principal.id)
        try:
            session = academic_sessions_vocab.getTerm(session).title
        except LookupError:
            session = _('void')
        creator = getUtility(IPDFCreator, name=orientation)
        style = getSampleStyleSheet()
        pdf_data = []
        pdf_data += [Paragraph(
            translate(_('<b>Lecturer(s): ${a}</b>',
                      mapping = {'a':lecturers})), style["Normal"]),]
        pdf_data += [Paragraph(
            translate(_('<b>Credits: ${a}</b>',
                      mapping = {'a':view.context.credits})), style["Normal"]),]
        # Not used in base package.
        if data[1]:
            pdf_data += [Paragraph(
                translate(_('<b>${a}</b>',
                    mapping = {'a':data[1][0]})), style["Normal"]),]
            pdf_data += [Paragraph(
                translate(_('<b>${a}</b>',
                    mapping = {'a':data[1][1]})), style["Normal"]),]
            pdf_data += [Paragraph(
                translate(_('<b>Total Students: ${a}</b>',
                    mapping = {'a':data[1][2]})), style["Normal"]),]
            pdf_data += [Paragraph(
                translate(_('<b>Total Pass: ${a} (${b}%)</b>',
                mapping = {'a':data[1][3],'b':data[1][4]})), style["Normal"]),]
            pdf_data += [Paragraph(
                translate(_('<b>Total Fail: ${a} (${b}%)</b>',
                mapping = {'a':data[1][5],'b':data[1][6]})), style["Normal"]),]
            grade_stats = []
            for item in sorted(data[1][7].items()):
                grade_stats.append(('%s=%s' % (item[0], item[1])))
            grade_stats_string = ', '.join(grade_stats)
            pdf_data += [Paragraph(
                translate(_('<b>${a}</b>',
                mapping = {'a':grade_stats_string})), style["Normal"]),]
        pdf_data.append(Spacer(1, 20))
        colWidths = [None] * len(data[0][0])
        pdf_data += [Table(data[0], colWidths=colWidths, style=CONTENT_STYLE,
                           repeatRows=1)]
        # Process title if too long
        title = " ".join(view.context.title.split())
        ct = textwrap.fill(title, title_length)
        ft = "" # title
        #if len(textwrap.wrap(title, title_length)) > 1:
        #    ft = textwrap.wrap(title, title_length)[0] + ' ...'
        doc_title = translate(_('${a} (${b})\nAcademic Session ${d}',
            mapping = {'a':ct,
                       'b':view.context.code,
                       'd':session}))
        if name == 'attendance':
            doc_title += '\n' + translate(_('Attendance Sheet'))
        if name == 'coursetickets':
            doc_title += '\n' + translate(_('Course Tickets Overview'))
        #footer_title = translate(_('${a} (${b}) - ${d}',
        #    mapping = {'a':ft,
        #               'b':view.context.code,
        #               'd':session}))
        footer_title = translate(_('${b} - ${d}',
            mapping = {'b':view.context.code,
                       'd':session}))
        author = '%s (%s)' % (view.request.principal.title,
                              view.request.principal.id)
        view.response.setHeader(
            'Content-Type', 'application/pdf')
        view.response.setHeader(
            'Content-Disposition:', 'attachment; filename="%s' % filename)
        pdf_stream = creator.create_pdf(
            pdf_data, None, doc_title, author, footer_title + ' -', note
            )
        return pdf_stream

    def updateCourseTickets(self, course):
        """Udate course tickets if course attributes were changed.
        """
        current_academic_session = grok.getSite()[
            'configuration'].current_academic_session
        if not current_academic_session:
            return
        cat = queryUtility(ICatalog, name='coursetickets_catalog')
        coursetickets = cat.searchResults(
            code=(course.code, course.code),
            session=(current_academic_session,current_academic_session))
        number = 0
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.', '')
        for ticket in coursetickets:
            if ticket.credits == course.credits:
                continue
            if ticket.student.current_session != current_academic_session:
                continue
            if ticket.student.state not in (PAID,):
                continue
            number += 1
            ticket.student.__parent__.logger.info(
                '%s - %s %s/%s credits updated (%s->%s)' % (
                    ob_class, ticket.student.student_id,
                    ticket.level, ticket.code, course.credits,
                    ticket.credits))
            ticket.credits = course.credits
        return number

    #: A dictionary which maps widget names to headlines. The headline
    #: is rendered in forms and on pdf slips above the respective
    #: display or input widget. There are no separating headlines
    #: in the base package.
    SEPARATORS_DICT = {}

    #: A tuple containing names of file upload viewlets which are not shown
    #: on the `StudentClearanceManageFormPage`. Nothing is being skipped
    #: in the base package. This attribute makes only sense, if intermediate
    #: custom packages are being used, like we do for all Nigerian portals.
    SKIP_UPLOAD_VIEWLETS = ()

    #: A tuple containing the names of registration states in which changing of
    #: passport pictures is allowed.
    PORTRAIT_CHANGE_STATES = (ADMITTED,)

    #: A tuple containing the names of registration states in which changing of
    #: scanned signatures is allowed.
    SIGNATURE_CHANGE_STATES = ()

    #: A tuple containing all exporter names referring to students or
    #: subobjects thereof.
    STUDENT_EXPORTER_NAMES = (
            'students',
            'studentstudycourses',
            'studentstudycourses_1',
            #'studentstudycourses_2',
            'studentstudylevels',
            #'studentstudylevels_1',
            #'studentstudylevels_2',
            'coursetickets',
            #'coursetickets_1',
            #'coursetickets_2',
            'studentpayments',
            'bedtickets',
            'trimmed',
            'outstandingcourses',
            'unpaidpayments',
            'sfpaymentsoverview',
            'sessionpaymentsoverview',
            'studylevelsoverview',
            'combocard',
            'bursary',
            'accommodationpayments',
            'transcriptdata',
            'trimmedpayments',
            )

    #: A tuple containing all exporter names needed for backing
    #: up student data
    STUDENT_BACKUP_EXPORTER_NAMES = (
            'students',
            'studentstudycourses',
            'studentstudycourses_1',
            'studentstudycourses_2',
            'studentstudylevels',
            'studentstudylevels_1',
            'studentstudylevels_2',
            'coursetickets',
            'coursetickets_1',
            'coursetickets_2',
            'studentpayments',
            'bedtickets')

    # Maximum size of upload files in kB
    MAX_KB = 250

    #: A prefix used when generating new student ids. Each student id will
    #: start with this string. The default is 'K' for Kofa.
    STUDENT_ID_PREFIX = u'K'
