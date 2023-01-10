# -*- coding: utf-8 -*-
# :Project:   SoL -- Track players merges
# :Created:   sab 21 dic 2013 13:12:36 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2014, 2018, 2020 Lele Gaifax
#

import logging

from sqlalchemy import Column, ForeignKey, Index, Sequence
from sqlalchemy.ext.declarative import declared_attr

from ..i18n import translatable_string as _
from . import Base, GloballyUnique
from .domains import intid_t, name_t, nickname_t


logger = logging.getLogger(__name__)


class MergedPlayer(GloballyUnique, Base):
    """A player who has been merged into another."""

    __tablename__ = 'mergedplayers'
    "Related table."

    @declared_attr
    def __table_args__(cls):
        return (GloballyUnique.__table_args__(cls) +
                (Index('%s_names' % cls.__tablename__,
                       'lastname', 'firstname', 'nickname'),
                 Index('%s_idplayer' % cls.__tablename__,
                       'idplayer')))

    ## Columns

    idmergedplayer = Column(
        intid_t, Sequence('gen_idmergedplayer', optional=True),
        primary_key=True,
        nullable=False,
        info=dict(label=_('Merge ID'),
                  hint=_('Unique ID of the merged player.')))
    """Primary key."""

    firstname = Column(
        name_t,
        nullable=False,
        default='',
        info=dict(label=_('First name'),
                  hint=_('First name of the player.')))
    """Player's first name."""

    lastname = Column(
        name_t,
        nullable=False,
        default='',
        info=dict(label=_('Last name'),
                  hint=_('Last name of the player.')))
    """Player's last name."""

    nickname = Column(
        nickname_t,
        nullable=False,
        default='',
        info=dict(label=_('Nickname'),
                  hint=_('Nickname of the player, for'
                         ' login and to disambiguate homonyms.')))
    """Player's nickname, used also for login purposes."""

    idplayer = Column(
        intid_t, ForeignKey('players.idplayer', name='fk_mergedplayer_player'),
        nullable=False,
        info=dict(label=_('Player ID'),
                  hint=_('ID of the target player.')))
    """Target :py:class:`player <.Player>`'s ID."""

    def caption(self, html=None, localized=True):
        "Description of the player, made up concatenating his names."

        if self.lastname:
            oldname = "%s %s" % (self.lastname, self.firstname)
        else:  # pragma: nocover
            oldname = self.guid

        newname = self.player.caption(html, localized=localized)
        return '%s -> %s' % (oldname, newname)

    description = property(caption)
