# -*- coding: utf-8 -*-
# :Project:   SoL -- Tests for /svg/* views
# :Created:   sab 07 lug 2018 18:01:18 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018, 2019 Lele Gaifax
#

import pytest

from sqlalchemy import and_, select
from webtest.app import AppError

from sol.models import Competitor, Match, Player


def test_rating(guest_user, rating_european):
    app = guest_user
    response = app.get_route('ratings')
    result = response.json
    assert result['success'] is True
    assert result['message'] == "Ok"
    assert result['root'][0]['description'] == rating_european.description

    idrating = result['root'][0]['idrating']
    guidrating = result['root'][0]['guid']

    response = app.get_route('rated_players', _query=dict(filter_by_idrating=idrating))
    result = response.json

    idp1 = result['root'][0]['idplayer']
    idp2 = result['root'][1]['idplayer']
    idp3 = result['root'][2]['idplayer']
    idp4 = result['root'][3]['idplayer']
    guidp1 = result['root'][0]['guid']
    guidp2 = result['root'][1]['guid']
    guidp3 = result['root'][2]['guid']
    guidp4 = result['root'][3]['guid']

    response = app.get_route('svg_ratingchart', id=idrating,
                             _query=(('idplayer', idp) for idp in (idp1, idp2, idp3, idp4)))
    assert response.text.startswith('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<svg')

    response = app.get_route('svg_ratingchart', id=guidrating,
                             _query=(('player', uidp)
                                     for uidp in (guidp1, guidp2, guidp3, guidp4)))
    assert response.text.startswith('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<svg')


def test_bad_rating(guest_user):
    app = guest_user
    with pytest.raises(AppError) as e:
        app.get_route('svg_ratingchart', id='aaaa')
    assert '400 Bad Request' in str(e.value)

    with pytest.raises(AppError) as e:
        app.get_route('svg_ratingchart', id='999999')
    assert '400 Bad Request' in str(e.value)


def test_players_distribution(guest_user):
    app = guest_user
    response = app.get_route('svg_playersdist')
    assert response.text.startswith('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<svg')


def test_opponents(session, guest_user):
    app = guest_user
    mt = Match.__table__
    ct1 = Competitor.__table__.alias('c1')
    ct2 = Competitor.__table__.alias('c2')
    pt1 = Player.__table__.alias('p1')
    pt2 = Player.__table__.alias('p2')
    q = select([pt1.c.guid, pt2.c.guid],
               and_(ct1.c.idplayer1 == pt1.c.idplayer,
                    ct2.c.idplayer1 == pt2.c.idplayer,
                    mt.c.idcompetitor1 == ct1.c.idcompetitor,
                    mt.c.idcompetitor2 == ct2.c.idcompetitor))
    r = session.execute(q).first()
    response = app.get_route('svg_player_opponent', guid=r[0], opponent=r[1])
    assert response.text.startswith('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<svg')

    with pytest.raises(AppError) as e:
        app.get_route('svg_player_opponent', guid=r[0], opponent='bbbb')
    assert '400 Bad Request' in str(e.value)

    with pytest.raises(AppError) as e:
        app.get_route('svg_player_opponent', guid='aaaa', opponent=r[1])
    assert '400 Bad Request' in str(e.value)
