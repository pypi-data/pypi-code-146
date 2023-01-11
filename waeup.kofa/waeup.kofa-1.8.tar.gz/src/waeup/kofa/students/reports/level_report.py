## $Id: level_report.py 15968 2020-01-30 22:47:56Z henrik $
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
from waeup.kofa.utils.helpers import get_user_account
from waeup.kofa.browser.pdf import get_signature_tables
from waeup.kofa.students.vocabularies import StudyLevelSource
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
from waeup.kofa.browser.pdf import SMALL_PARA_STYLE

STYLE = getSampleStyleSheet()

class TTR(Flowable): #TableTextRotate
    '''Rotates a text in a table cell.'''

    def __init__(self, text):
        Flowable.__init__(self)
        self.text=text

    def draw(self):
        canvas = self.canv
        canvas.rotate(45)
        canvas.drawString( 0, -1, self.text)

    #def wrap(self,aW,aH):
    #    canv = self.canv
    #    return canv._leading, canv.stringWidth(self.text)

def tbl_data_to_table(data):
    result = []
    col_names = (
            'S/N',
            'Matric No.',
            translate(_('Student Name')),
            TTR(translate(_('Total Credits Taken'))),
            TTR(translate(_('Total Credits Passed'))),
            TTR(translate(_('GPA'))),
            translate(_('Courses Failed')),
            translate(_('Outstanding Courses')),
            TTR(translate(_('Cum. Credits Taken'))),
            TTR(translate(_('Cum. Credits Passed'))),
            TTR(translate(_('CGPA'))),
            TTR(translate(_('Remark'))))
    table = [col_names]
    sn = 1
    for line in data:
        # Underline mandatory (core) courses
        failed_courses = Paragraph(
            line[5].replace(
                'm_', '<u>').replace('_m', '</u>'), SMALL_PARA_STYLE)
        line = line[:5] + (failed_courses,) + line[6:]
        # Superscript in remarks (needed by AAUE)
        remark = Paragraph(
            line[10].replace(
                's_', '<super>').replace('_s', '</super>'), SMALL_PARA_STYLE)
        line = line[:10] + (remark,)
        line = (sn,) + line
        table.append(line)
        sn += 1
    return table

TABLE_STYLE = [
    ('FONT', (0,0), (-1,-1), 'Helvetica', 8),
    ('VALIGN', (0, 1), (-1,-1), 'TOP'),
    #('FONT', (0,0), (0,-1), 'Helvetica-Bold', 8), # 1st column
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8), # 1st row
    #('FONT', (0,-1), (-1,-1), 'Helvetica-Bold', 8), # last row
    #('FONT', (-1,0), (-1,-1), 'Helvetica-Bold', 8), # last column
    ('ALIGN', (3,1), (-1,-1), 'RIGHT'),
    ('ALIGN', (0,0), (0,-1), 'RIGHT'),
    ('ALIGN', (6,0), (6,-1), 'LEFT'),
    ('ALIGN', (7,0), (7,-1), 'LEFT'),
    ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
    ('BOX', (0,1), (-1,-1), 1, colors.black),
    ]

class ILevelReport(IReport):

    session = Attribute('Session to report')
    level = Attribute('Level to report')
    faccode = Attribute('Faculty to report')
    depcode = Attribute('Department to report')
    certcode = Attribute('Certificate to report')
    creation_dt_string = Attribute('Human readable report creation datetime')

