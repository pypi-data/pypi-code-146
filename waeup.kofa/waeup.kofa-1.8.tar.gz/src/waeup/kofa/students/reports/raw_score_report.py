## $Id: raw_score_report.py 16239 2020-09-17 07:16:01Z henrik $
##
## Copyright (C) 2013 Uli Fouquet & Henrik Bettermann
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
import grok
import textwrap
from zope.i18n import translate
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, getUtility
from zope.interface import implementer, Interface, Attribute
from waeup.kofa.interfaces import (
    IKofaUtils, GRADUATED,
    academic_sessions_vocab, registration_states_vocab)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.reports import IReport
from waeup.kofa.browser.pdf import get_signature_tables
from waeup.kofa.students.vocabularies import StudyLevelSource
from waeup.kofa.students.reports.level_report import LevelReportGeneratorPage
from waeup.kofa.students.reports.student_statistics import (
    StudentStatisticsReportPDFView)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Table, Spacer
from reportlab.platypus.flowables import Flowable
from waeup.kofa.reports import IReport, IReportGenerator
from waeup.kofa.reports import Report
from waeup.kofa.browser.interfaces import IPDFCreator

STYLE = getSampleStyleSheet()

class TTR(Flowable): #TableTextRotate
    '''Rotates a text in a table cell.'''

    def __init__(self, text):
        Flowable.__init__(self)
        self.text=text

    def draw(self):
        canvas = self.canv
        canvas.rotate(25)
        canvas.drawString( 0, -1, self.text)

def tbl_data_to_table(data, certcourses):
    col_names = (
            #'Student Id',
            'S/N',
            'Matric No.',
            'Name',
            )
    for certcourse in certcourses:
        course = certcourse.course
        if certcourse.course_category:
            col_names += (TTR('%s (%s, %s)' % (
                course.code, course.credits, certcourse.course_category)),)
        else:
            col_names += (TTR('%s (%s)' % (course.code, course.credits)),)
    table = [col_names]
    sn = 1
    for line in data:
        scores = tuple()
        composed_line = (sn,) + line[:-1]
        for certcourse in certcourses:
            result = line[-1].get(certcourse.course.code)
            if not result:
                scores += ('N/R',)
            else:
                scores += ('%s %s' % (result[0], result[1]),)
        composed_line += scores
        table.append(composed_line)
        sn += 1
    return table

class IRawScoreReport(IReport):

    session = Attribute('Session to report')
    level = Attribute('Level to report')
    faccode = Attribute('Faculty to report')
    depcode = Attribute('Department to report')
    certcode = Attribute('Certificate to report')
    creation_dt_string = Attribute('Human readable report creation datetime')

