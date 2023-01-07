# -*- coding: utf-8 -*-
# :Project:   SoL -- Results printout
# :Created:   lun 13 giu 2016 11:46:23 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018, 2020 Lele Gaifax
#

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import CondPageBreak, Paragraph, Spacer, TableStyle
from reportlab.platypus.tables import Table

from ..i18n import translatable_string as _, gettext, translator
from ..models.errors import OperationAborted

from . import (
    BOLD_FONT_NAME,
    caption_style,
    heading_style,
    normal_style,
    rank_width,
    scores_width,
    )
from .basic import TourneyPrintout
from .utils import ordinalp


class ResultsPrintout(TourneyPrintout):
    "Results of the last turn."

    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        args = super().getArgumentsFromRequest(session, request)
        t = translator(request)
        kw = request.params
        if 'turn' in kw:
            if kw['turn'] == 'all':
                args.append(None)
            else:
                try:
                    args.append(int(kw['turn']))
                except ValueError:
                    raise OperationAborted(
                        t(_('Invalid turn: $turn',
                            mapping=dict(turn=repr(kw['turn'])))))
        else:
            args.append(args[1].rankedturn)

        return args

    def __init__(self, output, locale, tourney, turn):
        super().__init__(output, locale, tourney, 1)
        self.turn = turn

    def getLitURL(self, request):
        functional_testing = request.registry.settings['desktop.version'] == 'test'
        if not request.host.startswith('localhost') or functional_testing:
            otherargs = {}
            if self.turn:
                otherargs['_query'] = {'turn': self.turn}
            return request.route_url('lit_tourney', guid=self.tourney.guid, **otherargs)

    def getTurnDescription(self, turn, count):
        if count == 1:
            title = gettext('Result of final')
        elif count == 2:
            title = gettext('Results of semifinals')
        elif count == 4:
            title = gettext('Results of quarterfinals')
        elif count == 8:
            title = gettext('Results of pre-quarterfinals')
        elif count == 16:
            title = gettext('Results of 16th-finals')
        elif count == 32:
            title = gettext('Results of 32nd-finals')
        elif count == 64:
            title = gettext('Results of 64th-finals')
        else:
            title = gettext('Results %s round') % ordinalp(turn)
        return title

    def getSubTitle(self):
        if self.turn:
            matches = [m.final for m in self.tourney.matches if m.turn == self.turn]
            if self.tourney.system == 'knockout':
                return self.getTurnDescription(self.turn, len(matches))
            else:
                if matches[0]:
                    return gettext('Results %s final round') % ordinalp(self.turn)
                else:
                    return gettext('Results %s round') % ordinalp(self.turn)
        else:
            return gettext('All results')

    def getElements(self):
        yield from super().getElements()

        turn = self.turn

        phantom = gettext('Phantom')
        results = []
        for m in self.tourney.matches:
            if turn is None or m.turn == turn:
                c1 = m.competitor1.caption(nationality=True)
                c2 = m.competitor2.caption(nationality=True) if m.competitor2 else phantom
                s1 = m.score1
                s2 = m.score2
                if s1 > s2:
                    c1 = '<b>%s</b>' % c1
                elif s1 < s2:
                    c2 = '<b>%s</b>' % c2
                results.append((m.turn, m.board, c1, c2, s1, s2, m.final))

        if not results:
            return

        results.sort()

        if turn:
            yield from self.getSingleTurnElements(results)
        else:
            yield from self.getAllTurnElements(results)

    def getSingleTurnElements(self, results):
        from reportlab.pdfbase.pdfmetrics import stringWidth

        slash_w = stringWidth('/', normal_style.fontName, normal_style.fontSize)

        rows = [(gettext('#'), gettext('Match'), '', gettext('Result'), '')]

        rows.extend([(board,
                      Paragraph(c1, normal_style), Paragraph(c2, normal_style),
                      str(score1), '/', str(score2))
                     for (turn, board, c1, c2, score1, score2, final) in results])

        desc_width = (self.doc.width/self.columns*0.9
                      - rank_width - scores_width*2 - slash_w) / 2
        yield Table(rows,
                    (rank_width, desc_width, desc_width, scores_width, slash_w, scores_width),
                    style=TableStyle([
                        ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
                        ('SPAN', (1, 0), (2, 0)),
                        ('ALIGN', (1, 0), (2, 0), 'CENTER'),
                        ('SPAN', (-3, 0), (-1, 0)),
                        ('ALIGN', (-3, 0), (-1, 0), 'CENTER'),
                        ('ALIGN', (-3, 1), (-3, -1), 'RIGHT'),
                        ('ALIGN', (-2, 1), (-2, -1), 'CENTER'),
                        ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('FONT', (0, 0), (-1, 0), caption_style.fontName),
                        ('SIZE', (0, 0), (-1, 0), caption_style.fontSize),
                        ('LEADING', (0, 0), (-1, 0), caption_style.leading),
                        ('SIZE', (0, 1), (-1, -1), normal_style.fontSize),
                        ('LEADING', (0, 1), (-1, -1), normal_style.leading),
                        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)] + [
                            ('FONT',
                             (-3 if s1 > s2 else -1, r),
                             (-3 if s1 > s2 else -1, r),
                             BOLD_FONT_NAME)
                            for (r, (turn, board, c1, c2, s1, s2, final))
                            in enumerate(results, 1) if s1 != s2]))

    def getAllTurnElements(self, results):
        from itertools import groupby
        from operator import itemgetter

        key = itemgetter(0)
        for turn, res in groupby(results, key):
            yield CondPageBreak(4*cm)
            res = list(res)
            if self.tourney.system == 'knockout':
                title = Paragraph(self.getTurnDescription(turn, len(res)), heading_style)
            else:
                if res[0][6]:
                    title = Paragraph(gettext('Results %s final round') % ordinalp(turn),
                                      heading_style)
                else:
                    title = Paragraph(gettext('Results %s round') % ordinalp(turn),
                                      heading_style)
            yield title
            yield from self.getSingleTurnElements(res)
            yield Spacer(0, 0.4*cm)
