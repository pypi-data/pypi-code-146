# -*- coding: utf-8 -*-
# :Project:   SoL -- The Club entity
# :Created:   gio 27 nov 2008 13:49:40 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2013, 2014, 2016, 2018, 2020 Lele Gaifax
#

import logging

from sqlalchemy import Column, ForeignKey, Index, Table, Sequence, func, or_, select
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import object_session, relationship

from ..i18n import country_name, translatable_string as _
from . import Base, GloballyUnique
from .domains import (
    boolean_t,
    code_t,
    description_t,
    email_t,
    filename_t,
    intid_t,
    nationality_t,
    url_t,
    )
from .errors import OperationAborted
from .utils import normalize


logger = logging.getLogger(__name__)


clubusers = Table(
    'clubusers', Base.metadata,
    Column(
        'idclub',
        intid_t,
        ForeignKey('clubs.idclub', name='fk_clubuser_club', ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        info=dict(label=_('Club ID'),
                  hint=_('ID of the club.'))),
    Column(
        'iduser',
        intid_t,
        ForeignKey('users.iduser', name='fk_clubuser_user', ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
        index=True,
        info=dict(label=_('User ID'),
                  hint=_('ID of the user.'))))


class Club(GloballyUnique, Base):
    """A club, which organizes championships of tourneys."""

    __tablename__ = 'clubs'
    "Related table"

    @declared_attr
    def __table_args__(cls):
        return (GloballyUnique.__table_args__(cls) +
                (Index('%s_uk' % cls.__tablename__, 'description',
                       unique=True),))

    ## Columns

    idclub = Column(
        intid_t, Sequence('gen_idclub', optional=True),
        primary_key=True,
        nullable=False,
        info=dict(label=_('Club ID'),
                  hint=_('Unique ID of the club.')))
    """Primary key."""

    idrating = Column(
        intid_t, ForeignKey('ratings.idrating', use_alter=True, name='fk_club_rating',
                            ondelete="SET NULL"),
        nullable=True,
        info=dict(label=_('Rating ID'),
                  hint=_('ID of the default rating used by championships organized by this'
                         ' club.')))
    """Possible :py:class:`rating <.Rating>` ID, used as default value
    for the corresponding field when creating a new championship."""

    idowner = Column(
        intid_t, ForeignKey('users.iduser', use_alter=True, name="fk_club_owner",
                            ondelete="SET NULL"),
        info=dict(label=_('Owner ID'),
                  hint=_('ID of the user that is responsible for this record.')))
    """ID of the :py:class:`user <.User>` that is responsible for this record."""

    description = Column(
        description_t,
        nullable=False,
        info=dict(label=_('Description'),
                  hint=_('Description of the club.')))
    """Description of the club."""

    emblem = Column(
        filename_t,
        info=dict(label=_('Emblem'),
                  hint=_('File name of the PNG, JPG or GIF'
                         ' logo of the club.')))
    """Logo of the club, used on badges.

    This is just the filename, referencing a picture inside the
    ``sol.emblems_dir`` directory.
    """

    nationality = Column(
        nationality_t,
        info=dict(label=_('Country'),
                  hint=_('Nationality of the club.')))
    """`ISO country code <http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3>`_
    to compute national rankings."""

    couplings = Column(
        code_t,
        default='serial',
        info=dict(label=_('Pairings'),
                  hint=_('Default method used to pair competitors at each round.'),
                  dictionary=dict(serial=_('Ranking order'),
                                  dazed=_('Cross ranking order'),
                                  staggered=_('Staggered ranking order'))))
    """Kind of pairing method used to build next round, used as default value
    for the corresponding field when creating a new championship."""

    prizes = Column(
        code_t,
        nullable=False,
        default='fixed',
        info=dict(label=_('Prizes'),
                  hint=_('Default method used to assign final prizes.'),
                  dictionary=dict(
                      asis=_('Simple tourneys, no special prizes'),
                      fixed=_('Fixed prizes: 18,16,14,13…'),
                      fixed40=_('Fixed prizes: 1000,900,800,750…'),
                      millesimal=_('Classic millesimal prizes'))))
    """Kind of prize-giving, used as default value for the corresponding
    field when creating a new championship.

    This is used to determine which method will be used to assign
    final prizes. It may be:

    `asis`
      means that the final prize is the same as the competitor's points;

    `fixed`
      means the usual way, that is 18 points to the winner, 16 to the
      second, 14 to the third, 13 to the fourth, …, 1 point to the
      16th, 0 points after that;

    `fixed40`
      similar to `fixed`, but applied to best fourty scores starting
      from 1000:

        1. 1000
        2. 900
        3. 800
        4. 750
        5. 700
        6. 650
        7. 600
        8. 550
        9. 500
        10. 450
        11. 400
        12. 375
        13. 350
        14. 325
        15. 300
        16. 275
        17. 250
        18. 225
        19. 200
        20. 175
        21. 150
        22. 140
        23. 130
        24. 120
        25. 110
        26. 100
        27. 90
        28. 80
        29. 70
        30. 60
        31. 50
        32. 40
        33. 35
        34. 30
        35. 25
        36. 20
        37. 15
        38. 10
        39. 5
        40. 1

    `millesimal`
      is the classic method, that distributes a multiple of
      1000/num-of-competitors."""

    siteurl = Column(
        url_t,
        info=dict(label=_('Website'),
                  hint=_('URL of the web site of the club.')))
    """Web site URL."""

    email = Column(
        email_t,
        info=dict(label=_('Email'),
                  hint=_('Email address of the club.')))
    """Email address of the club."""

    isfederation = Column(
        boolean_t,
        nullable=False,
        default=False,
        info=dict(label=_('Federation'),
                  hint=_('Whether the club is also a federation.')))
    """Flag indicating whether the club is also a federation."""

    ## Relations

    owner = relationship('User', backref='owned_clubs',
                         primaryjoin="Club.idowner==User.iduser")
    """The :py:class:`owner <.User>` of this record, `admin` when ``None``."""

    championships = relationship('Championship', backref='club',
                                 cascade="all, delete-orphan",
                                 order_by="Championship.description")
    """:py:class:`Championships <.Championship>` organized by this club."""

    associated_players = relationship('Player', backref='club',
                                      primaryjoin='Player.idclub==Club.idclub',
                                      passive_updates=False)
    """Players associated with this club."""

    federated_players = relationship('Player', backref='federation',
                                     primaryjoin='Player.idfederation==Club.idclub',
                                     passive_updates=False)
    """Players associated with this federation."""

    rating = relationship('Rating', foreign_keys=[idrating])
    """Default :py:class:`Ratings <.Rating>` used by this club's championships."""

    ratings = relationship('Rating', backref='club',
                           primaryjoin='Rating.idclub == Club.idclub')
    """:py:class:`Ratings <.Rating>` reserved for tourneys organized by this club."""

    users = relationship('User', secondary=clubusers)

    hosted_tourneys = relationship('Tourney', backref='hosting_club')

    @classmethod
    def check_insert(klass, session, fields, user_id):
        "Check description validity"

        try:
            desc = normalize(fields['description'])
        except KeyError:
            raise OperationAborted(_('For a new club the "description" field'
                                     ' is mandatory'))
        if not desc:
            raise OperationAborted(_('For a new club the "description" field'
                                     ' is mandatory'))

    def check_update(self, fields):
        "Check description validity"

        if 'description' in fields:
            desc = normalize(fields['description'])
            if not desc:
                raise OperationAborted(_('The "description" field of a club'
                                         ' cannot be empty'))

    @property
    def country(self):
        "The name of the club's country."

        return country_name(self.nationality)

    def countChampionships(self):
        """Return the number of championships organized by this club."""

        from .championship import Championship

        s = object_session(self)
        ct = Championship.__table__
        return s.execute(select([func.count(ct.c.idchampionship)])
                         .where(ct.c.idclub == self.idclub)).fetchone()[0]

    def countPlayers(self):
        """Return the number of players associated to this club."""

        from .player import Player

        s = object_session(self)
        pt = Player.__table__
        return s.execute(select([func.count(pt.c.idplayer)])
                         .where(or_(pt.c.idclub == self.idclub,
                                    pt.c.idfederation == self.idclub))).fetchone()[0]

    def serialize(self, serializer):
        """Reduce a single club to a simple dictionary.

        :param serializer: a :py:class:`.Serializer` instance
        :rtype: dict
        :returns: a plain dictionary containing a flatified view of this club
        """

        simple = {}
        simple['guid'] = self.guid
        simple['modified'] = self.modified
        if self.idrating:
            simple['rating'] = serializer.addRating(self.rating)
        if self.idowner:
            simple['owner'] = serializer.addUser(self.owner)
        simple['description'] = self.description
        if self.emblem:
            simple['emblem'] = self.emblem
        simple['prizes'] = self.prizes
        simple['couplings'] = self.couplings
        if self.nationality:
            simple['nationality'] = self.nationality
        if self.siteurl:
            simple['siteurl'] = self.siteurl
        if self.email:
            simple['email'] = self.email
        if self.isfederation:
            simple['isfederation'] = self.isfederation
        if self.users:
            susers = simple['users'] = []
            for user in self.users:
                susers.append(serializer.addUser(user))

        return simple
