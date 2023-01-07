# -*- coding: utf-8 -*-
# :Project:   SoL -- The Match entity
# :Created:   gio 27 nov 2008 13:52:02 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008–2010, 2013–2015, 2016, 2018, 2020, 2021, 2023 Lele Gaifax
#

import logging

from sqlalchemy import Column, ForeignKey, Index, Sequence
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from itsdangerous import Signer

from ..i18n import gettext, translatable_string as _
from . import Base
from .domains import boolean_t, flag_t, intid_t, smallint_t
from .errors import OperationAborted


logger = logging.getLogger(__name__)


class Match(Base):
    """A single match.

    This table contains all the matches played in the various rounds
    of a tourney. A match may be between two different competitors
    or between a competitor and a *placeholder*, when the number of
    competitors is odd.
    """

    __tablename__ = 'matches'
    "Related table"

    @declared_attr
    def __table_args__(cls):
        return (Index('%s_board' % cls.__tablename__, 'idtourney', 'turn', 'board',
                      unique=True),
                Index('%s_c1_vs_c2' % cls.__tablename__,
                      'idtourney', 'idcompetitor1', 'idcompetitor2',
                      unique=True, sqlite_where=(cls.final == 0)))

    ## Columns

    idmatch = Column(
        intid_t, Sequence('gen_idmatch', optional=True),
        primary_key=True,
        nullable=False,
        info=dict(label=_('Match ID'),
                  hint=_('Unique ID of the match.')))
    """Primary key."""

    idtourney = Column(
        intid_t, ForeignKey('tourneys.idtourney', name='fk_match_tourney'),
        nullable=False,
        info=dict(label=_('Tourney ID'),
                  hint=_('ID of the tourney the match belongs to.')))
    """Related :py:class:`tourney <.Tourney>`'s ID."""

    turn = Column(
        smallint_t,
        nullable=False,
        info=dict(label=_('Round #'),
                  hint=_('Round number.')))
    """Round number of the match."""

    board = Column(
        smallint_t, nullable=False,
        info=dict(label=_('Board #'),
                  hint=_('Board where this match is played.')))
    """The number of the carromboard this match is played on."""

    final = Column(
        boolean_t,
        nullable=False,
        default=False,
        info=dict(label=_('Final'),
                  hint=_('Whether the match is a normal one or a final.')))
    """Whether the match is a normal one or a final."""

    idcompetitor1 = Column(
        intid_t, ForeignKey('competitors.idcompetitor', name='fk_match_competitor1'),
        nullable=False,
        info=dict(label=_('1st competitor ID'),
                  hint=_('ID of the first competitor.')))
    """First :py:class:`competitor <.Competitor>`'s ID."""

    idcompetitor2 = Column(
        intid_t, ForeignKey('competitors.idcompetitor', name='fk_match_competitor2'),
        info=dict(label=_('2nd competitor ID'),
                  hint=_('ID of the second competitor.')))
    """Second :py:class:`competitor <.Competitor>`'s ID (possibly None)."""

    breaker = Column(
        flag_t,
        info=dict(label=_('Breaker'),
                  hint=_("Which competitor started the match."),
                  dictionary={
                      '1': _('First competitor'),
                      '2': _('Second competitor')}))
    """Which competitor started the break."""

    score1 = Column(
        smallint_t,
        nullable=False,
        default=0,
        # TRANSLATORS: this is label for the "score of the first competitor" in the Matches
        # grid, keep it as compact as possible
        info=dict(label=_('S1'),
                  hint=_("Score of the first competitor."),
                  min=0, max=25))
    """Score of the first :py:class:`competitor <.Competitor>`."""

    score2 = Column(
        smallint_t,
        nullable=False,
        default=0,
        # TRANSLATORS: this is label for the "score of the second competitor" in the Matches
        # grid, keep it as compact as possible
        info=dict(label=_('S2'),
                  hint=_("Score of the second competitor."),
                  min=0, max=25))
    """Score of the second :py:class:`competitor <.Competitor>`."""

    ## Relations

    competitor1 = relationship(
        'Competitor',
        primaryjoin='Competitor.idcompetitor==Match.idcompetitor1')
    """First :py:class:`competitor <.Competitor>`"""

    competitor2 = relationship(
        'Competitor',
        primaryjoin='Competitor.idcompetitor==Match.idcompetitor2')
    """Second :py:class:`competitor <.Competitor>`
    (may be ``None``, the Phantom)."""

    boards = relationship('Board', backref='match',
                          cascade="all, delete-orphan",
                          order_by="Board.number")
    """List of :py:class:`boards <.Board>`."""

    def __repr__(self):  # pragma: no cover
        r = super().__repr__()
        r = r[:-1] + ' in turn %d of t%s: %d-%d>' % (self.turn,
                                                     repr(self.tourney)[2:-1],
                                                     self.score1, self.score2)
        return r

    def caption(self, html=None, localized=True):
        "A description of the match, made up with the description of each competitor."

        comp1 = self.competitor1.caption(html, localized, css_class='c1')
        if self.competitor2:
            comp2 = self.competitor2.caption(html, localized, css_class='c2')
        else:
            # TRANSLATORS: this is the name used for the "missing"
            # player, when there's an odd number of them
            comp2 = gettext('Phantom', just_subst=not localized)
        if html is None or html:
            if self.tourney.championship.playersperteam > 1:
                # TRANSLATORS: this is used to format the description
                # of a match for double events
                format = _('$comp1<br/><i>vs.</i><br/>$comp2')
            else:
                # TRANSLATORS: this is used to format the description
                # of a match for single events
                format = _('$comp1 <i>vs.</i> $comp2')
        else:
            format = _('$comp1 vs. $comp2')
        return gettext(format, mapping=dict(comp1=comp1, comp2=comp2),
                       just_subst=not localized)

    description = property(caption)

    @property
    def competitor1FullName(self):
        "Full name of the first :py:class:`competitor <.Competitor>`"
        c1 = self.competitor1
        return c1.description if c1 is not None else gettext('Player NOT assigned yet!')

    @property
    def competitor2FullName(self):
        "Full name of the second :py:class:`competitor <.Competitor>`"
        c2 = self.competitor2
        return c2.description if c2 is not None else gettext('Phantom')

    @property
    def competitor1Opponents(self):
        "List of competitors ID who played against the first competitor"
        c1 = self.competitor1
        return c1.getOpponentsPreceedingTurns(self.turn) if c1 is not None else []

    @property
    def competitor2Opponents(self):
        "List of competitors ID who played against the second competitor"
        c2 = self.competitor2
        return c2.getOpponentsPreceedingTurns(self.turn) if c2 is not None else []

    def check_update(self, fields):
        from .board import Board

        existing = len(self.boards)
        boardno = 1
        while boardno <= 10:
            if ((f'coins1_{boardno}' in fields
                 or f'coins2_{boardno}' in fields
                 or f'queen_{boardno}' in fields)):
                coins1 = fields.pop(f'coins1_{boardno}', None)
                coins2 = fields.pop(f'coins2_{boardno}', None)
                queen = fields.pop(f'queen_{boardno}', None)
                while existing < boardno:
                    existing += 1
                    self.boards.append(Board(number=existing))
                if not coins1 and not coins2 and not queen:
                    break
                if coins1 is not None:
                    self.boards[boardno - 1].coins1 = coins1
                if coins2 is not None:
                    self.boards[boardno - 1].coins2 = coins2
                self.boards[boardno - 1].queen = queen
            boardno += 1

    @property
    def isScored(self):
        "Tell whether the match has been compiled."

        return not (self.score1 == self.score2 == 0)

    def results(self):
        """Results of this match, comparing competitor' scores.

        :rtype: tuple
        :returns: winner, loser, netscore
        """

        if self.competitor2 is None:
            return self.competitor1, None, self.tourney.phantomscore
        elif self.score1 > self.score2:
            return self.competitor1, self.competitor2, self.score1 - self.score2
        elif self.score1 < self.score2:
            return self.competitor2, self.competitor1, self.score2 - self.score1
        elif self.score1 == self.score2 == 0:
            raise OperationAborted(
                _('How could match "$match" end without result?!?',
                  mapping=dict(match=self.description)))
        elif self.score1 == self.score2 and self.tourney.system == 'knockout':
            raise OperationAborted(
                _('How could match "$match" end with a draw in a knockout tourney?!?',
                  mapping=dict(match=self.description)))
        else:
            return self.competitor1, self.competitor2, 0

    def serialize(self, serializer, competitors):
        """Reduce a single match to a simple dictionary.

        :param serializer: a :py:class:`.Serializer` instance
        :param competitors: a mapping between competitor integer ID to its integer marker
        :rtype: dict
        :returns: a plain dictionary containing a flatified view of this match
        """

        simple = {}
        simple['competitor1'] = competitors[self.idcompetitor1]
        simple['competitor2'] = competitors[self.idcompetitor2]
        if self.breaker:
            simple['breaker'] = self.breaker
        simple['turn'] = self.turn
        simple['board'] = self.board
        if self.final:
            simple['final'] = self.final
        simple['score1'] = self.score1
        simple['score2'] = self.score2
        if self.boards:
            boards = simple['boards'] = []
            for b in self.boards:
                sb = b.serialize(serializer)
                boards.append(sb)
        if self.breaker:
            simple['breaker'] = self.breaker

        return simple

    def getEditCompetitorURL(self, request, cnum):
        settings = request.registry.settings
        s = Signer(settings['sol.signer_secret_key'])
        signed_match = s.sign('%d-%d' % (self.idmatch, cnum)).decode('ascii')
        return request.route_url('training_match_form', match=signed_match)

    def compute_partial_scores(self):
        "Enrich played boards with partial scores."

        total1 = total2 = self.partial_score1 = self.partial_score2 = 0
        if not self.boards:
            return
        for board in self.boards:
            score1 = board.coins1 or 0
            score2 = board.coins2 or 0
            if score1 == score2 == 0:
                if board.queen == '1':
                    score1 += 3 if total1 < 22 else 1
                elif board.queen == '2':
                    score2 += 3 if total2 < 22 else 1
            else:
                if board.queen == '1' and score1 > score2 and total1 < 22:
                    score1 += 3
                elif board.queen == '2' and score1 < score2 and total2 < 22:
                    score2 += 3
            board.score1 = score1
            board.score2 = score2
            total1 += score1
            total2 += score2
        self.partial_score1 = total1
        self.partial_score2 = total2
