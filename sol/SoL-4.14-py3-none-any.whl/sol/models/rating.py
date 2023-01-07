# -*- coding: utf-8 -*-
# :Project:   SoL -- The Rating entity
# :Created:   gio 05 dic 2013 09:05:58 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2013, 2014, 2015, 2016, 2018, 2020, 2022 Lele Gaifax
#

from datetime import date
from decimal import Decimal
import logging

from sqlalchemy import Column, ForeignKey, Index, Sequence, func, or_, exists, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import object_session

from ..i18n import translatable_string as _
from . import Base, GloballyUnique
from .domains import (
    boolean_t,
    code_t,
    description_t,
    flag_t,
    intid_t,
    prize_t,
    smallint_t,
    volatility_t,
    )
from .errors import OperationAborted
from .glicko2 import Glicko2, DRAW, LOSS, WIN
from .utils import normalize


logger = logging.getLogger(__name__)


class Rating(GloballyUnique, Base):
    """A particular rating a tournament can be related to."""

    __tablename__ = 'ratings'
    "Related table"

    @declared_attr
    def __table_args__(cls):
        return (GloballyUnique.__table_args__(cls) +
                (Index('%s_uk' % cls.__tablename__,
                       'description',
                       unique=True),))

    ## Columns

    idrating = Column(
        intid_t, Sequence('gen_idrating', optional=True),
        primary_key=True,
        nullable=False,
        info=dict(label=_('Rating ID'),
                  hint=_('Unique ID of the rating.')))
    """Primary key."""

    idowner = Column(
        intid_t, ForeignKey('users.iduser', name='fk_rating_owner', ondelete="SET NULL"),
        info=dict(label=_('Owner ID'),
                  hint=_('ID of the user that is responsible for this record.')))
    """ID of the :py:class:`user <.User>` that is responsible for this record."""

    idclub = Column(
        intid_t, ForeignKey('clubs.idclub', name='fk_rating_club', ondelete="SET NULL"),
        info=dict(label=_('Club ID'),
                  hint=_('ID of the club the rating is restricted to.')))
    """Restricted to :py:class:`club <.Club>`'s ID."""

    description = Column(
        description_t,
        nullable=False,
        info=dict(label=_('Description'),
                  hint=_('Description of the rating.')))
    """Description of the rating."""

    level = Column(
        flag_t,
        nullable=False,
        info=dict(label=_('Level'),
                  hint=_('Rating level.'),
                  dictionary=dict((str(i), v) for i, v in enumerate((
                      _('Historical (imported) rating'),
                      _('Level 1, international tourneys'),
                      _('Level 2, national/open tourneys'),
                      _('Level 3, regional tourneys'),
                      _('Level 4, courtyard tourneys'),
                  )))))
    """Rating level."""

    tau = Column(
        prize_t,
        nullable=False,
        default='0.5',
        info=dict(label=_('Tau'),
                  hint=_('The TAU value for the Glicko2 algorithm.'),
                  min=0.01, max=2))
    """Value of TAU for the Glicko2 algorithm."""

    default_rate = Column(
        smallint_t,
        nullable=False,
        default=1500,
        info=dict(label=_('Rate'),
                  hint=_('The default rate value for the Glicko2 algorithm.'),
                  min=1, max=3000))
    """Default value of rate (MU) for the Glicko2 algorithm."""

    default_deviation = Column(
        smallint_t,
        nullable=False,
        default=350,
        info=dict(label=_('Deviation'),
                  hint=_('The default deviation value for the Glicko2 algorithm.'),
                  min=1, max=500))
    """Default value of deviation (PHI) for the Glicko2 algorithm."""

    default_volatility = Column(
        volatility_t,
        nullable=False,
        default='0.06',
        info=dict(label=_('Volatility'),
                  hint=_('The default volatility value for the Glicko2 algorithm.'),
                  min=0.00001, max=1))
    """Default value of volatility (SIGMA) for the Glicko2 algorithm."""

    inherit = Column(
        boolean_t,
        nullable=False,
        default=False,
        info=dict(label=_('Inherit'),
                  hint=_('Whether to lookup rates in higher levels ratings.')))
    """Whether to lookup rates in higher levels ratings."""

    lower_rate = Column(
        smallint_t,
        nullable=False,
        default=1600,
        info=dict(label=_('Lower points'),
                  hint=_('Lower value of the range used to interpolate players rates'
                         ' when (almost) all competitors are unrated.')))
    """
    Lower value of the range used to interpolate players rates when (almost) all competitors
    are unrated.
    """

    higher_rate = Column(
        smallint_t,
        nullable=False,
        default=2600,
        info=dict(label=_('Higher points'),
                  hint=_('Higher value of the range used to interpolate players rates.')))
    """Higher value of the range used to interpolate players rates."""

    outcomes = Column(
        code_t,
        nullable=False,
        default='guido',
        info=dict(label=_('Match outcomes'),
                  hint=_('Kind of formula used to compute match outcomes.'),
                  dictionary=dict(
                      glicko=_('Standard Glicko'),
                      guido=_("Guido's formula"),
                      expds=_('Exponential on scores difference'))))
    """Kind of formula used to compute match outcomes.

    This is used to determine which formula will be used to compute the match outcomes to feed
    Glicko2 algorithm. It may be:

    `glicko2`
      standard Glicko, giving 1.0 to the winner and 0.0 to the loser, 0.5 in case of draw,
      developed with Chess in mind;

    `guido`
      Guido's variant, better suited to Carrom: basically each player is assigned a fraction of
      his own score divided by the sum of the scores of both players;

    `expds`
      an exponential formula applied to the two concurrents final scores difference.
    """

    ## Relations

    owner = relationship('User', backref='owned_ratings')
    """The :py:class:`owner <.User>` of this record, `admin` when ``None``."""

    championships = relationship('Championship', backref='rating',
                                 passive_updates=False)
    """:py:class:`Championships <.Championship>` using this rating by default."""

    tourneys = relationship('Tourney', backref='rating',
                            passive_updates=False,
                            order_by="Tourney.date")
    """:py:class:`Tourneys <.Tourney>` using this rating."""

    rates = relationship('Rate', backref='rating',
                         cascade="all, delete-orphan",
                         order_by="Rate.date, Rate.idplayer")
    """List of :py:class:`rates <.Rate>`."""

    @classmethod
    def check_insert(klass, session, fields, user_id):
        "Check description validity"

        from .club import Club, clubusers

        try:
            desc = normalize(fields['description'])
        except KeyError:
            raise OperationAborted(_('For a new rating the "description" field'
                                     ' is mandatory'))

        if not desc:
            raise OperationAborted(_('For a new rating the "description" field'
                                     ' is mandatory'))

        if user_id != 'admin':
            idclub = fields.get('idclub')

            if idclub is None:
                raise OperationAborted(_('You are not allowed to add a global rating,'
                                         ' not associated to a specific club'))

            clubs = Club.__table__
            if not session.scalar(select([True])
                                  .where(or_(
                                      exists()
                                      .where(clubs.c.idclub == idclub)
                                      .where(clubs.c.idowner == user_id),
                                      exists()
                                      .where(clubusers.c.idclub == idclub)
                                      .where(clubusers.c.iduser == user_id)))):
                raise OperationAborted(_('You are not allowed to add a rating to the'
                                         ' selected club'))

    def check_update(self, fields):
        "Check description validity"

        if 'description' in fields:
            desc = normalize(fields['description'])
            if not desc:
                raise OperationAborted(_('The "description" field of a rating'
                                         ' cannot be empty'))

    def getPlayerRating(self, player, before=None):
        """Return the rate of a `player`

        :param player: a Player instance
        :param before: a date instance
        :rtype: an instance of glicko2.Rating

        If `before` is not specified fetch the latest rate, otherwise the most recent one
        preceeding `before`.

        The method considers the referenced rating as well as all those with an higher level.
        """

        from . import Rate, Rating

        s = object_session(self)

        rt = Rate.__table__

        q = select([rt.c.rate, rt.c.deviation, rt.c.volatility]) \
            .where(rt.c.idplayer == player.idplayer)

        if before is not None:
            q = q.where(rt.c.date < before)

        if self.level > '0' and self.inherit:
            rts = Rating.__table__
            q = q.where(or_(rt.c.idrating == self.idrating,
                            rt.c.idrating.in_(select([rts.c.idrating])
                                              .where(rts.c.level < self.level))))
        else:
            q = q.where(rt.c.idrating == self.idrating)

        r = s.execute(q.order_by(rt.c.date.desc())).first()

        cr = Glicko2(tau=float(self.tau),
                     mu=self.default_rate,
                     phi=self.default_deviation,
                     sigma=float(self.default_volatility)).create_rating

        return cr(r[0], r[1], r[2]) if r is not None else cr()

    @property
    def ranking(self):
        """Players sorted by their latest rate.

        :rtype: sequence
        :returns: a sorted list of tuples containing the
                  :py:class:`player <.Player>`,
                  its latest rate, deviation and volatility, and the number of rates
                  in this rating.
        """

        from . import Player, Rate

        s = object_session(self)

        rt = Rate.__table__
        rta = rt.alias()
        rtc = rt.alias()

        lastrate = select([func.max(rta.c.date)]) \
            .where(rta.c.idrating == rt.c.idrating) \
            .where(rta.c.idplayer == rt.c.idplayer)

        ratecount = select([func.count(rtc.c.idrate)]) \
            .where(rtc.c.idrating == rt.c.idrating) \
            .where(rtc.c.idplayer == rt.c.idplayer).label('rates_count')

        q = select([rt.c.idplayer, rt.c.rate, rt.c.deviation, rt.c.volatility, ratecount]) \
            .where(rt.c.idrating == self.idrating) \
            .where(rt.c.date == lastrate) \
            .order_by(rt.c.rate.desc())

        rates = s.execute(q).fetchall()

        return [(s.query(Player).get(idplayer), r, rd, rv, rc)
                for idplayer, r, rd, rv, rc in rates]

    @property
    def time_span(self):
        "Return the time span of this rating."

        from . import Rate

        s = object_session(self)

        rt = Rate.__table__

        timespan = (select([func.min(rt.c.date), func.max(rt.c.date)])
                    .where(rt.c.idrating == self.idrating))
        return s.execute(timespan).first()

    def isPhantom(self, competitor):
        """Determine whether the given competitor is actually a Phantom.

        :param competitor: a Competitor instance

        This is needed because someone use a concrete player as Phantom,
        to customize its name (not everybody have a good sense of humor…)
        """

        return (competitor is None
                or (competitor.points == 0
                    and competitor.totscore == 0
                    and competitor.netscore % competitor.tourney.phantomscore == 0))

    def shouldConsiderTourney(self, tourney):
        """Determine whether the given tourney should be considered.

        :param tourney: a Tourney instance

        Only singles using the Swiss System should be considered. Also, "online" tournaments
        are excluded.
        """

        return ((tourney.system == 'swiss'
                 and tourney.championship.playersperteam == 1
                 and not tourney.championship.trainingboards))

    def _computeGlickoOutcomes(self, score1, score2):
        # Standard Glicko, best suited to Chess matches

        if score1 > score2:
            outcome1 = WIN
            outcome2 = LOSS
        elif score1 == score2:
            outcome1 = DRAW
            outcome2 = DRAW
        else:
            outcome1 = LOSS
            outcome2 = WIN

        return outcome1, outcome2

    def _computeGuidoOutcomes(self, score1, score2):
        # This is Guido Truffelli <truffelli.guido@gmail.com> adaptation to Carrom,
        # approved by dr. Glickman himself: use the whole range of values from 0 to 1,
        # not simply 0, 0.5 and 1.

        if score1 == 25 and score2 == 0:
            outcome1 = WIN
            outcome2 = LOSS
        elif score1 == 0 and score2 == 25:
            outcome1 = LOSS
            outcome2 = WIN
        elif score1 == score2:
            outcome1 = DRAW
            outcome2 = DRAW
        else:
            totalscore = float(score1 + score2)
            outcome1 = float(score1) / totalscore
            outcome2 = float(score2) / totalscore

        return outcome1, outcome2

    def _computeExpdsOutcomes(self, score1, score2):
        # Experimental/Exponential variant, taking into account the scores difference

        from math import exp

        diffscore = score1 - score2
        if diffscore > 22:
            outcome1 = WIN
            outcome2 = LOSS
        elif diffscore < -22:
            outcome1 = LOSS
            outcome2 = WIN
        elif diffscore == 0:
            outcome1 = DRAW
            outcome2 = DRAW
        else:
            outcome1 = 1.0 / (1.0 + exp(-0.3 * diffscore))
            outcome2 = 1.0 - outcome1

        return outcome1, outcome2

    def recompute(self, mindate=None, scratch=False):
        """Recompute the whole rating.

        :param mindate: either ``None`` or a date
        :param scratch: a boolean, True to recompute from scratch

        If `mindate` is given, recompute the rating ignoring the tourneys
        *before* that date.
        """

        from collections import defaultdict
        from . import Player, Rate

        if self.level == '0' or not self.tourneys:
            return

        try:
            compute_outcomes = getattr(self, "_compute%sOutcomes" % self.outcomes.capitalize())
        except AttributeError:  # pragma: nocover
            raise AttributeError("No %r method to compute match outcomes" % self.outcomes)

        logger.debug('Using the %r method to compute match outcomes', self.outcomes)

        firstdate = self.time_span[0]
        if scratch or (firstdate and ((mindate is None and self.tourneys[0].date < firstdate)
                                      or (mindate is not None and mindate < firstdate))):
            logger.debug('Recomputing %r from scratch', self)

            # TODO: find a more elegant way to do the following!
            # Non-inheriting ratings may contain historical rates, that does not have
            # a corresponding tourney, so we don't want to delete them...
            mindate = date(1900, 12, 31)
            if not self.inherit:
                rates = self.rates
                while rates and rates[-1].date > mindate:
                    rates.pop()
            else:
                self.rates = []
            mindate = None
        elif mindate:
            rates = self.rates
            while rates and rates[-1].date >= mindate:
                rates.pop()

        s = object_session(self)

        logger.debug('Glicko2 parameters: tau=%s mu=%s phi=%s sigma=%s',
                     self.tau, self.default_rate,
                     self.default_deviation, self.default_volatility)

        glicko2 = Glicko2(tau=float(self.tau),
                          mu=self.default_rate,
                          phi=self.default_deviation,
                          sigma=float(self.default_volatility))

        rcache = {}
        phantom_p = self.isPhantom

        for tourney in self.tourneys:
            if mindate is not None and tourney.date < mindate:
                continue

            if not tourney.prized or not self.shouldConsiderTourney(tourney):
                continue

            logger.debug('Considering tourney %s', tourney)

            outcomes = defaultdict(list)

            for match in tourney.matches:
                # Ignore final matches, per Guido advice
                if match.final:
                    continue

                c1 = match.competitor1
                c2 = match.competitor2

                # Usually a match against the Phantom is recognizable by the fact that the
                # second competitor is not assigned, but some people insist in using a concrete
                # player to customize the name
                if phantom_p(c1) or phantom_p(c2):
                    # Skip matches against Phantom
                    continue

                outcome1, outcome2 = compute_outcomes(match.score1, match.score2)

                # Player 1
                occ = outcomes[c1.idplayer1]
                if c2.idplayer1 not in rcache:
                    rcache[c2.idplayer1] = self.getPlayerRating(c2.player1,
                                                                tourney.date)
                    if logger.isEnabledFor(logging.DEBUG):  # pragma: nocover
                        logger.debug('%s rate is: %s',
                                     s.query(Player).get(c2.idplayer1),
                                     rcache[c2.idplayer1])
                occ.append((outcome1, rcache[c2.idplayer1]))

                # Player 2
                occ = outcomes[c2.idplayer1]
                if c1.idplayer1 not in rcache:
                    rcache[c1.idplayer1] = self.getPlayerRating(c1.player1,
                                                                tourney.date)
                    if logger.isEnabledFor(logging.DEBUG):  # pragma: nocover
                        logger.debug('%s rate is: %s',
                                     s.query(Player).get(c1.idplayer1),
                                     rcache[c1.idplayer1])
                occ.append((outcome2, rcache[c1.idplayer1]))

            # If there are unrated players interpolate their rate
            if any(rcache[idplayer].is_default for idplayer in outcomes):
                logger.debug('Interpolating unrated players rate')
                interpolate_unrated(rcache, tourney.ranking, glicko2, phantom_p,
                                    self.lower_rate, self.higher_rate)

            for idplayer in outcomes:
                current = rcache[idplayer]

                if logger.isEnabledFor(logging.DEBUG):  # pragma: nocover
                    logger.debug('Computing new rate for %s', s.query(Player).get(idplayer))
                    logger.debug('Player current rate: %s', current)
                    logger.debug('Player outcomes: %s', outcomes[idplayer])

                new = glicko2.rate(current, outcomes[idplayer])

                try:
                    pr = s.query(Rate) \
                          .filter(Rate.idrating == self.idrating) \
                          .filter(Rate.idplayer == idplayer) \
                          .filter(Rate.date == tourney.date).one()
                except NoResultFound:
                    pr = Rate(rating=self,
                              idplayer=idplayer,
                              date=tourney.date)
                    s.add(pr)

                pr.rate = max(new.rate, 800)
                pr.deviation = new.deviation
                pr.volatility = new.volatility

                rcache[idplayer] = new

                logger.debug('Recomputed rate=%s deviation=%s volatility=%s',
                             pr.rate, pr.deviation, pr.volatility)

    def update(self, data, missing_only=False):
        for field in ('tau', 'default_volatility'):
            value = data.get(field, None)
            if isinstance(value, str):
                data[field] = Decimal(value)
        return super().update(data, missing_only)

    def serialize(self, serializer):
        """Reduce a single rating to a simple dictionary.

        :param serializer: a :py:class:`.Serializer` instance
        :rtype: dict
        :returns: a plain dictionary containing a flatified view of this rating
        """

        simple = {}
        simple['guid'] = self.guid
        simple['modified'] = self.modified
        if self.idowner:
            simple['owner'] = serializer.addUser(self.owner)
        if self.idclub:
            simple['club'] = serializer.addClub(self.club)
        simple['description'] = self.description
        simple['level'] = self.level
        simple['inherit'] = self.inherit
        simple['tau'] = str(self.tau)
        simple['default_rate'] = self.default_rate
        simple['default_deviation'] = self.default_deviation
        simple['default_volatility'] = str(self.default_volatility)
        simple['lower_rate'] = self.lower_rate
        simple['higher_rate'] = self.higher_rate
        simple['outcomes'] = self.outcomes

        return simple


