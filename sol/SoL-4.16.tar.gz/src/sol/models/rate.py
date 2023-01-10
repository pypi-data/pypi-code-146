# -*- coding: utf-8 -*-
# :Project:   SoL -- The PlayerRating entity
# :Created:   ven 06 dic 2013 19:20:58 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2013, 2014, 2018, 2020 Lele Gaifax
#

from decimal import Decimal
import logging

from sqlalchemy import Column, ForeignKey, Index, Sequence
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from ..i18n import gettext, translatable_string as _
from . import Base
from .domains import date_t, intid_t, int_t, volatility_t


logger = logging.getLogger(__name__)


class Rate(Base):
    """The Glicko rating of a player."""

    __tablename__ = 'rates'
    "Related table"

    @declared_attr
    def __table_args__(cls):
        return (Index('%s_uk' % cls.__tablename__,
                      'idrating', 'idplayer', 'date',
                      unique=True),)

    ## Columns

    idrate = Column(
        intid_t, Sequence('gen_idrate', optional=True),
        primary_key=True,
        nullable=False,
        info=dict(label=_('Player rate ID'),
                  hint=_('Unique ID of the player rate.')))
    """Primary key."""

    idrating = Column(
        intid_t, ForeignKey('ratings.idrating', name='fk_rate_rating'),
        nullable=False,
        info=dict(label=_('Rating ID'),
                  hint=_('ID of the related rating.')))
    """Related rating's ID."""

    idplayer = Column(
        intid_t, ForeignKey('players.idplayer', name='fk_rate_player'),
        nullable=False,
        info=dict(label=_('Player ID'),
                  hint=_('ID of the related player.')))
    """Related :py:class:`player <.Player>` ID."""

    date = Column(
        date_t,
        nullable=False,
        info=dict(label=_('Date'),
                  hint=_('Date of the rating.')))
    """Rating date."""

    rate = Column(
        int_t,
        nullable=False,
        info=dict(label=_('Rate'),
                  hint=_('The value of Glicko rate.')))
    """The value of Glicko rating."""

    deviation = Column(
        int_t,
        nullable=False,
        info=dict(label=_('Deviation'),
                  hint=_('The value of Glicko deviation.')))
    """The value of Glicko deviation."""

    volatility = Column(
        volatility_t,
        nullable=False,
        info=dict(label=_('Volatility'),
                  hint=_('The value of the Glicko volatility.')))

    ## Relations

    player = relationship('Player')
    """The related :py:class:`player <.Player>`."""

    def __repr__(self):
        r = super().__repr__()
        r = r[:-1] + ': r=%s d=%s v=%s>' % (self.rate,
                                            self.deviation,
                                            self.volatility)
        return r

    def caption(self, html=None, localized=True):
        "A description of the rate."

        format = _('$player in $rating on $date')
        return gettext(format, just_subst=not localized,
                       mapping=dict(player=self.player.caption(html, localized),
                                    rating=self.rating.caption(html, localized),
                                    date=self.date.strftime(gettext('%m-%d-%Y'))))

    def update(self, data, missing_only=False):
        if 'volatility' in data:
            data['volatility'] = Decimal(data['volatility'])
        return super().update(data, missing_only)

    def serialize(self, serializer):
        """Reduce a single rate to a simple dictionary.

        :param serializer: a :py:class:`.Serializer` instance
        :rtype: dict
        :returns: a plain dictionary containing a flatified view of this rate
        """

        simple = {}
        simple['rating'] = serializer.addRating(self.rating)
        simple['player'] = serializer.addPlayer(self.player)
        simple['date'] = self.date
        simple['rate'] = self.rate
        simple['deviation'] = self.deviation
        simple['volatility'] = str(self.volatility)

        return simple