@implementer(ILevelReport)
class LevelReport(Report):
    data = None
    session = None
    level = None
    faccode = None
    depcode = None
    certcode = None
    pdfcreator = 'landscape'
    note = None
    signatures = None

    @property
    def title(self):
        return translate(_('Level Report'))

    @property
    def right_footer(self):
        return self.title + ' - %s -' % self.session

    def _excluded(self, level_obj):
        """Some universities may add further conditions to exclude
        students from reports. These conditions can be customized in
        this function.
        """
        return False

    def _get_students(self, faccode, depcode, certcode, session, level):
        """Get students in a certain department, studying a certain programmen
        who registered courses in a certain session at a certain level.

        Returns a list of student data tuples.
        """
        site = grok.getSite()
        cat = queryUtility(ICatalog, name="students_catalog")
        if certcode == 'all':
            certcode = None
        result = cat.searchResults(
            depcode = (depcode, depcode), faccode = (faccode, faccode),
            certcode = (certcode, certcode)
            )
        table = []
        format_float = getUtility(IKofaUtils).format_float
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
            passed_params = level_obj.passed_params
            failed_courses = textwrap.fill(passed_params[4], 35)
            not_taken_courses = textwrap.fill(passed_params[5], 17)
            fullname = textwrap.fill(stud.display_fullname, 29)
            # This is a very special column requested by AAUE, Nigeria.
            # The 'remark' column remains empty in base package.
            remark = getattr(level_obj, 'remark', '')
            end_level = getattr(stud['studycourse'].certificate, 'end_level', None)
            credits_counted = level_obj.gpa_params[1]
            credits_passed = passed_params[2]
            level_gpa = format_float(level_obj.gpa_params[0], 3)
            cum_credits_taken = level_obj.cumulative_params[1]
            cum_credits_passed = level_obj.cumulative_params[4]
            if end_level and level >= end_level:
                cgpa = format_float(level_obj.cumulative_params[0], 2)
            else:
                cgpa = format_float(level_obj.cumulative_params[0], 3)
            if remark in ('FRNS', 'NER', 'NYV'):
                cgpa = ''
                if remark in ('NER', 'NYV'):
                    # hide all data (requestd by AAUE, Nigeria)
                    credits_counted = ''
                    credits_passed = ''
                    level_gpa = ''
                    failed_courses = ''
                    not_taken_courses = ''
                    cum_credits_taken = ''
                    cum_credits_passed = ''
            line = (
                    stud.matric_number,
                    fullname,
                    credits_counted,
                    credits_passed,
                    level_gpa,
                    failed_courses,
                    not_taken_courses,
                    cum_credits_taken,
                    cum_credits_passed,
                    cgpa,
                    remark,
                    )
            table.append(line)
        return sorted(table, key=lambda value:value[0])

    def __init__(self, faccode, depcode, certcode, session, level,
                 author='System'):
        super(LevelReport, self).__init__(
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
        self.data = self._get_students(faccode, depcode, certcode, session, level)

    def create_pdf(self, job_id):
        creator = getUtility(IPDFCreator, name=self.pdfcreator)
        table_data = tbl_data_to_table(self.data)
        #col_widths = [3.5*cm] * len(self.data[0])
        col_widths = [1*cm, 4*cm, 5*cm, 0.8*cm, 0.8*cm, 1*cm,
                      6*cm, 3*cm, 0.8*cm, 0.8*cm, 1*cm, 2*cm]
        pdf_data = [Paragraph('<b>%s - Report %s</b>'
                              % (self.creation_dt_string, job_id),
                              STYLE["Normal"]),
                    Spacer(1, 12),]
        pdf_data += [Paragraph(
                    translate(
                        '${a}<br />${b}<br />${c}<br />'
                        'Session: ${d}<br />Level: ${e}',
                        mapping = {'a':self.certtitle,
                                   'b':self.deptitle,
                                   'c':self.factitle,
                                   'd':self.session,
                                   'e':self.level,
                                   }),
                    STYLE["Normal"]),
                    Spacer(1, 12),]
        pdf_data += [
            Table(table_data, style=TABLE_STYLE, colWidths=col_widths)]

        pdf_data.append(Spacer(1, 40))
        if self.signatures:
            signaturetables = get_signature_tables(
                self.signatures, landscape=True)
            pdf_data.append(signaturetables[0])

        pdf = creator.create_pdf(
            pdf_data, None, self.title, self.author,
            self.right_footer, note = self.note
            )
        return pdf

@implementer(IReportGenerator)
class LevelReportGenerator(grok.GlobalUtility):

    title = _('Level Report')
    grok.name('level_report')

    def generate(self, site, faccode=None, depcode=None, certcode=None,
                 session=None, level=None, author=None):
        result = LevelReport(faccode=faccode, depcode=depcode,
                             certcode=certcode,
                             session=session, level=level, author=author)
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
class LevelReportGeneratorPage(KofaPage):

    grok.context(LevelReportGenerator)
    grok.name('index.html')
    grok.require('waeup.handleReports')

    label = _('Create level report')

    @property
    def generator_name(self):
        for name, gen in get_generators():
            if gen == self.context:
                return name
        return None

    def update(self, CREATE=None, faccode_depcode_certcode=None,
               session=None, level=None):
        self.parent_url = self.url(self.context.__parent__)
        self._set_session_values()
        self._set_level_values()
        try:
            local_roles = get_user_account(self.request).getLocalRoles()
        except AttributeError:  # Managers have no user account
            local_roles = {}
        lror = local_roles.get('waeup.local.ReportsOfficer', None)
        self._set_faccode_depcode_certcode_values(lror)
        if not faccode_depcode_certcode:
            self.flash(_('No certificate selected.'), type="warning")
            return
        if CREATE:
            # create a new report job for students by session
            faccode = faccode_depcode_certcode.split('_')[0]
            depcode = faccode_depcode_certcode.split('_')[1]
            certcode = faccode_depcode_certcode.split('_')[2]
            container = self.context.__parent__
            user_id = self.request.principal.id
            if level:
                level = int(level)
            if session:
                session = int(session)
            kw = dict(
                session=session,
                level=level,
                faccode=faccode,
                depcode=depcode,
                certcode=certcode)
            self.flash(_('New report is being created in background'))
            job_id = container.start_report_job(
                self.generator_name, user_id, kw=kw)
            ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
            grok.getSite().logger.info(
                '%s - report %s created: %s '
                '(faculty=%s, department=%s, certificate=%s, '
                'session=%s, level=%s)' % (
                ob_class, job_id, self.context.title, faccode, depcode,
                certcode, session, level))
            self.redirect(self.parent_url)
            return
        return

    def _set_session_values(self):
        vocab_terms = academic_sessions_vocab.by_value.values()
        self.sessions = [(x.title, x.token) for x in vocab_terms]
        return

    #def _set_level_values(self):
    #    vocab_terms = course_levels.by_value.values()
    #    self.levels = sorted([(x.title, x.token) for x in vocab_terms])
    #    return

    def _set_level_values(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        studylevelsource = StudyLevelSource().factory
        self.levels = []
        for code in studylevelsource.getValues(None):
            title = translate(studylevelsource.getTitle(None, code),
                'waeup.kofa', target_language=portal_language)
            self.levels.append((title, code))
        return

    def _set_faccode_depcode_certcode_values(self, lror):
        faccode_depcode_certcode = []
        faculties = grok.getSite()['faculties']
        if lror:
           for dep in lror:
                faccode_depcode_certcode.append(
                    (' All certificates -- %s, %s)'
                     %(dep.longtitle, dep.__parent__.longtitle),
                     '%s_%s_all'
                     %(dep.__parent__.code, dep.code)))
                for cert in dep.certificates.values():
                    faccode_depcode_certcode.append(
                        ('%s -- %s, %s)'
                         %(cert.longtitle, dep.longtitle, dep.__parent__.longtitle),
                         '%s_%s_%s'
                         %(dep.__parent__.code, dep.code, cert.code)))
        else:
            for fac in faculties.values():
                for dep in fac.values():
                    faccode_depcode_certcode.append(
                        (' All certificates -- %s, %s)'
                         %(dep.longtitle, fac.longtitle),
                         '%s_%s_all'
                         %(fac.code, dep.code)))
                    for cert in dep.certificates.values():
                        faccode_depcode_certcode.append(
                            ('%s -- %s, %s)'
                             %(cert.longtitle, dep.longtitle, fac.longtitle),
                             '%s_%s_%s'
                             %(fac.code, dep.code, cert.code)))
        self.faccode_depcode_certcode = sorted(
            faccode_depcode_certcode, key=lambda value: value[0])
        return

class LevelReportPDFView(StudentStatisticsReportPDFView):

    grok.context(ILevelReport)
    grok.name('pdf')
    grok.require('waeup.handleReports')

    def _filename(self):
        return 'LevelReport_rno%s_%s.pdf' % (
            self.context.__name__,
            self.context.creation_dt_string)
