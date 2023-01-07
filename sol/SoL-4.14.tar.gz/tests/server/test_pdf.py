# -*- coding: utf-8 -*-
# :Project:   SoL -- Tests for /pdf/* views
# :Created:   sab 07 lug 2018 19:06:51 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018, 2020 Lele Gaifax
#

from datetime import datetime
from random import randint

import pytest
import transaction
from webtest.app import AppError

from metapensiero.sqlalchemy.proxy.json import JSON


@pytest.fixture
def tourney_prized(session, tourney_rated):
    if not tourney_rated.prized:
        with transaction.manager:
            tourney_rated.updateRanking()
            for i, (scorer, points) in enumerate((('score2', 10),
                                                  ('score1', 10),
                                                  ('score2', 20))):
                tourney_rated.makeFinalTurn()
                finals = [m for m in tourney_rated.matches if m.final]
                setattr(finals[i], scorer, points)
                tourney_rated.updateRanking()
            session.flush()

    return tourney_rated


@pytest.fixture
def tourney_asis_prized(session, tourney_asis):
    if not tourney_asis.prized:
        with transaction.manager:
            tourney_asis.updateRanking()
            tourney_asis.assignPrizes()
            session.flush()

    return tourney_asis


@pytest.fixture
def tourney_skipworstprize_prized(session, tourney_skipworstprize):
    if not tourney_skipworstprize.prized:
        with transaction.manager:
            tourney_skipworstprize.updateRanking()
            tourney_skipworstprize.assignPrizes()
            session.flush()

    return tourney_skipworstprize


@pytest.fixture
def tourney_closed_prized(session, tourney_closed):
    t = tourney_closed
    if not t.prized:
        with transaction.manager:
            for turn in range(1, 4):
                t.makeNextTurn()
                for m in t.matches:
                    if m.turn == turn:
                        m.score1 = randint(1, 25)
                        m.score2 = randint(1, 25)
                t.updateRanking()
            t.assignPrizes()
            session.flush()

    return t


@pytest.fixture
def tourney_knockout_played(session, tourney_knockout):
    for i in range(1, 7):
        tourney_knockout.updateRanking()
        tourney_knockout.makeNextTurn()
        for m in tourney_knockout.matches:
            if m.turn == i:
                m.score1 = 10
                m.score2 = 5
        session.flush()
    return tourney_knockout


def test_boardlabels(guest_user, tourney_knockout):
    app = guest_user

    app.get_route('pdf_boardlabels', id=tourney_knockout.idtourney)


def test_participants(guest_user, tourney_prized, tourney_simple):
    app = guest_user

    app.get_route('pdf_participants', id=tourney_prized.idtourney)
    app.get_route('pdf_participants', id=tourney_prized.guid)

    app.get_route('pdf_participants', id=tourney_simple.idtourney)


def test_ranking(guest_user, tourney_prized, tourney_apr24, tourney_asis_prized,
                 tourney_double, tourney_simple):
    app = guest_user

    app.get_route('pdf_tourneyranking', id=tourney_prized.idtourney)
    app.get_route('pdf_tourneyranking', id=tourney_prized.guid)

    app.get_route('pdf_tourneyranking', id=tourney_apr24.idtourney)
    app.get_route('pdf_tourneyranking', id=tourney_apr24.idtourney, _query={'turn': 1})

    app.get_route('pdf_tourneyranking', id=tourney_asis_prized.idtourney)
    app.get_route('pdf_tourneyranking', id=tourney_asis_prized.idtourney, _query={'turn': 1})

    app.get_route('pdf_tourneyranking', id=tourney_double.idtourney)
    app.get_route('pdf_tourneyranking', id=tourney_simple.idtourney)

    with pytest.raises(AppError):
        app.get_route('pdf_tourneyranking', id=tourney_apr24.idtourney, _query={'turn': 'foo'})