def interpolate_unrated(cache, ranking, glicko2, phantom_p, lower_rate, higher_rate):
    """Interpolate the rate of unrated players from the ranking."""

    unrated = []

    sumx = sumy = sumxy = sumx2 = phantoms = 0

    for x, competitor in enumerate(ranking, 1):
        # Do not consider withdrawn players when their only match was against the phantom
        if phantom_p(competitor) or competitor.idplayer1 not in cache:
            phantoms += 1
            continue

        if cache[competitor.idplayer1].is_default:
            unrated.append((x, competitor.idplayer1))
        else:
            y = cache[competitor.idplayer1].rate
            sumx += x
            sumy += y
            sumxy += x*y
            sumx2 += x**2

    nrated = len(ranking) - phantoms - len(unrated)
    if nrated < 2:
        # If there are less than 2 rated players, arbitrarily consider
        # two players, the first with 2600pt the other with 1600pt
        nrated = 2
        sumx = 1 + len(ranking) - phantoms
        sumy = lower_rate + higher_rate
        sumxy = higher_rate + (len(ranking) - phantoms) * lower_rate
        sumx2 = 1 + (len(ranking) - phantoms)**2

    den = nrated * sumx2 - sumx**2
    m = float(nrated * sumxy - sumx * sumy) / den
    q = float(sumy * sumx2 - sumx * sumxy) / den

    for x, idplayer in unrated:
        cache[idplayer].update(glicko2.create_rating(mu=int(x * m + q + 0.5)))
