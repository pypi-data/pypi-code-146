# -*- coding: utf-8 -*-
# :Project:   SoL -- Rating printout
# :Created:   lun 13 giu 2016 12:16:15 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018 Lele Gaifax
#

from babel.numbers import format_decimal

from reportlab.lib import colors
from reportlab.platypus import FrameBreak, NextPageTemplate, Paragraph
from reportlab.platypus.tables import Table

from sqlalchemy.orm.exc import NoResultFound

from ..i18n import translatable_string as _, gettext, ngettext, translator
from ..models import Rating
from ..models.errors import OperationAborted

from . import (
    caption_style,
    normal_style,
    rank_width,
    scores_width,
    subtitle_style,
    title_style,
    )
from .basic import BasicPrintout


class RatingRankingPrintout(BasicPrintout):
    "Glicko2 rating ranking."

    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        args = super().getArgumentsFromRequest(session, request)
        t = translator(request)

        id = request.matchdict['id']
        try:
            idrating = int(id)
        except ValueError:
            try:
                entity = session.query(Rating).filter_by(guid=id).one()
            except NoResultFound:
                raise OperationAborted(t(_('No rating with guid $id',
                                           mapping=dict(id=id))))
        else:
            entity = session.query(Rating).get(idrating)
            if entity is None:
                raise OperationAborted(t(_('No rating with id $id',
                                           mapping=dict(id=str(idrating)))))

        args.append(entity)
        return args

    def __init__(self, output, locale, rating):
        super().__init__(output, locale, 1)
        self.rating = rating
        self.ranking = rating.ranking

    def getLitURL(self, request):
        functional_testing = request.registry.settings['desktop.version'] == 'test'
        if not request.host.startswith('localhost') or functional_testing:
            return request.route_url('lit_rating', guid=self.rating.guid)

    @property
    def cache_max_age(self):
        "No cache."

        return 0

    def getSubTitle(self):
        return self.rating.description

    def getLeftHeader(self):
        howmany = len(self.rating.tourneys)
        if howmany == 0:  # pragma: nocover
            return gettext('No tourneys in the rating')
        else:
            return ngettext('%d tourney', '%d tourneys',
                            howmany) % howmany

    def getTitle(self):
        return gettext('Rating ranking')

    def getRightHeader(self):
        ts = self.rating.time_span
        if ts and ts[0]:
            # TRANSLATORS: this is a Python strftime() format, see
            # http://docs.python.org/3/library/time.html#time.strftime
            format = gettext('%m-%d-%Y')
            return gettext('Period from %s to %s') % (ts[0].strftime(format),
                                                      ts[1].strftime(format))
        else:  # pragma: nocover
            return ""

    def getCenterHeader(self):
        return ""

    def getCenterFooter(self):
        return self.getSubTitle()

    def getElements(self):
        yield Paragraph(self.getTitle(), title_style)
        yield Paragraph(self.getSubTitle(), subtitle_style)
        yield FrameBreak()
        yield NextPageTemplate('laterPages')

        rows = [('#',
                 gettext('Player'),
                 gettext('Rate'),
                 gettext('Deviation'),
                 gettext('Volatility'),
                 gettext('Tourneys'))]

        rows.extend((rank,
                     Paragraph(r[0].description, normal_style),
                     r[1], r[2], format_decimal(r[3], '0.00000', self.locale), r[4])
                    for rank, r in enumerate(self.ranking, 1))

        desc_width = self.doc.width - rank_width - scores_width*6
        style = [('SIZE', (0, 0), (-1, -1), caption_style.fontSize),
                 ('LEADING', (0, 0), (-1, -1), caption_style.leading),
                 ('FONT', (0, 0), (-1, 0), caption_style.fontName),
                 ('ALIGN', (2, 0), (-1, 0), 'RIGHT'),
                 ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                 ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
                 ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.black)]

        yield Table(rows, (rank_width, desc_width,
                           scores_width*1.5, scores_width*1.5, scores_width*1.5,
                           scores_width*1.5),
                    style=style)