def test_under_ranking(guest_user, tourney_prized, tourney_apr24, tourney_asis):
    app = guest_user

    app.get_route('pdf_tourneyunderranking', id=tourney_prized.idtourney,
                  _query={'age': 69})
    app.get_route('pdf_tourneyunderranking', id=tourney_prized.guid,
                  _query={'age': 69})

    app.get_route('pdf_tourneyunderranking', id=tourney_apr24.idtourney,
                  _query={'age': 69})
    app.get_route('pdf_tourneyunderranking', id=tourney_apr24.idtourney,
                  _query={'age': 69, 'turn': 1})

    app.get_route('pdf_tourneyunderranking', id=tourney_asis.idtourney)

    with pytest.raises(AppError):
        app.get_route('pdf_tourneyunderranking', id=tourney_apr24.idtourney,
                      _query={'turn': 'foo'})

    with pytest.raises(AppError):
        app.get_route('pdf_tourneyunderranking', id=tourney_apr24.idtourney,
                      _query={'age': 'foo'})


def test_women_ranking(guest_user, tourney_prized, tourney_apr24, tourney_asis):
    app = guest_user

    app.get_route('pdf_tourneywomenranking', id=tourney_prized.idtourney,
                  _query={'age': 69})
    app.get_route('pdf_tourneywomenranking', id=tourney_prized.guid,
                  _query={'age': 69})

    app.get_route('pdf_tourneywomenranking', id=tourney_apr24.idtourney,
                  _query={'age': 69})
    app.get_route('pdf_tourneywomenranking', id=tourney_apr24.idtourney,
                  _query={'age': 69, 'turn': 1})

    app.get_route('pdf_tourneywomenranking', id=tourney_asis.idtourney)

    with pytest.raises(AppError):
        app.get_route('pdf_tourneywomenranking', id=tourney_apr24.idtourney,
                      _query={'turn': 'foo'})


def test_nationalranking(guest_user, tourney_first, tourney_double, tourney_prized,
                         tourney_apr24, tourney_simple):
    app = guest_user

    app.get_route('pdf_nationalranking', id=tourney_first.idtourney)
    app.get_route('pdf_nationalranking', id=tourney_double.idtourney)

    app.get_route('pdf_nationalranking', id=tourney_prized.idtourney)
    app.get_route('pdf_nationalranking', id=tourney_prized.guid)

    app.get_route('pdf_nationalranking', id=tourney_apr24.idtourney)
    app.get_route('pdf_nationalranking', id=tourney_apr24.idtourney, _query={'turn': 1})

    app.get_route('pdf_nationalranking', id=tourney_simple.idtourney)

    with pytest.raises(AppError):
        app.get_route('pdf_nationalranking', id=tourney_apr24.idtourney,
                      _query={'turn': 'foo'})


def test_results(guest_user, tourney_prized, tourney_simple):
    app = guest_user

    app.get_route('pdf_results', id=tourney_prized.idtourney)
    app.get_route('pdf_results', id=tourney_prized.guid)
    app.get_route('pdf_results', id=tourney_prized.idtourney, _query={'turn': 0})
    app.get_route('pdf_results', id=tourney_prized.guid, _query={'turn': 0})
    app.get_route('pdf_results', id=tourney_prized.idtourney, _query={'turn': 'all'})
    app.get_route('pdf_results', id=tourney_prized.guid, _query={'turn': 'all'})
    app.get_route('pdf_results', id=tourney_simple.idtourney)
    with pytest.raises(AppError):
        app.get_route('pdf_results', id=tourney_prized.idtourney, _query={'turn': 'foo'})


def test_results_knockout(guest_user, tourney_knockout_played):
    guest_user.get_route('pdf_results', id=tourney_knockout_played.idtourney,
                         _query={'turn': 'all'})


def test_matches(guest_user, tourney_double, tourney_odd, tourney_prized):
    app = guest_user

    app.get_route('pdf_matches', id=tourney_double.idtourney)
    app.get_route('pdf_matches', id=tourney_odd.idtourney)
    app.get_route('pdf_matches', id=tourney_prized.idtourney)
    app.get_route('pdf_matches', id=tourney_prized.guid)
    app.get_route('pdf_matches', id=tourney_prized.idtourney, _query={'turn': 1})
    app.get_route('pdf_matches', id=tourney_prized.guid, _query={'turn': 1})
    with pytest.raises(AppError):
        app.get_route('pdf_matches', id=tourney_prized.idtourney, _query={'turn': 'foo'})


