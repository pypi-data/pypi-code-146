## $Id: student_statistics.py 15698 2019-10-22 10:54:34Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
    IKofaUtils,
    academic_sessions_vocab, registration_states_vocab)
from waeup.kofa.students.vocabularies import StudyLevelSource
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.reports import IReport

class IStudentStatisticsReport(IReport):

    session = Attribute('Session to report')
    level = Attribute('Level to report')
    mode = Attribute('Study modes group to report')
    creation_dt_string = Attribute('Human readable report creation datetime')

def get_student_stats(session, mode, level, breakdown):
    """Get students in a certain session, study mode and current level.

    Returns a table ordered by code (faculty or department, one per row) and
    registration state (cols). The result is a 3-tuple representing
    ((<PATHS>), (<STATES>), (<NUM_OF_STUDENTS>)). The
    (<NUM_OF_STUDENTS>) is an n-tuple with each entry containing the
    number of students found in that faculty/department and with the respective
    state.

    Sample result:

      >>> ((u'FAC1', u'FAC2'),
      ...  ('created', 'accepted', 'registered'),
      ...  ((12, 10, 1), (0, 5, 25)))

    This result means: there are 5 students in FAC2 in state
    'accepted' while 12 students in 'FAC1' are in state 'created'.
    """
    site = grok.getSite()
    states = tuple([x.value for x in registration_states_vocab])
    states = states + (u'Total',)
    if breakdown == 'faccode':
        paths = tuple(sorted([x for x in site['faculties'].keys()],
                                 key=lambda x: x.lower()))
    elif breakdown == 'depcode':
        faculties = site['faculties']
        deppaths = []
        for fac in faculties.values():
            for dep in fac.values():
                deppaths.append('%s/%s' % (fac.code, dep.code))
        paths = tuple(sorted([x for x in deppaths],
                                 key=lambda x: x.lower()))
    # XXX: Here we do _one_ query and then examine the single
    #   students. One could also do multiple queries and just look for
    #   the result length (not introspecting the delivered students
    #   further).
    cat = queryUtility(ICatalog, name="students_catalog")
    result = cat.searchResults(current_session=(session, session))
    table = [[0 for x in xrange(len(states))] for y in xrange(len(paths)+1)]
    mode_groups = getUtility(IKofaUtils).MODE_GROUPS
    for stud in result:
        if mode != 'All' and stud.current_mode \
            and stud.current_mode not in mode_groups[mode]:
            continue
        if level != 0 and stud.current_level != level:
            continue
        if getattr(stud, breakdown) is None:
            continue
        if breakdown == 'faccode':
            row_name = getattr(stud, 'faccode')
        elif breakdown == 'depcode':
            row_name = '%s/%s' % (
                getattr(stud, 'faccode'), getattr(stud, 'depcode'))
        row = paths.index(row_name)
        col = states.index(stud.state)
        table[row][col] += 1
        table[-1][col] += 1
        table[row][-1] += 1
        table[-1][-1] += 1
    # turn lists into tuples
    table = tuple([tuple(row) for row in table])

    paths = paths + (u'Total',)
    return (paths, states, table)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Table, Spacer
from waeup.kofa.reports import IReport, IReportGenerator
from waeup.kofa.reports import Report
from waeup.kofa.browser.interfaces import IPDFCreator

STYLE = getSampleStyleSheet()

def tbl_data_to_table(row_names, col_names, data):
    result = []
    new_col_names = []
    for name in col_names:
        new_col_names.append(name.replace(' ', '\n'))
    head = [''] + list(new_col_names)
    result = [head]
    for idx, row_name in enumerate(row_names):
        row = [row_name] + list(data[idx])
        result.append(row)
    return result

TABLE_STYLE = [
    ('FONT', (0,0), (-1,-1), 'Helvetica', 8),
    ('FONT', (0,0), (0,-1), 'Helvetica-Bold', 8),
    ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8),
    ('FONT', (0,-1), (-1,-1), 'Helvetica-Bold', 8),
    ('FONT', (-1,0), (-1,-1), 'Helvetica-Bold', 8),
    ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black),
    ('LINEAFTER', (-1,0), (-1,-1), 0.25, colors.black),
    ('LINEBEFORE', (-1,0), (-1,-1), 1.0, colors.black),
    #('LINEABOVE', (0,-1), (-1,-1), 1.0, colors.black),
    #('LINEABOVE', (0,0), (-1,0), 0.25, colors.black),
    ]

