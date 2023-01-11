## $Id: session_results_presentation.py 14917 2017-11-30 11:19:10Z henrik $
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
from zope.i18n import translate
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, getUtility
from zope.interface import implementer, Interface, Attribute
from waeup.kofa.interfaces import (
    IKofaUtils, GRADUATED,
    academic_sessions_vocab, registration_states_vocab)
from waeup.kofa.students.vocabularies import StudyLevelSource
from waeup.kofa.students.interfaces import IStudentsUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.browser.pdf import get_signature_tables
from waeup.kofa.reports import IReport
from waeup.kofa.students.reports.level_report import (
    ILevelReport, LevelReportGeneratorPage)
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

TABLE_STYLE = [
    ('FONT', (0,0), (-1,-1), 'Helvetica', 8),
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8), # 1st row
    #('ALIGN', (3,1), (-1,-1), 'RIGHT'),
    #('ALIGN', (1,0), (1,-1), 'LEFT'),
    #('ALIGN', (2,0), (2,-1), 'LEFT'),
    #('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
    #('BOX', (0,1), (-1,-1), 1, colors.black),
    ]

SUMMARY_STYLE = [
    ('ALIGN', (3,1), (-1,-1), 'RIGHT'),
    ]

class ISessionResultsPresentation(ILevelReport):
    """ Same interface as for level session results presentation.
    """