def test_scorecards(guest_user, tourney_prized, tourney_closed_prized):
    app = guest_user

    app.get_route('pdf_scorecards', id='blank')
    app.get_route('pdf_scorecards', id=tourney_prized.idtourney)
    app.get_route('pdf_scorecards', id=tourney_closed_prized.guid)
    app.get_route('pdf_scorecards', id=tourney_prized.guid,
                  _query={'starttime': datetime.now().timestamp()})
    app.get_route('pdf_scorecards', id=tourney_prized.guid,
                  _query={'starttime': int(datetime.now().timestamp() * 1000)})
    with pytest.raises(AppError):
        app.get_route('pdf_scorecards', id=tourney_prized.guid,
                      _query={'starttime': 'foo'})
    with pytest.raises(AppError):
        app.get_route('pdf_scorecards', id='foo')
    with pytest.raises(AppError):
        app.get_route('pdf_scorecards', id=-1)


def test_badges(guest_user, tourney_prized, tourney_apr24, tourney_asis_prized,
                tourney_closed, tourney_simple):
    app = guest_user

    app.get_route('pdf_badges', id=tourney_prized.idtourney)
    app.get_route('pdf_badges', id=tourney_prized.guid)

    app.get_route('pdf_badges', id=tourney_apr24.idtourney)
    app.get_route('pdf_badges', id=tourney_apr24.guid)

    app.get_route('pdf_badges', id=tourney_asis_prized.idtourney)

    app.get_route('pdf_badges', id=tourney_closed.idtourney)

    app.get_route('pdf_badges', id=tourney_simple.idtourney)

    with pytest.raises(AppError):
        app.get_route('pdf_badges', id='foo')
    with pytest.raises(AppError):
        app.get_route('pdf_badges', id=-1)


def test_badges_centesimal_prized(guest_user, tourney_closed_prized):
    app = guest_user
    app.get_route('pdf_badges', id=tourney_closed_prized.idtourney)


def test_badges_emblem(admin_user, tourney_closed_prized):
    img = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
           "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
           "9TXL0Y4OHwAAAABJRU5ErkJggg==")

    modified = [('idclub', dict(idclub=tourney_closed_prized.championship.club.idclub,
                                image=img,
                                emblem='foo.png'))]
    deleted = []
    admin_user.post_route(dict(modified_records=JSON.encode(modified),
                               deleted_records=JSON.encode(deleted)),
                          'save_changes')
    admin_user.get_route('pdf_badges', id=tourney_closed_prized.idtourney)


def test_championshipranking(guest_user, tourney_closed, tourney_double, tourney_prized,
                             tourney_skipworstprize_prized):
    app = guest_user

    app.get_route('pdf_championshipranking', id=tourney_closed.championship.idchampionship)
    app.get_route('pdf_championshipranking', id=tourney_double.championship.idchampionship)
    app.get_route('pdf_championshipranking', id=tourney_prized.championship.idchampionship)
    app.get_route('pdf_championshipranking', id=tourney_prized.championship.guid)
    app.get_route('pdf_championshipranking',
                  id=tourney_skipworstprize_prized.championship.guid)

    with pytest.raises(AppError):
        app.get_route('pdf_championshipranking', id='foo')
    with pytest.raises(AppError):
        app.get_route('pdf_championshipranking', id=-1)


def test_ratingranking(guest_user, tourney_prized):
    app = guest_user

    app.get_route('pdf_ratingranking', id=tourney_prized.rating.idrating)
    app.get_route('pdf_ratingranking', id=tourney_prized.rating.guid)
    with pytest.raises(AppError):
        app.get_route('pdf_ratingranking', id='foo')
    with pytest.raises(AppError):
        app.get_route('pdf_ratingranking', id=-1)