@implementer(IStudentStatisticsReport)
class StudentStatisticsReport(Report):
    data = None
    session = None
    mode = None
    pdfcreator = 'landscape'
    title = translate(_('Student Statistics'))

    @property
    def title(self):
        return translate(_('Student Statistics'))

    def __init__(self, session, mode, level, breakdown, author='System'):
        super(StudentStatisticsReport, self).__init__(
            args=[session, mode, breakdown], kwargs={'author':author})
        self.sessioncode = session
        self.levelcode = level
        self.studylevelsource = StudyLevelSource().factory
        self.portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        self.session = academic_sessions_vocab.getTerm(session).title
        self.mode = mode
        if level == 0:
            self.level = 'All levels'
        else:
            self.level = translate(
                self.studylevelsource.getTitle(None, int(level)),
                'waeup.kofa', target_language=self.portal_language)
        self.breakdown = breakdown
        self.author = author
        self.creation_dt_string = self.creation_dt.astimezone(
            getUtility(IKofaUtils).tzinfo).strftime("%Y-%m-%d %H:%M:%S %Z")
        self.data = get_student_stats(session, mode, level, breakdown)

    def create_pdf(self, job_id):
        creator = getUtility(IPDFCreator, name=self.pdfcreator)
        table_data = tbl_data_to_table(*self.data)
        col_widths = [None,] + [1.6*cm] * len(self.data[1]) + [None,]
        pdf_data = [Paragraph('<b>%s - Report %s</b>'
                              % (self.creation_dt_string, job_id),
                              STYLE["Normal"]),
                    Spacer(1, 12),]
        pdf_data += [Paragraph(
                    translate(
                        'Study Mode: ${a}<br />'
                        'Academic Session: ${b}<br />Level: ${c}<br />',
                        mapping = {'a':self.mode,
                                   'b':self.session,
                                   'c':self.level,
                                   }),
                    STYLE["Normal"]),
                    Spacer(1, 12),]
        pdf_data += [
            Table(table_data, style=TABLE_STYLE, colWidths=col_widths)]
        right_footer = translate(
            _('${a} Students - ${b} -',
            mapping = {'a':self.mode, 'b':self.session}))
        pdf = creator.create_pdf(
            pdf_data, None, self.title, self.author, right_footer
            )
        return pdf

@implementer(IReportGenerator)
class StudentStatisticsReportGenerator(grok.GlobalUtility):

    title = _('Student Statistics')
    grok.name('student_stats')

    def generate(
        self, site, session=None, mode=None,
        level=None, breakdown=None, author=None):
        result = StudentStatisticsReport(
            session=session, mode=mode, level=level,
            breakdown=breakdown, author=author)
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
class StudentStatisticsReportGeneratorPage(KofaPage):

    grok.context(StudentStatisticsReportGenerator)
    grok.name('index.html')
    grok.require('waeup.handleReports')

    label = _('Create student statistics report')

    @property
    def generator_name(self):
        for name, gen in get_generators():
            if gen == self.context:
                return name
        return None

    def update(
        self, CREATE=None, session=None, mode=None, level=None, breakdown=None):
        self.parent_url = self.url(self.context.__parent__)
        self._set_session_values()
        self._set_mode_values()
        self._set_level_values()
        self._set_breakdown_values()
        if CREATE and session:
            # create a new report job for students by session and level
            container = self.context.__parent__
            user_id = self.request.principal.id
            kw = dict(
                session=int(session),
                mode=mode,
                level=int(level),
                breakdown=breakdown)
            self.flash(_('New report is being created in background'))
            job_id = container.start_report_job(
                self.generator_name, user_id, kw=kw)
            ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
            grok.getSite().logger.info(
                '%s - report %s created: %s '
                '(session=%s, mode=%s, level=%s, breakdown=%s)' % (
                ob_class, job_id, self.context.title,
                session, mode, level, breakdown))
            self.redirect(self.parent_url)
            return
        return

    def _set_session_values(self):
        vocab_terms = academic_sessions_vocab.by_value.values()
        self.sessions = [(x.title, x.token) for x in vocab_terms]
        return

    def _set_mode_values(self):
        mode_groups = getUtility(IKofaUtils).MODE_GROUPS
        self.modes = sorted([(key, key) for key in mode_groups.keys()])
        return

    def _set_level_values(self):
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        studylevelsource = StudyLevelSource().factory
        self.levels = [(u'All', 0)]
        for code in studylevelsource.getValues(None):
            title = translate(studylevelsource.getTitle(None, code),
                'waeup.kofa', target_language=portal_language)
            self.levels.append((title, code))
        return

    def _set_breakdown_values(self):
        self.breakdowns = [(_('Faculties'), 'faccode'), (_('Departments'), 'depcode')]
        return

class StudentStatisticsReportPDFView(grok.View):

    grok.context(IStudentStatisticsReport)
    grok.name('pdf')
    grok.require('waeup.handleReports')

    def _filename(self):
        return 'StudentStatisticsReport_rno%s_%s.pdf' % (
            self.context.__name__,
            self.context.creation_dt_string)

    def render(self):
        filename = self._filename().replace(
            '/', '_').replace(' ','_').replace(':', '-')
        self.response.setHeader(
            'Content-Type', 'application/pdf')
        self.response.setHeader(
            'Content-Disposition:', 'attachment; filename="%s' % filename)
        pdf_stream = self.context.create_pdf(self.context.__name__)
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        grok.getSite().logger.info('%s - report %s downloaded: %s' % (
            ob_class, self.context.__name__, filename))
        return pdf_stream
