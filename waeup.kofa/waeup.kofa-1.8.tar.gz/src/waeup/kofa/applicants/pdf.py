## $Id: pdf.py 16057 2020-04-18 08:12:53Z henrik $
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
"""
Generate PDF docs for applicants.
"""
import grok
from reportlab.platypus import Paragraph, Spacer, Table
from reportlab.lib.units import cm
from zope.component import getUtility
from zope.i18n import translate
from waeup.kofa.applicants.interfaces import IApplicant, IApplicantsUtils
from waeup.kofa.browser import DEFAULT_PASSPORT_IMAGE_PATH
from waeup.kofa.browser.interfaces import IPDFCreator
from waeup.kofa.browser.pdf import SMALL_PARA_STYLE, ENTRY1_STYLE, get_qrcode
from waeup.kofa.interfaces import IExtFileStore, IPDF, IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.widgets.datewidget import FriendlyDateDisplayWidget

SLIP_STYLE = [
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    #('FONT', (0,0), (-1,-1), 'Helvetica', 11),
    ]

class PDFApplicationSlip(grok.Adapter):
    """Create a PDF application slip for applicants.
    """
    # XXX: Many things in here are reusable. We might want to split
    # things. Possibly move parts to IPDFCreator?
    grok.context(IApplicant)
    grok.implements(IPDF)
    grok.name('application_slip')

    form_fields =  grok.AutoFields(IApplicant).omit(
        'locked', 'course_admitted', 'suspended',
        )
    form_fields['date_of_birth'].custom_widget = FriendlyDateDisplayWidget('le')
    column_two_fields = ('applicant_id', 'reg_number',
        'firstname', 'middlename', 'lastname')
    two_columns_design_fields = []

    @property
    def note(self):
        note = getattr(self.context.__parent__, 'application_slip_notice', None)
        if note:
            return '<br /><br />' + note
        return

    @property
    def target(self):
        return getattr(self.context.__parent__, 'prefix', None)

    @property
    def title(self):
        container_title = self.context.__parent__.title
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        ar_translation = translate(_('Application Record'),
            'waeup.kofa', target_language=portal_language)
        return '%s - %s %s' % (container_title,
            ar_translation, self.context.application_number)

    def _getCourseAdmittedLink(self, view):
        """Return link, title and code in html format to the certificate
           admitted.
        """
        course_admitted = self.context.course_admitted
        if course_admitted is not None:
            if view is None:
                title = course_admitted.title
                code = course_admitted.code
                return '%s - %s' %(code,title)
            if getattr(course_admitted, '__parent__',None):
                url = view.url(course_admitted)
                title = course_admitted.title
                code = course_admitted.code
                return '<a href="%s">%s - %s</a>' %(url,code,title)
        return ''

    def _getDeptAndFaculty(self):
        """Return long titles of department and faculty.

        Returns a list [department_title, faculty_title]

        If the context applicant has no course admitted or dept. and
        faculty cannot be determined, ``None`` is returned.
        """
        course_admitted = self.context.course_admitted
        dept = getattr(
                getattr(course_admitted, '__parent__', None),
                '__parent__', None)
        faculty = getattr(dept, '__parent__', None)
        return [x is not None and x.longtitle or x for x in dept, faculty]

    def _addLoginInformation(self):
        if self.context.state == 'created':
            comment = translate(_(
                '\n Proceed to the login page of the portal' +
                ' and enter your new credentials:' +
                ' user name= ${a}, password = ${b}. ' +
                'Change your password when you have logged in.',
                mapping = {
                    'a':self.context.student_id,
                    'b':self.context.application_number}
                ))
            return comment
        return

    def _getPDFCreator(self):
        return getUtility(IPDFCreator)

    def __call__(self, view=None, note=None):
        """Return a PDF representation of the context applicant.

        If no `view` is given, the course admitted field will be an
        empty string and author will be set as ``'unknown'``.

        If a `view` is given, author will be set as the calling
        principal.
        """
        doc_title = '\n'.join([x.strip() for x in self.title.split(' - ')])
        data = []
        topMargin = 1.5
        if len(self.title.split(' - ')) > 2:
            topMargin = 1.8
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        separators = getUtility(IApplicantsUtils).SEPARATORS_DICT
        creator = self._getPDFCreator()

        # append history
        data.extend(creator.fromStringList(self.context.history.messages))
        data.append(Spacer(1, 5))

        if self.context.__parent__.with_picture:

            # create three-column header table
            # append photograph to the left
            img_path = getattr(
                getUtility(IExtFileStore).getFileByContext(self.context),
                'name', DEFAULT_PASSPORT_IMAGE_PATH)
            data_left = [[creator.getImage(img_path)]]
            table_left = Table(data_left,style=SLIP_STYLE)

            # append base data table to the middle
            fields = [
                field for field in self.form_fields
                    if field.__name__ in self.column_two_fields]
            table_middle = creator.getWidgetsTable(
                fields, self.context, None, lang=portal_language,
                separators=None, colWidths=[5*cm, 4.5*cm])

            # append QR code to the right
            if view is not None:
                url = view.url(self.context, 'application_slip.pdf')
                data_right = [[get_qrcode(url, width=70.0)]]
                table_right = Table(data_right,style=SLIP_STYLE)
            else:
                table_right = None

            header_table = Table(
                [[table_left, table_middle, table_right],],style=SLIP_STYLE)
            data.append(header_table)

        else:
            fields = [
                field for field in self.form_fields
                    if field.__name__ in self.column_two_fields]
            data.append(creator.getWidgetsTable(
                fields, self.context, None, lang=portal_language,
                separators=None, colWidths=[7*cm, 10*cm]))

        # append widgets except those already added in column two
        # and those in two_columns_design_fields
        dept, faculty = self._getDeptAndFaculty()
        fields = [
            field for field in self.form_fields
                if not field.__name__ in self.column_two_fields and
                not field.__name__ in self.two_columns_design_fields]
        data.append(creator.getWidgetsTable(
            fields, self.context, view, lang=portal_language,
            domain='waeup.kofa', separators=separators,
            course_label='Admitted Course of Study:',
            course_link=self._getCourseAdmittedLink(view),
            dept=dept, faculty=faculty, colWidths=[7*cm, 10*cm]))

        # append two-column table of widgets of those fields defined in
        # two_columns_design_fields
        if len(self.two_columns_design_fields):
            fields = [
                field for field in self.form_fields
                    if not field.__name__ in self.column_two_fields and
                    field.__name__ in self.two_columns_design_fields]
            if fields:
                data.append(creator.getWidgetsTable(
                    fields, self.context, view, lang=portal_language,
                    domain='waeup.kofa', separators=separators,
                    twoDataCols=True))

        # append QR Code if without picture
        if not self.context.__parent__.with_picture and view is not None:
            data.append(Spacer(1, 5))
            url = view.url(self.context, 'application_slip.pdf')
            data_right = [[get_qrcode(url, width=70.0)]]
            table_right = Table(data_right,style=SLIP_STYLE)
            data.append(get_qrcode(url, width=70.0))

        # append login information
        note = None
        login_information = self._addLoginInformation()
        if not None in (self.note, login_information):
            note = self.note + login_information
        elif self.note:
            note = self.note
        elif login_information:
            note = login_information

        return creator.create_pdf(data, None, doc_title, note=note,
            topMargin=topMargin)