@implementer(ISessionResultsPresentation)
class SessionResultsPresentation(Report):
    data = None
    session = None
    level = None
    faccode = None
    depcode = None
    certcode = None
    pdfcreator = ''
    signatures = None
    introduction = ''

    @property
    def title(self):
        return translate(_('Presentation of Session Results'))

    @property
    def right_footer(self):
        return self.title + ' - %s -' % self.session

    note = None

    def _excluded(self, level_obj):
        """Some universities may add further conditions to exclude
        students from reports. These conditions can be customized in
        this function.
        """
        return False

    def _get_students(self, faccode, depcode, certcode, session, level=None):
        """Get students in a certain department, studying a certain programmen
        who registered courses in a certain session at a certain level.

        Returns a list of lists of student data tuples.
        """
        site = grok.getSite()
        cat = queryUtility(ICatalog, name="students_catalog")
        if certcode == 'all':
            certcode = None
        result = cat.searchResults(
            depcode = (depcode, depcode), faccode = (faccode, faccode),
            certcode = (certcode, certcode)
            )
        students_utils = getUtility(IStudentsUtils)
        table = list()
        for i in range(len(students_utils.GPABoundaries(
                faccode=faccode, depcode=depcode,
                certcode=certcode))+1):
            # The last list is reserved for students with more than one
            # level in the same session.
            table.append([])
        for stud in result:
            if stud.state == GRADUATED:
                continue
            line = (stud.student_id,
                    stud.matric_number,
                    stud.display_fullname,
                    )
            if level != 0:
                if not stud['studycourse'].has_key(str(level)):
                    continue
                level_obj = stud['studycourse'][str(level)]
                if level_obj.level_session != session:
                    continue
                if self._excluded(level_obj):
                    continue
            else:
                itemcount = 0
                for item in stud['studycourse'].values():
                    if item.level_session == session:
                        level_obj = item
                        itemcount += 1
                if itemcount == 0:
                    # No level registered in this session
                    continue
                if itemcount > 1:
                    # Error: more than one level registered in this session
                    table[len(students_utils.GPABoundaries(
                        faccode=faccode, depcode=depcode,
                        certcode=certcode))].append(line)
                    continue
            gpaclass = students_utils.getDegreeClassNumber(level_obj)
            table[gpaclass].append(line)
            for i in range(len(students_utils.GPABoundaries(
                    faccode=faccode, depcode=depcode,
                    certcode=certcode))+1):
                if len(table[i]):
                    table[i] = sorted([value for value in table[i]],
                        key=lambda value: value[2])
        return table

    def __init__(self, faccode, depcode, certcode, session, level,
                 author='System'):
        super(SessionResultsPresentation, self).__init__(
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
        else:
            certificate = site[
                'faculties'][faccode][depcode].certificates[certcode]
            self.certtitle = certificate.longtitle
        if level == 0:
            self.level = translate(_('all levels'))
        else:
            if self.certcode == 'all':
                self.level = translate(
                    self.studylevelsource.getTitle(None, int(level)),
                    'waeup.kofa', target_language=self.portal_language)
            else:
                self.level = translate(
                    self.studylevelsource.getTitle(certificate, int(level)),
                    'waeup.kofa', target_language=self.portal_language)
        self.author = author
        self.creation_dt_string = self.creation_dt.astimezone(
            getUtility(IKofaUtils).tzinfo).strftime("%Y-%m-%d %H:%M:%S %Z")
        self.data = self._get_students(faccode, depcode, certcode, session, level)

    def create_pdf(self, job_id):
        creator = getUtility(IPDFCreator, name=self.pdfcreator)
        #col_widths = [2*cm, 4*cm, 5*cm, 0.8*cm, 0.8*cm, 0.8*cm, 6*cm, ]
        pdf_data = [Paragraph('<b>%s - Report %s</b>'
                              % (self.creation_dt_string, job_id),
                              STYLE["Normal"]),
                    Spacer(1, 12),]
        if self.introduction:
            pdf_data += [Paragraph(self.introduction,
                         STYLE["Normal"]), Spacer(1, 12)]
        pdf_data += [Paragraph(
                    translate(
                        '${a}<br />${b}<br />${c}<br />Session: ${d}<br />'
                        'Level: ${e}',
                        mapping = {'a':self.certtitle,
                                   'b':self.deptitle,
                                   'c':self.factitle,
                                   'd':self.session,
                                   'e':self.level,
                                   }),
                    STYLE["Normal"]),
                    ]
        students_utils = getUtility(IStudentsUtils)
        # Print classes in reverse order
        for gpa_class in range(len(students_utils.GPABoundaries(
                faccode=self.faccode, depcode=self.depcode,
                certcode=self.certcode))-1,-1,-1):
            pdf_data.append(Spacer(1, 20))
            gpa_class_name = students_utils.GPABoundaries(
                faccode=self.faccode, depcode=self.depcode,
                certcode=self.certcode)[gpa_class][1]
            pdf_data += [Paragraph('<strong>%s</strong>' % gpa_class_name,
                         STYLE["Normal"])]
            pdf_data.append(Spacer(1, 6))
            if len(self.data[gpa_class]):
                sns = range(len(self.data[gpa_class]))
                gpa_class_data = [(i+1,) + self.data[gpa_class][i] for i in sns]
            else:
                gpa_class_data = [('', '', '- Nil -', '')]
            table_data = [('S/N', 'Student Id', 'Matric No.',
                translate(_('Student Name')))] + gpa_class_data
            pdf_data += [Table(table_data, style=TABLE_STYLE)]    #, colWidths=col_widths)]
        if self.data[-1]:
            pdf_data.append(Spacer(1, 20))
            pdf_data += [
                Paragraph(
                    '<strong>Students with erroneous data</strong>', STYLE["Normal"])]
            pdf_data.append(Spacer(1, 10))
            table_data = [('Student Id', 'Matric No.', 'Name')] + self.data[-1]
            pdf_data += [Table(table_data, style=TABLE_STYLE)]
        pdf_data.append(Spacer(1, 20))
        pdf_data += [Paragraph('<strong>Summary</strong>', STYLE["Normal"])]
        pdf_data.append(Spacer(1, 10))
        total_count = 0
        table_data = list()
        for gpa_class in range(len(students_utils.GPABoundaries(
                faccode=self.faccode, depcode=self.depcode,
                certcode=self.certcode))-1,-1,-1):
            gpa_class_name = students_utils.GPABoundaries(
                faccode=self.faccode, depcode=self.depcode,
                certcode=self.certcode)[gpa_class][1]
            gpa_count = len(self.data[gpa_class])
            total_count += gpa_count
            table_data += [(gpa_class_name + ':', '%02d' % gpa_count)]
            #pdf_data += [Paragraph('%s: %s'
            #             % (gpa_class_name, gpa_count), STYLE["Normal"])]
            pass
        #pdf_data += [Paragraph('Total: %s' % (total_count), STYLE["Normal"])]
        table_data += [('Total:', '%02d' % total_count)]
        pdf_data += [Table(table_data, style=SUMMARY_STYLE, hAlign='LEFT')]

        pdf_data.append(Spacer(1, 40))
        if self.signatures:
            signaturetables = get_signature_tables(self.signatures)
            pdf_data.append(signaturetables[0])

        pdf = creator.create_pdf(
            pdf_data, None, self.title, self.author,
            self.right_footer, note = self.note
            )
        return pdf

@implementer(IReportGenerator)
class SessionResultsPresentationGenerator(grok.GlobalUtility):

    title = _('Session Results Presentation')
    grok.name('session_results_presentation')

    def generate(self, site, faccode=None, depcode=None, certcode=None,
                 session=None, level=None, author=None):
        result = SessionResultsPresentation(faccode=faccode, depcode=depcode,
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
class SessionResultsPresentationGeneratorPage(LevelReportGeneratorPage):

    grok.context(SessionResultsPresentationGenerator)
    grok.template('levelreportgeneratorpage')
    label = _('Create session results presentation')

    def _set_level_values(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        studylevelsource = StudyLevelSource().factory
        self.levels = [(u'All levels', 0)]
        for code in studylevelsource.getValues(None):
            title = translate(studylevelsource.getTitle(None, code),
                'waeup.kofa', target_language=portal_language)
            self.levels.append((title, code))
        return

class SessionResultsPresentationPDFView(StudentStatisticsReportPDFView):

    grok.context(ISessionResultsPresentation)
    grok.name('pdf')
    grok.require('waeup.handleReports')

    def _filename(self):
        return 'SessionResultsPresentation_rno%s_%s.pdf' % (
            self.context.__name__,
            self.context.creation_dt_string)
