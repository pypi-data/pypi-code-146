# -*- coding: utf-8 -*-
# :Project:   SoL -- The Tourney entity
# :Created:   gio 27 nov 2008 13:54:14 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008-2010, 2013-2016, 2018-2023 Lele Gaifax
#

from collections import Counter, defaultdict, namedtuple
from fractions import Fraction
from itertools import chain, combinations
import logging
from math import log2
from operator import attrgetter, itemgetter

from itsdangerous import Signer
from sqlalchemy import Column, ForeignKey, Index, Sequence, func, exists, or_, select
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import object_session, relationship

from ..i18n import gettext, translatable_string as _
from . import Base, GloballyUnique
from .domains import (
    boolean_t,
    code_t,
    date_t,
    description_t,
    int_t,
    intid_t,
    smallint_t,
    url_t,
    )
from .errors import OperationAborted
from .utils import normalize


logger = logging.getLogger(__name__)

Rank = namedtuple('Rank', 'points,bucholz,netscore,totscore,position,rate')


class RankingStats:
    """
    An interim object used keep the ongoing values needed to compute the ranking of a single
    competitor.
    """

    __slots__ = ('points', 'netscore', 'totscore', 'bucholz', 'real_points',
                 'played_matches', 'virtual_points', 'retired')

    def __init__(self, retired):
        self.points = 0
        "Overall points."

        self.netscore = 0
        "Net score."

        self.totscore = 0
        "Total score."

        self.bucholz = 0
        "Bucholz."

        self.real_points = 0
        "Points made against real competitors."

        self.played_matches = 0
        "Number of played matches."

        self.virtual_points = 0
        "Estimated further points, after retirement."

        self.retired = retired
        "Whether it is a retired competitor."

    def won(self, netscore, against_phantom):
        "Update stats after a winned match."

        self.played_matches += 1
        self.netscore += netscore
        self.points += 2
        if not against_phantom:
            self.real_points += 2

    def lost(self, netscore):
        "Update stats after a lost match."

        self.played_matches += 1
        self.netscore -= netscore

    def drawn(self):
        "Update stats after a tie."

        self.played_matches += 1
        self.points += 1
        self.real_points += 1

    def rank(self, position, rate):
        "Return the final :class:`Rank`."

        return Rank(points=self.points, bucholz=self.bucholz, netscore=self.netscore,
                    totscore=self.totscore, position=None if position is None else -position,
                    rate=rate)


class NoMoreCombinationsError(OperationAborted):
    pass


