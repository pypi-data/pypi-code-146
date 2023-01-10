# -*- coding: utf-8 -*-
# :Project:   SoL -- Ranking printout
# :Created:   lun 13 giu 2016 11:41:01 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018, 2020 Lele Gaifax
#

from babel.numbers import format_decimal

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import FrameBreak, NextPageTemplate, Paragraph, TableStyle
from reportlab.platypus.tables import Table

from sqlalchemy.orm.exc import NoResultFound

from ..i18n import translatable_string as _, gettext, ngettext, translator
from ..models import Championship
from ..models.errors import OperationAborted

from . import caption_style, subtitle_style, title_style
from .basic import BasicPrintout
from .utils import reduce_fontsize_to_fit_width


class ChampionshipRankingPrintout(BasicPrintout):
    "Championship ranking."

    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        args = super().getArgumentsFromRequest(session, request)
        t = translator(request)

        id = request.matchdict['id']
        try:
            idchampionship = int(id)
        except ValueError:
            try:
                entity = session.query(Championship).filter_by(guid=id).one()
            except NoResultFound:
                raise OperationAborted(t(_('No championship with guid $id',
                                           mapping=dict(id=id))))
        else:
            entity = session.query(Championship).get(idchampionship)
            if entity is None:
                raise OperationAborted(t(_('No championship with id $id',
                                           mapping=dict(id=str(idchampionship)))))

        args.append(entity)
        return args

    def __init__(self, output, locale, arg):
        super().__init__(output, locale, 1)
        self.setup(arg)

    def getLitURL(self, request):
        functional_testing = request.registry.settings['desktop.version'] == 'test'
        if not request.host.startswith('localhost') or functional_testing:
            return request.route_url('lit_championship', guid=self.championship.guid)

    @property
    def cache_max_age(self):
        "Cache for one year closed championships, no cache otherwise."

        if self.championship.closed:
            return 60*60*24*365
        else:
            return 0

    def setup(self, championship):
        self.championship = championship
        self.dates, self.ranking = championship.ranking()
        if len(self.dates) > 5:
            self.pagesize = landscape(A4)

    def getLeftHeader(self):
        return self.getSubTitle()

    def getRightHeader(self):
        return self.championship.club.description

    def getCenterHeader(self):
        if self.championship.skipworstprizes:
            swp = self.championship.skipworstprizes
            return ngettext('Ignoring %d worst result',
                            'Ignoring %d worst results',
                            swp) % swp
        else:
            return ""

    def getTitle(self):
        return self.championship.description

    def getSubTitle(self):
        howmany = len(self.dates)
        if howmany == 0:
            return gettext('No prized tourneys in the championship')
        else:
            return ngettext('%d tourney', '%d tourneys',
                            howmany) % howmany

    def getElements(self):
        from sol.models.utils import njoin

        title = self.getTitle()
        tstyle, ststyle = reduce_fontsize_to_fit_width(title, self.title_width - 1*cm,
                                                       title_style, subtitle_style)

        yield Paragraph(title, tstyle)
        yield Paragraph(self.getSubTitle(), ststyle)
        yield FrameBreak()
        yield NextPageTemplate('laterPages')

        if not self.ranking:
            return

        header = self.createTableHeader()

        style = [('SIZE', (0, 0), (-1, -1), caption_style.fontSize),
                 ('LEADING', (0, 0), (-1, -1), caption_style.leading),
                 ('FONT', (0, 0), (-1, 0), caption_style.fontName),
                 ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
                 ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
                 ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.black)]
        header.append(gettext('Total'))
        rows = [header]

        for i, c in enumerate(self.ranking):
            row = [i+1]
            row.append(njoin(c[0]))
            for col, s in enumerate(c[2]):
                # If we have the skipped prizes and the current
                # prize is one of those, print it in light gray
                if len(c) > 4 and c[4] and s in c[4]:
                    if s:
                        style.append(('TEXTCOLOR',
                                      (col+2, i+1), (col+2, i+1),
                                      colors.lightgrey))
                    c[4].remove(s)
                row.append(self.format_prize(s) if s else '')
            row.append(self.format_prize(c[1]))
            rows.append(row)
        yield Table(rows, style=TableStyle(style))

    def createTableHeader(self):
        header = ['#']
        if self.championship.playersperteam > 1:
            header.append(gettext('Team'))
        else:
            header.append(gettext('Player'))

        for date, desc, g in self.dates:
            # TRANSLATORS: this is a Python strftime() format, see
            # http://docs.python.org/3/library/time.html#time.strftime
            header.append(date.strftime(gettext('%m-%d-%y')))
        return header

    def format_prize(self, prize):
        if self.championship.prizes != 'centesimal':
            return format_decimal(prize, '###0', self.locale)
        else:
            return format_decimal(prize, '###0.00', self.locale)
