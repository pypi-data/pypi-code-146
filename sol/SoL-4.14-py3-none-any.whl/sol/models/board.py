# -*- coding: utf-8 -*-
# :Project:   SoL -- The Board entity
# :Created:   dom 19 apr 2020, 09:49:47
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2020 Lele Gaifax
#

import logging

from sqlalchemy import Column, ForeignKey, Index, Sequence
from sqlalchemy.ext.declarative import declared_attr

from ..i18n import translatable_string as _
from . import Base
from .domains import flag_t, intid_t, smallint_t


logger = logging.getLogger(__name__)


class Board(Base):
    """A single board.

    This table contains the detailed scores of a single match.

    Since entering such details is very time-consuming, historically and usually only the final
    scores of the match are assigned.

    .. note:: In *normal boards* `coinsX` is the number of carrommen of the opponent competitor
              still on the table at the end of the board; `coins1` and `coins2` are thus
              mutually exclusive (ie, one is zero) and the board is won by the competitor with
              a `coins` number greater than zero, with a score equal to that number plus
              possibly the points of the `queen` if pocketed by him.

              In *training boards* `coins1` and `coins2` are actually the *number of misses* of
              the respective competitors, in other words how many unsuccessful shots they made:
              the meaning is reversed, the board is won by the competitor with the lower
              number. The `queen` field has no meaning.
    """

    __tablename__ = 'boards'
    "Related table"

    @declared_attr
    def __table_args__(cls):
        return (Index('%s_number' % cls.__tablename__, 'idmatch', 'number', unique=True),)

    ## Columns

    idboard = Column(
        intid_t, Sequence('gen_idboard', optional=True),
        primary_key=True,
        nullable=False,
        info=dict(label=_('Board ID'),
                  hint=_('Unique ID of the board.')))
    """Primary key."""

    idmatch = Column(
        intid_t, ForeignKey('matches.idmatch', name='fk_board_match'),
        nullable=False,
        info=dict(label=_('Match ID'),
                  hint=_('ID of the match the board belongs to.')))
    """Related :py:class:`match <.Match>`'s ID."""

    number = Column(
        smallint_t,
        nullable=False,
        info=dict(label=_('Board #'),
                  hint=_('Board number.')))
    """Progressive number of the board."""

    coins1 = Column(
        smallint_t,
        nullable=True,
        info=dict(label=_('Coins 1'),
                  hint=_("Coins of the first competitor."),
                  min=0))
    """Coins of the first :py:class:`competitor <.Competitor>` in this board."""

    coins2 = Column(
        smallint_t,
        nullable=True,
        info=dict(label=_('Coins 2'),
                  hint=_("Coins of the second competitor."),
                  min=0))
    """Coins of the second :py:class:`competitor <.Competitor>` in this board."""

    queen = Column(
        flag_t,
        nullable=True,
        info=dict(label=_('Queen'),
                  hint=_('Which competitor pocketed the Queen, if any.'),
                  dictionary={
                      '1': _('First competitor'),
                      '2': _('Second competitor')}))
    """Which competitor pocketed the Queen, if any."""

    def __repr__(self):  # pragma: no cover
        if self.queen:
            queen = ', queen pocketed by competitor %s' % self.queen
        else:
            queen = ''
        match = self.match.caption(html=False, localized=False)
        return '<%s %d of match %s: %s-%s%s>' % (self.__class__.__name__, self.number,
                                                 match, self.coins1, self.coins2, queen)

    description = property(__repr__)

    def serialize(self, serializer):
        """Reduce a single board to a simple dictionary.

        :param serializer: a :py:class:`.Serializer` instance
        :returns: a plain dictionary containing a flatified view of this board
        """

        simple = {}
        simple['number'] = self.number
        if self.coins1 is not None:
            simple['coins1'] = self.coins1
        if self.coins2 is not None:
            simple['coins2'] = self.coins2
        if self.queen:
            simple['queen'] = self.queen
        return simple
