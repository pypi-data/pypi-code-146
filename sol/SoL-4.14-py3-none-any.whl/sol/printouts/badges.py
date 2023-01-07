# -*- coding: utf-8 -*-
# :Project:   SoL -- Personal badges printout
# :Created:   lun 13 giu 2016 11:57:56 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018, 2019, 2020 Lele Gaifax
#

try:
    from importlib.metadata import metadata
except ImportError:
    from importlib_metadata import metadata

from babel.numbers import format_decimal
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm.exc import NoResultFound

from ..i18n import country_name, translatable_string as _, gettext, translator
from ..models import Tourney
from ..models.errors import OperationAborted

from . import (
    badgename_style,
    cardinfo_style,
    cardname_style,
    cardsmall_style,
    cardtitle_style,
    subtitle_style,
    )
from .utils import reduce_fontsize_to_fit_width


class BadgesPrintout(object):
    "Personal badges."

    emblems = '.'
    height = 5.4*cm
    width = 8.5*cm
    bottom_margin = 1*cm
    left_margin = 2*cm

    @classmethod
    def getArgumentsFromRequest(klass, session, request):
        t = translator(request)

        id = request.matchdict['id']
        try:
            idtourney = int(id)
        except ValueError:
            try:
                entity = session.query(Tourney).filter_by(guid=id).one()
            except NoResultFound:
                raise OperationAborted(t(_('No tourney with guid $id',
                                           mapping=dict(id=id))))
        else:
            entity = session.query(Tourney).get(idtourney)
            if entity is None:
                raise OperationAborted(t(_('No tourney with id $id',
                                           mapping=dict(id=str(idtourney)))))

        return [request.locale_name, entity]

    def __init__(self, output, locale, tourney):
        self.output = output
        self.locale = locale
        self.tourney = tourney

    @property
    def cache_max_age(self):
        "Cache for one year prized tourneys, no cache otherwise."

        if self.tourney.prized:
            return 60*60*24*365
        else:
            return 0

    def format_prize(self, prize):
        if self.tourney.championship.prizes != 'centesimal':
            return format_decimal(prize, '###0', self.locale)
        else:
            return format_decimal(prize, '###0.00', self.locale)

    def getPlayers(self):
        if self.tourney.prized:
            competitors = self.tourney.ranking
        else:
            competitors = self.tourney.competitors
        for r, c in enumerate(competitors, start=1):
            for p in (c.player1, c.player2, c.player3, c.player4):
                if p:
                    yield c, p, r

    def execute(self, request):
        c = self.canvas = canvas.Canvas(self.output)
        c.setAuthor('SoL %s' % metadata('sol')['Version'])
        c.setSubject(self.__class__.__name__)
        c.setTitle(gettext('Badges'))

        players = self.getPlayers()
        while self.drawOnePage(players):
            c.showPage()

        c.save()

    def drawOnePage(self, players):
        try:
            c, p, r = next(players)
        except StopIteration:
            return False
        first = True

        line = self.canvas.line
        for i in range(0, 6):
            y = self.bottom_margin + i * self.height
            line(5, y, 20, y)
            line(A4[0] - 5, y, A4[0] - 20, y)

        for i in range(0, 3):
            x = self.left_margin + i * self.width
            line(x, 5, x, 20)
            line(x, A4[1] - 5, x, A4[1] - 20)

        self.canvas.translate(self.left_margin, self.bottom_margin)
        for i in range(5):
            if not first:
                try:
                    c, p, r = next(players)
                except StopIteration:
                    return False
            else:
                first = False

            self.drawLeftSide(c, p, r)
            self.canvas.saveState()
            self.canvas.translate(self.width, 0)
            if self.tourney.prized:
                self.drawRightSide(c, p, r)
            else:
                try:
                    c, p, r = next(players)
                except StopIteration:
                    self.canvas.restoreState()
                    return False
                self.drawLeftSide(c, p, r)
            self.canvas.restoreState()
            self.canvas.translate(0, self.height)
        return True

    def drawLeftSide(self, competitor, player, rank):
        from os.path import exists, join

        c = self.canvas
        max_text_width = self.width
        center = self.width/2
        image_width = 0

        if self.tourney.championship.club.emblem:
            image = join(self.emblems, self.tourney.championship.club.emblem)
            if exists(image):
                image_width = self.width/5 * 2
                c.drawImage(image, 0, 0, image_width, self.height,
                            preserveAspectRatio=True)
                max_text_width -= image_width
                center = image_width + max_text_width/2

        style = reduce_fontsize_to_fit_width(self.tourney.description,
                                             max_text_width, cardtitle_style)[0]
        c.setFont(style.fontName, style.fontSize, style.leading)
        c.drawCentredString(center, self.height-0.8*cm, self.tourney.description)

        style = cardinfo_style
        c.setFont(style.fontName, style.fontSize, style.leading)
        c.drawCentredString(center, self.height-1.4*cm,
                            self.tourney.date.strftime(gettext('%m-%d-%Y')))

        style = reduce_fontsize_to_fit_width(self.tourney.championship.description,
                                             max_text_width, cardinfo_style)[0]
        c.setFont(style.fontName, style.fontSize, style.leading)
        c.drawCentredString(center, self.height-2*cm,
                            self.tourney.championship.description)

        if self.tourney.prized:
            style = subtitle_style
            c.setFont(style.fontName, style.fontSize, style.leading)
            c.drawCentredString(center, self.height-2.8*cm, str(rank))

            style = cardname_style
            c.setFont(style.fontName, style.fontSize, style.leading)
            if self.tourney.championship.prizes == 'asis':
                rx = image_width + 1.6*cm
                c.drawRightString(rx,        self.height-4.1*cm, gettext('Points:'))
                c.drawRightString(rx+0.8*cm, self.height-4.1*cm, str(competitor.points))
                c.setFont(style.fontName, style.fontSize-2, style.leading)
                rx = center + 1.7*cm
                c.drawRightString(rx,        self.height-3.9*cm, gettext('Bucholz:'))
                c.drawRightString(rx+0.6*cm, self.height-3.9*cm, str(competitor.bucholz))
                c.drawRightString(rx,        self.height-4.2*cm, gettext('Net score:'))
                c.drawRightString(rx+0.6*cm, self.height-4.2*cm, str(competitor.netscore))
            else:
                rx = image_width + 1.6*cm
                c.drawRightString(rx,        self.height-4.2*cm, gettext('Bounty:'))
                c.drawRightString(rx+1*cm, self.height-4.2*cm, str(competitor.prize))
                c.setFont(style.fontName, style.fontSize-2, style.leading)
                rx = center + 1.7*cm
                c.drawRightString(rx,        self.height-3.9*cm, gettext('Points:'))
                c.drawRightString(rx+0.6*cm, self.height-3.9*cm, str(competitor.points))
                c.drawRightString(rx,        self.height-4.2*cm, gettext('Bucholz:'))
                c.drawRightString(rx+0.6*cm, self.height-4.2*cm, str(competitor.bucholz))
                c.drawRightString(rx,        self.height-4.5*cm, gettext('Net score:'))
                c.drawRightString(rx+0.6*cm, self.height-4.5*cm, str(competitor.netscore))

        caption = player.caption(html=False)
        style = reduce_fontsize_to_fit_width(caption, max_text_width, badgename_style)[0]
        c.setFont(style.fontName, style.fontSize, style.leading)
        c.drawCentredString(center, self.height-3.5*cm, caption)

        style = cardname_style
        c.setFont(style.fontName, style.fontSize, style.leading)

        if competitor.player1Nationality:
            country = country_name(competitor.player1Nationality)
            flag = join(self.flags, competitor.player1Nationality+'.png')
            if exists(flag):
                c.drawRightString(center-0.1*cm, self.height-5.2*cm, country)
                c.drawImage(flag, center+0.1*cm, self.height-5.3*cm)
            else:
                c.drawCentredString(center, self.height-5.1*cm, country)

    def drawRightSide(self, competitor, player, rank):
        c = self.canvas

        def e(string, length):
            if c.stringWidth(string) > length:
                length -= c.stringWidth('…')
                while c.stringWidth(string) > length:
                    string = string[:-1]
                string += '…'
            return string

        c.setFont(cardsmall_style.fontName, cardsmall_style.fontSize, cardsmall_style.leading)

        c.drawCentredString(1.8*cm, self.height-1*cm, gettext('You met…'))
        c.drawString(0.3*cm, self.height-1.25*cm, gettext('Opponent'))

        # TRANSLATORS: this is the "score of this player" in the badge
        your = gettext('your')
        c.drawRightString(3*cm, self.height-1.25*cm, your)

        # TRANSLATORS: this is the "opponent score" in the badge
        his = gettext('his')
        c.drawRightString(3.4*cm, self.height-1.25*cm, his)

        pmatches = [m for m in self.tourney.matches
                    if m.idcompetitor1 == competitor.idcompetitor
                    or m.idcompetitor2 == competitor.idcompetitor]
        for i, m in enumerate(pmatches):
            if m.idcompetitor1 == competitor.idcompetitor:
                other = m.competitor2
                myscore = m.score1
                otherscore = m.score2
            elif m.idcompetitor2 == competitor.idcompetitor:
                other = m.competitor1
                myscore = m.score2
                otherscore = m.score1
            else:
                continue
            h = self.height-1.6*cm-i*0.3*cm
            c.drawString(0.3*cm, h,
                         other and e(other.caption(html=False), 2.3*cm)
                         or gettext('Phantom'))
            c.drawRightString(3*cm, h, str(myscore))
            c.drawRightString(3.4*cm, h, str(otherscore))

        c.drawCentredString(6.0*cm, self.height-1*cm,
                            gettext('Final ranking'))
        c.drawString(3.7*cm, self.height-1.25*cm,
                     gettext('Competitor'))
        if self.tourney.championship.prizes == 'asis':
            # TRANSLATORS: this is the points in the badge
            pts = gettext('pts')
            c.drawRightString(7.3*cm, self.height-1.25*cm, pts)
            # TRANSLATORS: this is the bucholz in the badge
            bch = gettext('bch')
            c.drawRightString(7.8*cm, self.height-1.25*cm, bch)
            # TRANSLATORS: this is the net score in the badge
            net = gettext('net')
            c.drawRightString(8.4*cm, self.height-1.25*cm, net)

            for i, ctor in enumerate(self.tourney.ranking):
                if i > 15:
                    break
                h = self.height-1.6*cm-i*0.22*cm
                c.drawRightString(3.8*cm, h, str(i+1))
                c.drawString(3.9*cm, h, e(ctor.caption(html=False), 3*cm))
                c.drawRightString(7.3*cm, h, str(ctor.points))
                c.drawRightString(7.8*cm, h, str(ctor.bucholz))
                c.drawRightString(8.4*cm, h, str(ctor.netscore))
        else:
            # TRANSLATORS: this is the points in the badge
            pts = gettext('pts')
            c.drawRightString(6.8*cm, self.height-1.25*cm, pts)
            # TRANSLATORS: this is the bucholz in the badge
            bch = gettext('bch')
            c.drawRightString(7.3*cm, self.height-1.25*cm, bch)
            # TRANSLATORS: this is the net score in the badge
            net = gettext('net')
            c.drawRightString(7.8*cm, self.height-1.25*cm, net)
            # TRANSLATORS: this is the prize in the badge
            prz = gettext('prz')
            c.drawRightString(8.5*cm, self.height-1.25*cm, prz)

            for i, ctor in enumerate(self.tourney.ranking):
                if i > 15:
                    break
                h = self.height-1.6*cm-i*0.22*cm
                c.drawRightString(3.7*cm, h, str(i+1))
                c.drawString(3.8*cm, h, e(ctor.caption(html=False), 2.6*cm))
                c.drawRightString(6.8*cm, h, str(ctor.points))
                c.drawRightString(7.3*cm, h, str(ctor.bucholz))
                c.drawRightString(7.8*cm, h, str(ctor.netscore))
                c.drawRightString(8.5*cm, h, self.format_prize(ctor.prize))