@implementer(IRawScoreReport)
class RawScoreReport(Report):
    data = None
    session = None
    level = None
    faccode = None
    depcode = None
    certcode = None
    note = ""
    signatures = None
    fontsize = 10

    @property
    def table_style(self):
        return [
            ('FONT', (0,0), (-1,-1), 'Helvetica', self.fontsize-2),
            ('VALIGN', (0, 1), (-1,-1), 'TOP'),
            #('FONT', (0,0), (0,-1), 'Helvetica-Bold', 8), # 1st column
            ('FONT', (0,0), (-1,0), 'Helvetica-Bold', self.fontsize-2), # 1st row
            #('FONT', (0,-1), (-1,-1), 'Helvetica-Bold', 8), # last row
            #('FONT', (-1,0), (-1,-1), 'Helvetica-Bold', 8), # last column
            ('ALIGN', (3,1), (-1,-1), 'CENTER'),
            ('ALIGN', (0,0), (0,-1), 'RIGHT'), # 1st column
            #('ALIGN', (6,0), (6,-1), 'LEFT'),
            ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
            ('BOX', (0,1), (-1,-1), 1, colors.black),
            ]

    @property
    def col_width(self):
        return [1*cm, 4*cm, 5*cm] + [1*cm] * len(self.certcourses)

    @property
    def title(self):
        return translate(_('Raw Score Report'))

    @property
    def right_footer(self):
        return self.title + ' - %s -' % self.session

    def _excluded(self, level_obj):
        """Some universities may add further conditions to exclude
        students from reports. These conditions can be customized in
        this function.
        """
        return False

    def _get_courses(self, faccode, depcode, certcode, session, level):
        """Method 1: Get certificate courses of a
        certain department/certificate at a certain level.
        """
        site = grok.getSite()
        certcourses = []
        department = site['faculties'][faccode][depcode]
        if certcode == 'all':
            for cert in department.certificates.values():
                for certcourse in cert.values():
                    if certcourse.level == level:
                        certcourses.append(certcourse)
        else:
            certificate = site['faculties'][faccode][depcode].certificates[certcode]
            for certcourse in certificate.values():
                if certcourse.level == level:
                    certcourses.append(certcourse)
        return certcourses

    def _get_students(self, faccode, depcode, certcode, session, level, certcourses):
        """Get students in a certain department/certificate who registered courses
        in a certain session at a certain level.

        Returns a list of student data tuples.
        """
        cat = queryUtility(ICatalog, name="students_catalog")
        if certcode == 'all':
            certcode = None
        result = cat.searchResults(
            depcode = (depcode, depcode), faccode = (faccode, faccode),
            certcode = (certcode, certcode)
            )
        table = []
        for stud in result:
            if not stud['studycourse'].has_key(str(level)):
                continue
            if stud.state == GRADUATED:
                continue
            level_obj = stud['studycourse'][str(level)]
            if level_obj.level_session != session:
                continue
            if self._excluded(level_obj):
                continue
            scores = dict()
            for ticket in level_obj.values():
                if ticket.code in [i.course.code for i in certcourses]:
                    if ticket.total_score is not None:
                        scores[ticket.code] = (ticket.total_score, ticket.grade)
                    else:
                        scores[ticket.code] = ('Nil', '')
            fullname = textwrap.fill(stud.display_fullname, 26)
            line = (
                    stud.matric_number,
                    fullname,
                    scores,
                    )
            table.append(line)
        return sorted(table, key=lambda value:value[0])

    def __init__(self, faccode, depcode, certcode, session, level,
                 author='System'):
        super(RawScoreReport, self).__init__(
            args=[faccode, depcode, certcode, session, level],
                  kwargs={'author':author})
        site = grok.getSite()
        self.studylevelsource = StudyLevelSource().factory
        self.portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        self.session = academic_sessions_vocab.getTerm(session).title
        self.levelcode = level
        self.sessioncode = session
        self.faccode = faccode
        self.depcode = depcode
        self.certcode = certcode
        self.factitle = site['faculties'][faccode].longtitle
        self.deptitle = site['faculties'][faccode][depcode].longtitle
        if self.certcode == 'all':
            self.certtitle = translate(
                _('All Certificates'), 'waeup.kofa',
                target_language=self.portal_language)
            self.level = translate(
                self.studylevelsource.getTitle(None, int(level)),
                'waeup.kofa', target_language=self.portal_language)
        else:
            certificate = site[
                'faculties'][faccode][depcode].certificates[certcode]
            self.certtitle = certificate.longtitle
            self.level = translate(
                self.studylevelsource.getTitle(certificate, int(level)),
                'waeup.kofa', target_language=self.portal_language)
        self.author = author
        self.creation_dt_string = self.creation_dt.astimezone(
            getUtility(IKofaUtils).tzinfo).strftime("%Y-%m-%d %H:%M:%S %Z")
        self.past_levels = range(int(level/100)*100, 0, -100)
        #self.course_codes = dict()
        self.certcourses = dict()
        self.data = dict()
        for level in self.past_levels:
            certcourses = self._get_courses(
                faccode, depcode, certcode, session, level)
            self.certcourses[level] = certcourses
            self.data[level] = self._get_students(
                faccode, depcode, certcode, session,
                self.levelcode, certcourses)

    def create_pdf(self, job_id):
        creator = getUtility(IPDFCreator, name='A3landscape')
        table_data = dict()
        for level in self.past_levels:
            table_data[level] = tbl_data_to_table(
                self.data[level], self.certcourses[level])
        pdf_data = [Paragraph('<font size=%s><b>%s - Report %s</b></font>'
                              % (self.fontsize, self.creation_dt_string, job_id),
                              STYLE["Normal"]),
                    Spacer(1, 12),]
        pdf_data += [Paragraph(
                    translate(
                        '<font size=${s}>${a}<br />${b}<br />${c}<br />'
                        'Session: ${d}<br />Level: ${e}</font>',
                        mapping = {'a':self.certtitle,
                                   'b':self.deptitle,
                                   'c':self.factitle,
                                   'd':self.session,
                                   'e':self.level,
                                   's':self.fontsize
                                   }),
                    STYLE["Normal"]),
                    ]

        for level in self.past_levels:
            pdf_data.append(Spacer(1, 20))
            pdf_data += [Paragraph('<font size=%s><b>Level %s Courses</b></font>'
                        % (self.fontsize, level), STYLE["Normal"]), Spacer(1, 20),]
            pdf_data += [
                Table(table_data[level],
                      style=self.table_style,
                      colWidths=self.col_width)]
        pdf_data.append(Spacer(1, 20))
        if self.signatures:
            signaturetables = get_signature_tables(
                self.signatures, landscape=True)
            pdf_data.append(signaturetables[0])

        pdf = creator.create_pdf(
            pdf_data, None, self.title, self.author,
            self.right_footer, note=self.note
            )
        return pdf

@implementer(IReportGenerator)
class RawScoreReportGenerator(grok.GlobalUtility):

    title = _('RAW Score Report')
    grok.name('raw_score_report')

    def generate(self, site, faccode=None, depcode=None, certcode=None,
                 session=None, level=None, author=None):
        result = RawScoreReport(faccode=faccode, depcode=depcode,
            certcode=certcode, session=session, level=level, author=author)
        return result

###############################################################
## Browser related stuff
##
## XXX: move to local browser module
###############################################################
from waeup.kofa.browser.layout import KofaPage
from waeup.kofa.interfaces import academic_sessions_vocab
from waeup.kofa.reports import get_generators
from waeup.kofa.browser.breadcrumbs import Breadcrumb
grok.templatedir('browser_templates')
class RawScoreReportGeneratorPage(LevelReportGeneratorPage):

    grok.context(RawScoreReportGenerator)

    label = _('Create raw score report')

class RawScoreReportPDFView(StudentStatisticsReportPDFView):

    grok.context(IRawScoreReport)
    grok.name('pdf')
    grok.require('waeup.handleReports')

    def _filename(self):
        return 'RawScoreReport_rno%s_%s.pdf' % (
            self.context.__name__,
            self.context.creation_dt_string)
