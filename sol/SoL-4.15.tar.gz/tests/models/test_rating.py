# -*- coding: utf-8 -*-
# :Project:   SoL -- Rating entity tests
# :Created:   ven 06 lug 2018 16:21:11 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Lele Gaifax
#

from datetime import date, timedelta
from decimal import Decimal
from operator import attrgetter

from sol.models import Competitor, Player, Rating, Tourney


def test_owned(rating_standalone, user_lele):
    assert rating_standalone.owner is user_lele


def test_mu(player_lele, rating_national):
    latest = rating_national.getPlayerRating(player_lele)
    assert latest.mu == 1505

    previous = rating_national.getPlayerRating(player_lele, date(2018, 7, 6))
    assert previous.mu == 1000


def test_level(player_varechina, rating_national, rating_standalone):
    rate = rating_national.getPlayerRating(player_varechina)
    assert rate.mu == 1300

    rate = rating_standalone.getPlayerRating(player_varechina)
    assert rate.mu == 1200


def test_competitor(session, player_lele, tourney_rated):
    fourp = iter(session.query(Player).limit(4))
    c = tourney_rated.competitors[0]
    assert c.player1 is player_lele
    assert c.rate == 1505

    newt = Tourney(date=tourney_rated.date + timedelta(days=10),
                   championship=tourney_rated.championship,
                   description='dummy',
                   rating=tourney_rated.rating)
    newc = Competitor(tourney=newt)
    newc.player1 = next(fourp)
    newc.player2 = next(fourp)
    newc.player3 = next(fourp)
    newc.player4 = next(fourp)
    session.add(newt)
    session.flush()

    assert newc.rate is not None


def test_first_turn(tourney_rated_empty, player_fabiot, player_lucab):
    assert tourney_rated_empty.matches == []
    tourney_rated_empty.makeNextTurn()
    assert len(tourney_rated_empty.matches) == (len(tourney_rated_empty.competitors) + 1) // 2
    fm = tourney_rated_empty.matches[0]
    assert fm.turn == 1
    assert fm.competitor1.player1 is player_fabiot
    assert fm.competitor2.player1 is player_lucab


def test_first_turn_odd(tourney_rated_empty_odd):
    t = tourney_rated_empty_odd
    assert t.matches == []
    byrevrate = list(sorted(t.competitors, key=attrgetter('rate'), reverse=True))
    assert not any(c.rate == 1500 for c in t.competitors)
    t.makeNextTurn()
    assert len(t.matches) == (len(t.competitors) + 1) // 2
    fm = t.matches[0]
    assert fm.turn == 1
    assert fm.competitor1.player1 is byrevrate[0].player1
    assert fm.competitor2.player1 is byrevrate[3].player1
    fm = t.matches[1]
    assert fm.competitor1.player1 is byrevrate[1].player1
    assert fm.competitor2.player1 is byrevrate[4].player1
    fm = t.matches[2]
    assert fm.competitor1.player1 is byrevrate[2].player1
    assert fm.competitor2.player1 is byrevrate[5].player1
    fm = t.matches[3]
    assert fm.competitor1.player1 is byrevrate[6].player1
    assert fm.competitor2 is None  # Phantom


def test_ranking(rating_national, player_picol, player_varechina):
    ranking = rating_national.ranking
    assert ranking[0][0] is player_picol
    assert ranking[0][1] == 1700
    assert ranking[-1][0] is player_varechina
    assert ranking[-1][1] == 1200


def test_timespan(rating_european):
    assert rating_european.time_span == (date(2018, 7, 4), date(2018, 7, 6))


def test_outcomes():
    for oc in ('glicko', 'guido', 'expds'):
        r = Rating(outcomes=oc)
        compute_outcomes = getattr(r, "_compute%sOutcomes" % oc.capitalize())
        assert compute_outcomes(25, 0) == (1, 0)
        assert compute_outcomes(0, 25) == (0, 1)
        for s in range(26):
            assert compute_outcomes(s, s) == (0.5, 0.5)


def test_recompute(tourney_rated):
    tourney_rated.updateRanking()
    tourney_rated.assignPrizes()

    c = tourney_rated.competitors[0]
    r = tourney_rated.rating.getPlayerRating(c.player1)
    assert r.rate == 1492
    assert r.deviation == 151
    assert r.volatility == Decimal('0.05999')


def test_recompute_exponential(tourney_rated_exponential):
    tourney_rated_exponential.updateRanking()
    ranking = tourney_rated_exponential.ranking
    assert len(ranking) == 2
    tourney_rated_exponential.assignPrizes()
    c = tourney_rated_exponential.competitors[0]
    r = tourney_rated_exponential.rating.getPlayerRating(c.player1)
    assert r.rate == 1595