class Tourney(GloballyUnique, Base):
    """A single tournament."""

    __tablename__ = 'tourneys'
    "Related table"

    @declared_attr
    def __table_args__(cls):
        return (GloballyUnique.__table_args__(cls) +
                (Index('%s_uk' % cls.__tablename__,
                       'date', 'idchampionship',
                       unique=True),))

    ## Columns

    idtourney = Column(
        intid_t, Sequence('gen_idtourney', optional=True),
        primary_key=True,
        nullable=False,
        info=dict(label=_('Tourney ID'),
                  hint=_('Unique ID of the tourney.')))
    """Primary key."""

    idchampionship = Column(
        intid_t, ForeignKey('championships.idchampionship', name='fk_tourney_championship'),
        nullable=False,
        info=dict(label=_('Championship ID'),
                  hint=_('ID of the championship the tourney belongs to.')))
    """Related :py:class:`championship <.Championship>`'s ID."""

    idhostingclub = Column(
        intid_t, ForeignKey('clubs.idclub', name='fk_championship_club'), nullable=True,
        info=dict(label=_('Hosting club ID'),
                  hint=_('ID of the club hosting the tournament.')))
    """Hosting :py:class:`club <.Club>`'s ID."""

    idrating = Column(
        intid_t, ForeignKey('ratings.idrating', name='fk_tourney_rating'),
        info=dict(label=_('Rating ID'),
                  hint=_('ID of the rating this tourney uses.')))
    """Possible :py:class:`rating <.Rating>` ID this tourney uses and updates."""

    idowner = Column(
        intid_t, ForeignKey('users.iduser', name='fk_tourney_owner', ondelete="SET NULL"),
        info=dict(label=_('Owner ID'),
                  hint=_('ID of the user that is responsible for this record.')))
    """ID of the :py:class:`user <.User>` that is responsible for this record."""

    date = Column(
        date_t,
        nullable=False,
        info=dict(label=_('Date'),
                  hint=_('Date of the event.')))
    """Event date."""

    description = Column(
        description_t,
        nullable=False,
        info=dict(label=_('Description'),
                  hint=_('Description of the tourney.')))
    """Event description."""

    location = Column(
        description_t,
        info=dict(label=_('Location'),
                  hint=_('Location of the tourney.')))
    """Event location."""

    socialurl = Column(
        url_t,
        info=dict(label=_('Social site'),
                  hint=_('URL of the social site dedicated to the tournament, if any.')))
    """Social site URL."""

    duration = Column(
        smallint_t,
        nullable=False,
        default=45,
        info=dict(label=_('Duration'),
                  hint=_('Duration in minutes of each round.'),
                  min=0))
    """Duration in minutes of each round, used by the clock."""

    prealarm = Column(
        smallint_t,
        nullable=False,
        default=5,
        info=dict(label=_('Prealarm'),
                  hint=_('Prealarm before the end of the round, usually no more games'
                         ' after that.'),
                  min=0))
    """Prealarm before the end of the round."""

    system = Column(
        code_t,
        nullable=False,
        default='swiss',
        info=dict(label=_('System'),
                  hint=_('Kind of tournament.'),
                  dictionary=dict(swiss=_('Swiss'),
                                  knockout=_('Knockout'))))
    """The type of tournament, it may be `swiss` (the default) or `knockout`."""

    couplings = Column(
        code_t,
        nullable=False,
        default='serial',
        info=dict(label=_('Pairings'),
                  hint=_('Method used to pair competitors at each round.'),
                  dictionary=dict(all=_('All possible matches'),
                                  serial=_('Ranking order'),
                                  dazed=_('Cross ranking order'),
                                  staggered=_('Staggered ranking order'),
                                  seeds=_('Top players (KO only)'),
                                  extremes=_('Ranking extremes (KO only)'))))
    """Kind of pairing method used to build next round. It may be `all`, `serial`, `dazed`,
    `staggered`, `seeds` or `extremes`, the latter two valid only for knockout tourneys."""

    delaytoppairing = Column(
        smallint_t,
        nullable=False,
        default=1,
        info=dict(label=_('Delay top players pairing'),
                  hint=_('Number of rounds for which pairing of top players should be'
                         ' postponed, if possible. Meaningful only if using a rating.'),
                  min=0))
    """Number of rounds for which pairing of top players should be postponed, if possible."""

    delaycompatriotpairing = Column(
        boolean_t,
        nullable=False,
        default=False,
        info=dict(label=_('Delay compatriots pairing'),
                  hint=_('Whether the system should try to postpone the pairing of players'
                         ' belonging to the same country, if possible.'),
                  min=0))
    """Whether the pairing of players belonging to the same country shall be postponed or
    not."""

    currentturn = Column(
        smallint_t,
        nullable=False,
        default=0,
        info=dict(label=_('Round'),
                  hint=_('The highest generated round number.')))
    """The current round."""

    countdownstarted = Column(
        int_t,
        info=dict(label=_('Countdown start'),
                  hint=_('The timestamp of the start of the clock countdown.')))
    """Timestamp of the start of the clock countdown, milliseconds since Unix epoch."""

    rankedturn = Column(
        smallint_t,
        nullable=False,
        default=0,
        info=dict(label=_('Ranked round'),
                  hint=_('To which round the ranking is up-to-date with.')))
    """The highest round considered in the ranking."""

    prized = Column(
        boolean_t,
        nullable=False,
        default=False,
        info=dict(label=_('Closed'),
                  hint=_('Whether the final prizes have been assigned.')))
    """Whether the tourney is closed, and final prizes updated."""

    phantomscore = Column(
        smallint_t,
        nullable=False,
        default=25,
        info=dict(label=_('Phantom score'),
                  hint=_('The score assigned to a player in matches against the Phantom.'),
                  min=1, max=25))
    """The score assigned to a player in matches against the Phantom."""

    retirements = Column(
        code_t,
        nullable=False,
        default='none',
        info=dict(label=_('Drop outs'),
                  hint=_('Policy used to adjust the bucholz of competitors who played against'
                         ' withdrawn players.'),
                  dictionary=dict(none=_('No adjustment'),
                                  trend=_('Average trend'),
                                  trend70=_('70％ of average trend'))))
    "Policy used to adjust the bucholz of competitors who played against withdrawn players."

    finals = Column(
        smallint_t,
        default=0,
        info=dict(label=_('Finals'),
                  hint=_('The number of finals that will be played: 0 means no finals,'
                         ' 1 means one final for the 1st and 2nd place, 2 also for the'
                         ' 3rd and fourth place.'),
                  min=0, max=2))
    """The number of finals that will be played."""

    finalkind = Column(
        code_t,
        nullable=False,
        default='simple',
        info=dict(label=_('Final kind'),
                  hint=_('The kind of finals.'),
                  dictionary=dict(simple=_('Single match'),
                                  bestof3=_('Best of three matches'))))
    """Kind of finals. It may be `simple` or `bestof3`."""

    finalturns = Column(
        boolean_t,
        nullable=False,
        default=False,
        info=dict(label=_('Final rounds'),
                  hint=_('Whether the tourney is in final rounds state.')))
    """Whether the tourney is in final rounds state."""

    ## Relations

    owner = relationship('User', backref='owned_tourneys')
    """The :py:class:`owner <.User>` of this record, `admin` when ``None``."""

    competitors = relationship('Competitor', backref='tourney',
                               cascade="all, delete-orphan",
                               lazy='joined')
    """List of :py:class:`competitors <.Competitor>`."""

    matches = relationship('Match', backref='tourney',
                           cascade="all, delete-orphan",
                           order_by="Match.turn, Match.board")
    """List of :py:class:`matches <.Match>`, sorted by round and board."""

    @classmethod
    def check_insert(klass, session, fields, user_id):
        "Check description validity"

        from . import Championship
        from .club import Club, clubusers

        try:
            desc = normalize(fields['description'])
        except KeyError:
            raise OperationAborted(_('For a new tourney the "description" field'
                                     ' is mandatory'))

        if not desc:
            raise OperationAborted(_('For a new tourney the "description" field'
                                     ' is mandatory'))

        idcship = fields.get('idchampionship')
        if idcship is None:  # pragma: no cover
            raise OperationAborted(_('For a new tourney the "championship" field'
                                     ' is mandatory'))

        if user_id != 'admin':
            clubs = Club.__table__
            cships = Championship.__table__
            if not session.scalar(select([True])
                                  .where(exists()
                                         .where(cships.c.idchampionship == idcship)
                                         .where(or_(
                                             cships.c.idowner == user_id,
                                             exists()
                                             .where(clubs.c.idclub == cships.c.idclub)
                                             .where(clubs.c.idowner == user_id),
                                             exists()
                                             .where(clubusers.c.idclub == cships.c.idclub)
                                             .where(clubusers.c.iduser == user_id))))):
                raise OperationAborted(_('You are not allowed to add a tourney to the'
                                         ' selected championship'))

    def check_update(self, fields):
        "Check description validity"

        if 'description' in fields:
            desc = normalize(fields['description'])
            if not desc:
                raise OperationAborted(_('The "description" field of a tourney'
                                         ' cannot be empty'))

    def caption(self, html=None, localized=True):
        return gettext('$tourney — $championship, $date', just_subst=not localized,
                       mapping=dict(tourney=self.description,
                                    championship=self.championship.caption(html, localized),
                                    date=self.date.strftime(gettext('%m-%d-%Y'))))

    def allPlayers(self):
        "Generator that return all involved players."

        for c in self.competitors:
            yield c.player1
            if c.player2 is not None:
                yield c.player2
                if c.player3 is not None:  # pragma: nocover
                    yield c.player3
                    if c.player4 is not None:  # pragma: nocover
                        yield c.player4

    @property
    def isAllAgainstAllTraining(self):
        return bool(self.couplings == 'all' and self.championship.trainingboards)

    @property
    def ranking(self):
        """Competitors sorted by their rank.

        :rtype: sequence
        :returns: sorted list of :py:class:`competitors <.Competitor>`
        """

        from operator import attrgetter

        # Initial sort on ascending players name, to match the ordering used by the Ranking
        # panel: thanks to Python's sort stability further sorts will maintain this ordering
        # for equal keys
        competitors = sorted(self.competitors, key=attrgetter('player1.lastname',
                                                              'player1.firstname'))

        if self.rankedturn == 0:
            if self.idrating is not None:
                def key(c):
                    return (-c.position, c.rate)
            else:
                def key(c):
                    return -c.position
        else:
            if self.prized:
                key = attrgetter('prize', 'points', 'bucholz', 'netscore', 'totscore')
            else:
                if self.idrating is not None:
                    def key(c):
                        return (c.points, c.bucholz, c.netscore, c.totscore, -c.position,
                                c.rate)
                else:
                    def key(c):
                        return (c.points, c.bucholz, c.netscore, c.totscore, -c.position)

        ranking = sorted(competitors, key=key, reverse=True)

        if not self.prized and self.finals and self.finalturns:
            enough, nfinalturns, wins = self._areFinalTurnsEnoughForPrizing()
            if enough:
                # Possibly swap positions of finalists
                for final in range(self.finals):
                    i1 = final*2
                    i2 = i1 + 1
                    c1 = ranking[i1]
                    c2 = ranking[i2]
                    if wins.get(c1, 0) < wins.get(c2, 0):
                        ranking[i1:i2+1] = [c2, c1]

        return ranking

    def _computeFinalWins(self):
        """Compute the number of matches won by each competitor in the finals"""

        finalmatches = [m for m in self.matches if m.final]
        nfinalturns = len(set(m.turn for m in finalmatches))

        wins = Counter()
        for match in finalmatches:
            if match.score1 != match.score2:
                winner, loser, netscore = match.results()
                wins[winner] += 1

        return nfinalturns, wins

    def _areFinalTurnsEnoughForPrizing(self):
        "Determine whether final rounds are enough to complete the tourney with prize-giving."

        nfinalturns, wins = self._computeFinalWins()

        if self.finalkind == 'simple':
            return nfinalturns == 1, nfinalturns, wins
        else:
            if nfinalturns == 3:
                return True, nfinalturns, wins
            else:
                # If all competitors won at least two matches, we are done
                return wins and all(wins[c] >= 2 for c in wins), nfinalturns, wins

    def updateRanking(self):
        """Recompute and update competitors ranking.
        """

        if self.prized:
            raise OperationAborted(_('Cannot update rankings after prize-giving!'))

        is_aaat = self.isAllAgainstAllTraining

        ranking = dict(self.computeRanking())

        for comp in self.competitors:
            r = ranking[comp]
            comp.points = r.points
            comp.netscore = r.netscore
            comp.totscore = r.totscore
            comp.bucholz = r.bucholz

        if is_aaat:
            if self.matches:
                for match in self.matches:
                    if not match.isScored:
                        self.currentturn = match.turn
                        self.rankedturn = match.turn - 1
                        break
                else:
                    self.currentturn = self.rankedturn = match.turn
        else:
            self.rankedturn = self.currentturn

        self.modified = func.now()

        if self.finals and self.finalturns and self._areFinalTurnsEnoughForPrizing()[0]:
            # Automatically assign final prizes, so the user isn't bothered with that
            # (the "prizes" button is hidden)
            self.assignPrizes()

    def computeRanking(self, turn=None):
        """Recompute competitors ranking.

        :param turn: if given, compute the ranking up to that turn
        :returns: a list of tuples, each containing one of the competitors and a :class:`Rank`
                  instance, sorted on the second item in descending order

        Compute each competitor rank by examining the matches of this tourney, summing up each
        other's current ranking position as the bucholz.
        """

        # Start from scratch, assigning zero to all competitors
        ranking = {comp: RankingStats(comp.retired) for comp in self.competitors}

        is_aaat = self.isAllAgainstAllTraining

        # First of all, sum up points and netscore
        highest_scored_turn = 0
        for match in self.matches:
            if (turn is not None and match.turn > turn) or match.final:
                break

            if is_aaat and not match.isScored:
                continue

            highest_scored_turn = match.turn

            winner, loser, netscore = match.results()
            if netscore == 0:
                ranking[winner].drawn()
                ranking[loser].drawn()
            else:
                ranking[winner].won(netscore, loser is None)
                if loser is not None:
                    ranking[loser].lost(netscore)

        # Then compute the bucholz, summing up each competitor's points, possibly adjusted by
        # the configured policy
        if self.retirements != 'none':
            if self.retirements == 'trend':
                factor = 1
            else:
                assert self.retirements == 'trend70'
                factor = Fraction(70, 100)
            current_turn = highest_scored_turn if turn is None else turn
            for r in ranking.values():
                if r.retired:
                    if r.real_points != 0:
                        average = Fraction(r.real_points, r.played_matches) * factor
                        adjustment = average * (current_turn - r.played_matches)
                    else:
                        adjustment = 0
                    r.virtual_points = int(adjustment)

        # Add phantom
        ranking[None] = RankingStats(False)

        for match in self.matches:
            if (turn is not None and match.turn > turn) or match.final:
                break

            r1 = ranking[match.competitor1]
            r2 = ranking[match.competitor2]
            r1.totscore += match.score1
            r2.totscore += match.score2
            r1.bucholz += r2.points + r2.virtual_points
            r2.bucholz += r1.points + r1.virtual_points

        # Compute the final ranking, properly sorted
        ranking = [(c, r.rank(c.position, c.rate))
                   for c, r in ranking.items() if c is not None]
        return sorted(ranking, key=itemgetter(1), reverse=True)

    def makeNextTurn(self):
        """Setup the next round.

        If there are no matches, build up the first round using a random coupler. Otherwise,
        using current ranking, create the next round pairing any given competitor with a
        not-yet-met other one that follows him in the ranking.
        """

        if self.prized:
            raise OperationAborted(_('Cannot create other rounds after prize-giving!'))

        if self.championship.trainingboards:
            noemail = [c.player1 for c in self.competitors if not c.player1.email]
            if noemail:  # pragma: no cover
                names = ', '.join(p.caption(localized=False) for p in noemail)
                raise OperationAborted(_('Cannot proceed, following competitors do not have'
                                         ' an email address: ${names}',
                                         mapping=dict(names=names)))

        is_aaat = self.isAllAgainstAllTraining

        if not is_aaat:
            if self.currentturn and self.currentturn != self.rankedturn:
                raise OperationAborted(_('The ranking is not up-to-date!'))

        if self.finalturns:
            self.currentturn = self._makeNextFinalTurn()
        elif is_aaat:
            self._makeAllTurns()
            self.currentturn = 1
        elif ((self.idrating is not None
               or self.currentturn
               or self.couplings == 'all'
               or self.system == 'knockout')):
            # If the tourney is using a rating, create the first round
            # with the usual rules instead of random couplings
            self.currentturn = self._makeNextTurn()
        else:
            self._makeFirstTurn()
            self.currentturn = 1

        self.countdownstarted = None
        self.modified = func.now()

    def _makeFirstTurn(self):
        "Create the first round of a tourney, pairing competitors in a random way."

        from random import randint
        from . import Match

        comps = self.competitors[:]
        i = len(comps)
        board = 1
        while i > 0:
            c1 = comps.pop(randint(0, i-1))
            if i == 1:
                c2 = None
            else:
                c2 = comps.pop(randint(0, i-2))
            m = Match(turn=1, board=board, competitor1=c1, competitor2=c2,
                      score1=self.phantomscore if c2 is None else 0, score2=0)
            self.matches.append(m)
            i -= 2
            board += 1

    def _makeAllTurns(self):
        "Create all possible turns in a training tournament."

        # Inspired by https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method

        from . import Match

        comps = self.competitors[:]
        n = len(comps)
        if n % 2:
            comps.append(None)
            n += 1
        half = n // 2

        for turn in range(1, n):
            matches = []

            halve_1 = comps[:half]
            halve_2 = comps[half:]
            halve_2.reverse()

            phantommatch = None
            for c1, c2 in zip(halve_1, halve_2):
                if c1 is None:
                    c1, c2 = c2, c1
                m = Match(turn=turn, competitor1=c1, competitor2=c2, score1=0, score2=0)
                if c2 is None:
                    phantommatch = m
                else:
                    matches.append(m)

            for board, match in enumerate(matches, 1):
                match.board = board

            if phantommatch is not None:
                phantommatch.board = len(matches) + 1
                matches.append(phantommatch)

            self.matches.extend(matches)

            comps = [comps[0], comps[-1]] + comps[1:-1]

    class AbstractVisitor:
        """Abstract visitor.

        :param tourney: a :py:class:`.Tourney` instance
        :param pivot: a :py:class:`.Competitor` instance
        :param competitors: a list of possible opponents
        :param done: the set of already played pairings

        This is an `iterator class`__, used by the method :py:meth:`Tourney._combine`: it
        yields all possible competitors to `pivot` in some order, without repeating already
        played matches present in `done`, a set containing previous matches (both ``(a, b)``
        and ``(b, a)``).

        The iteration honors the tourney's `delaycompatriotpairing`: when ``True``, players
        with the same nationality of the `pivot` and with the same points will be considered
        later.

        Concrete subclasses must reimplement the method ``computeVisitOrder()``, that
        determines the actual *order*.

        __ https://docs.python.org/3.7/library/stdtypes.html#iterator-types
        """

        def __init__(self, tourney, pivot, competitors, done):
            self.tourney = tourney
            self.pivot = pivot
            self.competitors = competitors
            self.done = done

        def computeVisitOrder(self):  # pragma: no cover
            "Return a sequence of *positions*, the indexes into the list `self.competitors`."

            raise NotImplementedError("Class %s must reimplement method computeVisitOrder()"
                                      % self.__class__)

        def __iter__(self):
            pivot = self.pivot
            competitors = self.competitors
            positions = self.computeVisitOrder()
            if self.tourney.delaycompatriotpairing:
                positions = list(positions)
                if len(positions) > 2:
                    soon = []
                    late = []
                    for i in positions:
                        c = competitors[i]
                        if c is None or c.nationality == pivot.nationality:
                            late.append(i)
                        else:
                            soon.append(i)
                    positions = soon + late
            done = self.done
            for i in positions:
                c = competitors[i]
                if c is not pivot and (pivot, c) not in done:
                    yield c

    class SerialVisitor(AbstractVisitor):
        """Visit the `competitors` in order.

        Given that the list of competitors is sorted by their rank, this effectively tries to
        combine players with the same strength.
        """

        def computeVisitOrder(self):
            "Simply return ``range(len(self.competitors))``."

            return range(len(self.competitors))

    class DazedVisitor(AbstractVisitor):
        """Visit the `competitors`, giving precedence to the competitors with the same points.

        This starts looking at the competitors with the same points as the `pivot`, and then
        goes on with the others: this is to postpone as much as possible the match between the
        strongest competitors.
        """

        def countSamePointsAsPivot(self):
            "Return the count of competitors with the same points as the `pivot`."

            same_points = 0
            pivot_points = self.pivot.points
            for c in self.competitors:
                # The competitors may contain the phantom, ie a None
                if c is not None and c.points == pivot_points:
                    same_points += 1
                else:
                    break
            return same_points

        def computeVisitOrder(self):
            """First count how many competitors have the same points as the `pivot`, then if
            possible iterate over the second half of them, then over the first half, and
            finally over the remaining ones.
            """

            same_points = self.countSamePointsAsPivot()
            all_players = len(self.competitors)
            if same_points > 2:
                # If the group cardinality is odd, try to include the first player of
                # the next group
                if same_points < all_players and same_points % 2:
                    # Considering the presence of the phantom, don't to that if we are
                    # building the very first round, ie when all players have 0 points
                    if None not in self.competitors or same_points != (all_players - 1):
                        if logger.isEnabledFor(logging.DEBUG):  # pragma: nocover
                            border_c = self.competitors[same_points].caption(False, False)
                            logger.debug("Considering competitor “%s” as belonging to"
                                         " the group with %d points",
                                         border_c, self.pivot.points)
                        same_points += 1
                middle = same_points // 2
                positions = chain(range(middle, same_points),
                                  range(0, middle),
                                  range(same_points, all_players))
            else:
                positions = range(all_players)
            return positions

    class StaggeredVisitor(DazedVisitor):
        """Visit the `competitors`, giving precedence to the competitors with the same points.

        This is similar to :py:class:`.DazedVisitor` except that when there are 50 or more
        competitors with the same points, instead of splitting them in two halves of the same
        size it uses an arbitrary offset of 25 (i.e. the 1st competitor is paired with the
        26th, the 2nd with the 27th, and so on): this should placate the gripes about unfair
        pairings between strongest and weakest competitors at the first turn.
        """

        def computeVisitOrder(self):
            same_points = self.countSamePointsAsPivot()
            all_players = len(self.competitors)
            if same_points > 2:
                if same_points < all_players and same_points % 2:
                    # Considering the presence of the phantom, don't to that if we are
                    # building the very first round, ie when all players have 0 points
                    if None not in self.competitors or same_points != (all_players - 1):
                        if logger.isEnabledFor(logging.DEBUG):  # pragma: nocover
                            border_c = self.competitors[same_points].caption(False, False)
                            logger.debug("Considering competitor “%s” as belonging to"
                                         " the group with %d points",
                                         border_c, self.pivot.points)
                        same_points += 1
                if same_points >= 50:
                    positions = chain(range(25, same_points),
                                      range(0, 25),
                                      range(same_points, all_players))
                else:
                    middle = same_points // 2
                    positions = chain(range(middle, same_points),
                                      range(0, middle),
                                      range(same_points, all_players))
            else:
                positions = range(all_players)
            return positions

    def _combine(self, competitors, done, _level=0):
        """Build the next round, based on current ranking.

        This recursively tries to build the next round, pairing together competitors that did
        not already played against each other.
        """

        if logger.isEnabledFor(logging.DEBUG):  # pragma: nocover
            from pprint import pformat

            ranking = self.ranking

            def debug(msg, *args):
                logger.debug("%sL%02d "+msg, "="*_level, _level, *args)

            def C(c):
                if c:
                    position = f"{ranking.index(c) + 1}. "
                    return f"{position}{c.caption(False, False)} ({c.points}p)"
                else:
                    return "Phantom"

            if _level == 0 and done:
                done_matches = {}
                for c1, c2 in done:
                    if c1:
                        matches = done_matches.setdefault(c1, [])
                        if c2 not in matches:
                            matches.append(c2)
                            matches = done_matches.setdefault(c2, [])
                            matches.append(c1)
                logger.debug("Done matches:\n%s",
                             '\n'.join(f"  {C(c)}: {', '.join(C(o) for o in done_matches[c])}"
                                       for c in ranking))

            debug("Competitors to be paired:\n%s",
                  '\n'.join(f"  {C(c)}" for c in competitors))
        else:
            debug = None

        if len(competitors) < 2:  # pragma: nocover
            if debug:
                debug("Backtracking: no more combinations")
            return None

        try:
            visitor = getattr(self, self.couplings.capitalize() + "Visitor")
        except AttributeError:  # pragma: nocover
            raise AttributeError("No %r method to pair competitors with"
                                 % self.couplings)

        c1 = competitors[0]
        if debug:  # pragma: nocover
            remainingc = tuple(visitor(self, c1, competitors, done))
            if remainingc:
                debug('Looking for a competitor for %s within\n%s', C(c1),
                      '\n'.join(f"  {C(c)}" for c in remainingc))
            else:
                debug('Backtracking: no possible competitors for %s', C(c1))

        for n, c2 in enumerate(visitor(self, c1, competitors, done), 1):
            if debug:  # pragma: nocover
                debug("Tentative %d: trying %s vs %s", n, C(c1), C(c2))
            if len(competitors) > 2:
                remainings = self._combine(
                    [c for c in competitors if c is not c1 and c is not c2],
                    done, _level=_level+1)
                if remainings:
                    newturn = [(c1, c2)] + remainings
                    if debug:  # pragma: nocover
                        if _level == 0:
                            debug("OK =>\n%s",
                                  '\n'.join(f"  {C(_c1)} vs {C(_c2)}" for _c1, _c2 in newturn))
                        else:
                            debug("OK")
                    return newturn
            else:
                if debug:  # pragma: nocover
                    debug("OK => %s vs %s", C(c1), C(c2))
                return [(c1, c2)]

    def _assignBoards(self, matches, comp_boards):
        """Assign a table to each match, possibly one not already used."""

        available_boards = range(1, len(matches)+1)
        for match in matches:
            boards_usage = comp_boards[match.competitor1]
            # Consider the second competitor only when there are more than
            # 6 boards/12 competitors: under that threshold it's better to
            # try making the first competitor to play an a different board
            # each time. See issue #34.
            if len(matches) > 6:
                boards_usage = boards_usage + comp_boards[match.competitor2]
            board = sorted(available_boards, key=boards_usage.__getitem__)[0]

            available_boards = [b for b in available_boards if b != board]
            match.board = board

    def _makeNextTurn(self):
        """Build the next round of the game."""

        from . import Match

        if self.system == 'knockout' and self.couplings == 'seeds':
            if not all(c.position for c in self.competitors
                       if not c.retired):  # pragma: no cover
                raise OperationAborted(_("Missing seeds position for some competitor"))

        ranking = self.ranking

        if self.idrating is not None and self.rankedturn <= self.delaytoppairing:
            # Reorder the ranking taking into account the rate of each competitors
            # just after the bucholz, to delay top players pairing
            if self.system == 'swiss':
                key = attrgetter('points', 'bucholz', 'rate', 'netscore', 'totscore')
            else:
                def key(c):
                    return (c.points, c.bucholz, -c.position, c.rate, c.netscore, c.totscore)
            ranking = sorted(ranking, key=key, reverse=True)

        done = set()
        last = 0
        # A dictionary with a counter of used boards for each competitor,
        # used later by _assignBoards()
        comp_boards = defaultdict(Counter)
        for m in self.matches:
            if m.turn > last:
                last = m.turn
            c1 = m.competitor1
            c2 = m.competitor2
            done.add((c1, c2))
            done.add((c2, c1))
            comp_boards[c1][m.board] += 1
            comp_boards[c2][m.board] += 1

        newturn = last+1
        if self.system == 'swiss' or newturn == 1:
            activecomps = [c for c in ranking if not c.retired]
        else:
            if self.couplings == 'extremes':
                losers = {m.results()[1] for m in self.matches}
                activecomps = [c for c in ranking if c not in losers]
            elif self.couplings == 'seeds':
                # With this method, the ranking is not considered, it's just "winner of first
                # table against winner of last table, winner of the third against winner of
                # the second-last table" and so on, see _makeNextKnockoutTurn()
                activecomps = [m.results()[0] for m in self.matches if m.turn == last]
            else:  # pragma: no cover
                raise OperationAborted(_("Invalid method $couplings for knockout tourney!",
                                         mapping=dict(couplings=repr(self.couplings))))

        if len(activecomps) == 1:
            raise NoMoreCombinationsError(
                _("Cannot create another round: no more possible combinations!"))

        # Append the phantom if the number is odd
        if len(activecomps) % 2:
            activecomps.append(None)

        if self.couplings == 'all':
            combination = self._makeNextAAATurn(activecomps, done)
        elif self.system == 'knockout':
            combination = self._makeNextKnockoutTurn(activecomps)
        else:
            combination = self._combine(activecomps, done)

        phantommatch = None
        if combination:
            matches = []
            for c1, c2 in combination:
                # Put match against phantom last
                if c2 is None:
                    phantommatch = Match(turn=newturn,
                                         competitor1=c1, competitor2=c2,
                                         score1=self.phantomscore, score2=0)
                else:
                    m = Match(turn=newturn,
                              competitor1=c1, competitor2=c2,
                              score1=0, score2=0)
                    matches.append(m)

            if self.system == 'swiss':
                self._assignBoards(matches, comp_boards)
            else:
                for board, match in enumerate(matches, 1):
                    match.board = board

            if phantommatch:
                phantommatch.board = len(matches)+1
                matches.append(phantommatch)

            self.matches.extend(matches)
        else:
            if self.couplings != 'all':
                remaining = self._countRemainingMatches(activecomps, done)
                if remaining:
                    raise OperationAborted(
                        _("Cannot create next round: there are further $remaining possible"
                          " matches but they cannot be grouped together with the current"
                          " pairing rules. Nevertheless, you can switch to the “All"
                          " possible matches” method to generate remaining rounds.",
                          mapping=dict(remaining=remaining)))
            raise NoMoreCombinationsError(
                _("Cannot create another round: no more possible combinations!"))
        return newturn

    def _makeNextAAATurn(self, competitors, done):
        "Mechanically generate next turn out of all possible matches."

        nextround = []
        playing = set()

        ncompetitors = len(competitors)
        for c1, c2 in combinations(competitors, 2):
            if (c1, c2) not in done and c1 not in playing and c2 not in playing:
                nextround.append((c1, c2))
                playing.add(c1)
                playing.add(c2)
                if len(playing) == ncompetitors:
                    break

        return nextround

    def _makeNextKnockoutTurn(self, competitors):
        "Couple the first with the last, the second with the second-last and so on."

        nextround = []
        for c in range(len(competitors) // 2):
            nextround.append((competitors[c], competitors[-(c+1)]))

        return nextround

    def _countRemainingMatches(self, competitors, done):
        remaining = 0
        playing = set()

        for c1, c2 in combinations(competitors, 2):
            if (c1, c2) not in done and c1 not in playing and c2 not in playing:
                remaining += 1
                playing.add(c1)
                playing.add(c2)

        return remaining

    def makeFinalTurn(self):
        "Generate the final matches."

        if self.prized:
            raise OperationAborted(_('Cannot generate final turn after prize-giving!'))

        if not self.finals:
            raise OperationAborted(_('Finals are not considered for this tourney!'))

        self.finalturns = True
        self.makeNextTurn()

    def _makeNextFinalTurn(self):
        from . import Match

        enough, nfinalturns, wins = self._areFinalTurnsEnoughForPrizing()
        if enough:  # pragma: no cover
            raise OperationAborted(_('No further final matches are needed!!'))

        ranking = self.ranking
        newturn = self.currentturn + 1
        boardno = 1

        for final in range(self.finals):
            c1 = ranking[final*2]
            c2 = ranking[final*2 + 1]
            if wins.get(c1, 0) < 2 and wins.get(c2, 0) < 2:
                self.matches.append(Match(turn=newturn, board=boardno, final=True,
                                          competitor1=c1, competitor2=c2,
                                          score1=0, score2=0))
                boardno += 1

        return newturn

    def assignPrizes(self):
        """Consolidate final points."""

        if self.prized:  # pragma: nocover
            raise OperationAborted(_('Cannot update prizes after prize-giving!'))

        cturn = self.currentturn

        if cturn and cturn != self.rankedturn:  # pragma: nocover
            raise OperationAborted(_('The ranking is not up-to-date!'))

        kind = (self.championship.prizes.capitalize()
                if self.championship.prizes else "Fixed")

        name = "_assign%sPrizes" % kind

        try:
            method = getattr(self, name)
        except AttributeError:  # pragma: nocover
            raise AttributeError("No %r method to assign prizes with" % kind)

        method()

        self.prized = True
        self.modified = func.now()

        if self.rating is not None and self.rating.shouldConsiderTourney(self):
            self.rating.recompute(self.date)

        logger.info('Assigned final prizes for %r', self)

    def _assignAsisPrizes(self):
        "Assign decreasing integer numbers as final prizes, down to 1 to the last competitor."

        prize = len(self.ranking)
        for c in self.ranking:
            c.prize = prize
            prize -= 1

    def _assignFixedPrizes(self, prizes=None):
        "Assign fixed prizes to the first 16 competitors."

        if prizes is None:
            # This is what Scarry used to do.
            prizes = [18, 16, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

        for c in self.ranking:
            if prizes:
                prize = prizes.pop(0)
            else:
                prize = 0
            c.prize = prize

    def _assignFixed40Prizes(self):
        "Assign fixed prizes to the first 40 competitors."

        # This is the Francesco Beltrami's series of prizes, used
        # in the 2009-2010 italian national championship.
        self._assignFixedPrizes(prizes=[
            1000, 900, 800, 750, 700, 650, 600, 550, 500, 450,
            400, 375, 350, 325, 300, 275, 250, 225, 200, 175,
            150, 140, 130, 120, 110, 100, 90, 80, 70, 60,
            50, 40, 35, 30, 25, 20, 15, 10, 5, 1])

    def _assignMillesimalPrizes(self):
        "Assign 1000 points to the winner stepping down in fixed amount."

        # This is how the FIC currently assigns the prizes.

        ranking = self.ranking
        prize = 1000
        fraction = prize // len(ranking)
        for c in ranking:
            c.prize = prize
            prize -= fraction

    def _assignCentesimalPrizes(self):
        "Assigns 100 to the winner, 1 to the last, linear interpolation to the others."

        # This was suggested by Carlito

        ranking = self.ranking
        prize = 100.0
        fraction = (prize - 1) / (len(ranking) - 1)
        for c in ranking:
            c.prize = round(prize, 2)
            prize -= fraction

    def resetPrizes(self):
        """Reset assigned final points."""

        for c in self.competitors:
            c.prize = 0.0

        self.prized = False
        self.modified = func.now()
        if self.rating is not None and self.rating.shouldConsiderTourney(self):
            self.rating.recompute(self.date)

    def replay(self, date, newidowner=None):
        """Clone this tourney, creating new one at given date.

        Of the original, only the competitors are copied. This is particularly useful for
        doubles (or team), so that the players get copied in the same order.
        """

        from . import Competitor, Championship

        new = Tourney(idrating=self.idrating,
                      idowner=newidowner,
                      date=date,
                      description=gettext('Replica of $tourney',
                                          mapping=dict(tourney=self.description)),
                      location=self.location,
                      duration=self.duration,
                      prealarm=self.prealarm,
                      couplings=self.couplings,
                      system=self.system,
                      delaytoppairing=self.delaytoppairing,
                      delaycompatriotpairing=self.delaycompatriotpairing,
                      phantomscore=self.phantomscore,
                      retirements=self.retirements,
                      finals=self.finals,
                      finalkind=self.finalkind)

        if not self.championship.closed:
            championship = self.championship
        else:
            s = object_session(self)
            championship = s.query(Championship).filter_by(
                idclub=self.championship.idclub,
                playersperteam=self.championship.playersperteam,
                closed=False).first()
            if championship is None:
                raise OperationAborted(
                    _('Cannot replicate tourney, no open championships!'))

        championship.tourneys.append(new)

        append = new.competitors.append
        for c in self.competitors:
            append(Competitor(player1=c.player1,
                              player2=c.player2,
                              player3=c.player3,
                              player4=c.player4))
        return new

    def createKnockout(self, date, ncompetitors, newidowner=None):
        """Create a "knockout" tourney with `ncompetitors` top players."""

        from . import Competitor, Championship

        if int(log2(ncompetitors)) != log2(ncompetitors):  # pragma: no cover
            raise OperationAborted(_('For a knockout tourney there must be a power-of-two'
                                     ' number of competitors!'))

        if len(self.competitors) < ncompetitors:  # pragma: no cover
            raise OperationAborted(_('There are only $n competitors in the tourney!',
                                     mapping=dict(n=len(self.competitors))))

        new = Tourney(idrating=self.idrating,
                      idowner=newidowner,
                      date=date,
                      description=gettext('Knockout of $tourney',
                                          mapping=dict(tourney=self.description)),
                      location=self.location,
                      duration=self.duration,
                      prealarm=self.prealarm,
                      couplings='seeds',
                      system='knockout',
                      delaytoppairing=self.delaytoppairing,
                      delaycompatriotpairing=self.delaycompatriotpairing,
                      phantomscore=self.phantomscore,
                      retirements=self.retirements,
                      finals=self.finals,
                      finalkind=self.finalkind)

        if not self.championship.closed:
            championship = self.championship
        else:
            s = object_session(self)
            championship = s.query(Championship).filter_by(
                idclub=self.championship.idclub,
                playersperteam=self.championship.playersperteam,
                closed=False).first()
            if championship is None:
                raise OperationAborted(
                    _('Cannot replicate tourney, no open championships!'))

        championship.tourneys.append(new)

        append = new.competitors.append
        for i, c in enumerate(self.ranking, 1):
            if i > ncompetitors:
                break
            append(Competitor(player1=c.player1,
                              player2=c.player2,
                              player3=c.player3,
                              player4=c.player4,
                              position=i))

        return new

    def serialize(self, serializer):
        """Reduce a single tourney to a simple dictionary.

        :param serializer: a :py:class:`.Serializer` instance
        :rtype: dict
        :returns: a plain dictionary containing a flatified view of this tourney
        """

        from operator import attrgetter

        simple = {}
        simple['guid'] = self.guid
        simple['modified'] = self.modified
        simple['championship'] = serializer.addChampionship(self.championship)
        if self.idhostingclub:
            simple['hosting_club'] = serializer.addClub(self.hosting_club)
        if self.idrating:
            simple['rating'] = serializer.addRating(self.rating)
        if self.idowner:
            simple['owner'] = serializer.addUser(self.owner)
        simple['description'] = self.description
        simple['date'] = self.date
        if self.location:
            simple['location'] = self.location
        if self.socialurl:
            simple['socialurl'] = self.socialurl
        simple['currentturn'] = self.currentturn
        simple['rankedturn'] = self.rankedturn
        simple['prized'] = self.prized
        simple['couplings'] = self.couplings
        simple['delaytoppairing'] = self.delaytoppairing
        simple['delaycompatriotpairing'] = self.delaycompatriotpairing
        simple['duration'] = self.duration
        simple['prealarm'] = self.prealarm
        simple['phantomscore'] = self.phantomscore
        simple['retirements'] = self.retirements
        if self.finals is not None:
            simple['finals'] = self.finals
        if self.finalturns:
            simple['finalturns'] = self.finalturns
        simple['finalkind'] = self.finalkind

        cmap = {None: None}
        ctors = simple['competitors'] = []

        # Sort competitors by first player name, to aid the tests
        fullname = attrgetter('player1.lastname', 'player1.firstname')
        for i, c in enumerate(sorted(self.competitors, key=fullname), 1):
            cmap[c.idcompetitor] = i
            sctor = c.serialize(serializer)
            ctors.append(sctor)

        matches = simple['matches'] = []
        for m in self.matches:
            sm = m.serialize(serializer, cmap)
            matches.append(sm)

        return simple

    def sendTrainingURLs(self, request):
        if not self.championship.trainingboards:  # pragma: nocover
            raise OperationAborted(_('Not a training tournament!'))

        if self.couplings == 'all':
            byp = {}
            for m in self.matches:
                pm = byp.setdefault(m.competitor1.player1, [])
                pm.append((m, 1, m.competitor2.player1 if m.competitor2 is not None else None))
                if m.competitor2 is not None:
                    pm = byp.setdefault(m.competitor2.player1, [])
                    pm.append((m, 2, m.competitor1.player1))
            for p in byp:
                p.sendTrainingURLs(request, byp[p])
        else:
            for m in self.matches:
                if m.turn == self.currentturn:
                    m.competitor1.player1.sendTrainingURL(request, m, 1,
                                                          m.competitor2.player1
                                                          if m.competitor2 is not None
                                                          else None)
                    if m.competitor2 is not None:
                        m.competitor2.player1.sendTrainingURL(request, m, 2,
                                                              m.competitor1.player1)

    def getEditBoardURL(self, request, boardno):
        settings = request.registry.settings
        s = Signer(settings['sol.signer_secret_key'])
        signed_board = s.sign('%d-%d' % (self.idtourney, boardno)).decode('ascii')
        return request.route_url('match_form', board=signed_board)
