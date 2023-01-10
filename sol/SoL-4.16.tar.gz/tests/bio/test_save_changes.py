# -*- coding: utf-8 -*-
# :Project:   SoL -- save_changes() tests
# :Created:   sab 07 lug 2018 07:31:07 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018, 2019, 2020 Lele Gaifax
#

from os.path import exists, join
from tempfile import gettempdir

import pytest

from sol.models import Competitor, Match, Player, Tourney, User
from sol.models.bio import save_changes
from sol.models.errors import OperationAborted


def test_insert_user(session):
    # email is missing
    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(firstname='New',
                            lastname='user',
                            password='test')),
        ], [])
    assert 'are mandatory' in str(e.value)

    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(firstname='New',
                            lastname='user',
                            password='test',
                            email='')),
        ], [])
    assert 'are mandatory' in str(e.value)

    # weak password
    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(firstname='New',
                            lastname='user',
                            email='user@example.com',
                            password='test')),
        ], [])
    assert 'Password' in str(e.value) and 'weak' in str(e.value)

    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(firstname='New',
                            lastname='User',
                            email='admin',
                            password='tst123')),
        ], [])
    assert 'is reserved' in str(e.value)

    i, m, d = save_changes(session, None, [
        ('iduser', dict(firstname='New ',
                        lastname='user ',
                        email='user@example.com ',
                        password='tst123')),
    ], [])
    assert len(i) == 1
    assert len(m) == 0
    assert len(d) == 0

    new = session.query(User).get(i[0]['iduser'])
    assert new.firstname == 'New'
    assert new.lastname == 'User'
    assert new.email == 'user@example.com'
    assert new.password and new.password != 'tst123'

    # Dup email
    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(firstname='New',
                            lastname='Again',
                            email='user@example.com',
                            password='test123')),
        ], [])
    assert 'already exists' in str(e.value)


def test_modify_user(session):
    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(iduser=1,
                            lastname='')),
        ], [])
    assert 'cannot be empty' in str(e.value)

    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(iduser=1,
                            firstname='')),
        ], [])
    assert 'cannot be empty' in str(e.value)

    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(iduser=1,
                            email='')),
        ], [])
    assert 'provide a valid "email"' in str(e.value)

    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(iduser=1,
                            password='test')),
        ], [])
    assert 'Password is too weak' in str(e.value)

    with pytest.raises(OperationAborted) as e:
        save_changes(session, None, [
            ('iduser', dict(iduser=1,
                            email='admin')),
        ], [])
    assert 'is reserved' in str(e.value)

    i, m, d = save_changes(session, None, [
        ('iduser', dict(iduser=1,
                        email='user@example.com ',
                        password='tst123')),
    ], [])
    assert len(i) == 0
    assert len(m) == 1
    assert len(d) == 0

    session.expunge_all()
    chg = session.query(User).get(1)
    assert chg.password is not None and chg.password != 'test'
    assert chg.email == 'user@example.com'


def test_bad_player_name(session, fake_admin_request):
    with pytest.raises(OperationAborted) as e:
        save_changes(session, fake_admin_request, [
            ('idplayer', dict(firstname='New',
                              lastname=' ')),
        ], [])
    assert 'lastname' in str(e.value) and 'mandatory' in str(e.value)

    with pytest.raises(OperationAborted) as e:
        save_changes(session, fake_admin_request, [
            ('idplayer', dict(firstname=' ',
                              lastname=' ')),
        ], [])
    assert 'lastname' in str(e.value) and 'mandatory' in str(e.value)

    with pytest.raises(OperationAborted) as e:
        save_changes(session, fake_admin_request, [
            ('idplayer', dict(idplayer=1,
                              firstname=' ')),
        ], [])
    assert 'cannot be empty' in str(e.value)

    with pytest.raises(OperationAborted) as e:
        save_changes(session, fake_admin_request, [
            ('idplayer', dict(idplayer=1,
                              lastname=' ')),
        ], [])
    assert 'cannot be empty' in str(e.value)


def test_bad_description(session, fake_admin_request):
    for key in ('idchampionship', 'idclub', 'idrating', 'idtourney'):
        with pytest.raises(OperationAborted) as e:
            save_changes(session, None, [(key, {'description': ' '})], [])
        assert 'description' in str(e.value) and 'mandatory' in str(e.value)
        session.rollback()

        with pytest.raises(OperationAborted) as e:
            save_changes(session, fake_admin_request,
                         [(key, {key: 1, 'description': ' '})], [])
        assert 'description' in str(e.value) and 'cannot be empty' in str(e.value)

    for key in ('idchampionship', 'idclub', 'idrating', 'idtourney'):
        with pytest.raises(OperationAborted) as e:
            save_changes(session, None, [(key, {'guid': 'bar'})], [])
        assert 'description' in str(e.value) and 'mandatory' in str(e.value)
        session.rollback()


def test_delete(session, fake_admin_request):
    # player is playing!
    with pytest.raises(OperationAborted) as e:
        save_changes(session, fake_admin_request, [], [('idplayer', 1)])
    assert 'not allowed' in str(e.value) and 'is a competitor' in str(e.value)

    with pytest.raises(OperationAborted):
        save_changes(session, None, [
            ('idplayer', dict(firstname='New',
                              lastname='user',
                              nickname='test',
                              email='user@example.com',
                              password='tst123')),
        ], [])

    i, m, d = save_changes(session, fake_admin_request, [
        ('idplayer', dict(firstname='New',
                          lastname='user',
                          nickname='test',
                          email='user@example.com',
                          password='tst123')),
    ], [])
    assert len(i) == 1
    assert len(m) == 0
    assert len(d) == 0

    tbdid = i[0]['idplayer']
    i, m, d = save_changes(session, fake_admin_request, [], [('idplayer', tbdid)])
    session.flush()
    assert len(i) == 0
    assert len(m) == 0
    assert len(d) == 1

    session.expunge_all()
    deleted = session.query(Player).get(tbdid)
    assert deleted is None

    # user owns something!
    with pytest.raises(OperationAborted) as e:
        save_changes(session, fake_admin_request, [], [('iduser', 1)])
    assert 'not allowed' in str(e.value) and 'owns' in str(e.value)


def test_upload_portrait(session, fake_admin_request):
    img = ("data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
           "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
           "9TXL0Y4OHwAAAABJRU5ErkJggg==")

    with pytest.raises(OperationAborted):
        save_changes(session, None, [
            ('idplayer', dict(idplayer=1, image=img, portrait='bar.jpeg')),
        ], [])

    basedir = fake_admin_request.registry.settings['sol.portraits_dir']
    i, m, d = save_changes(session, fake_admin_request, [
        ('idplayer', dict(idplayer=1, image=img, portrait='bar.jpeg')),
    ], [])
    assert len(i) == 0
    assert len(m) == 1
    assert len(d) == 0

    assert exists(join(basedir, 'b60ab2708daec7685f3d412a5e05191a.jpeg'))

    i, m, d = save_changes(session, fake_admin_request, [
        ('idplayer', dict(idplayer=1, portrait=None)),
    ], [])
    assert len(i) == 0
    assert len(m) == 1
    assert len(d) == 0

    assert not exists(join(basedir, 'b60ab2708daec7685f3d412a5e05191a.jpeg'))


def test_upload_emblem(session):
    basedir = gettempdir()

    img = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
           "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
           "9TXL0Y4OHwAAAABJRU5ErkJggg==")

    i, m, d = save_changes(session, None, [
        ('idclub', dict(idclub=1, image=img, emblem='foo.png')),
    ], [])
    assert len(i) == 0
    assert len(m) == 1
    assert len(d) == 0

    assert exists(join(basedir, 'b60ab2708daec7685f3d412a5e05191a.png'))

    i, m, d = save_changes(session, None, [
        ('idclub', dict(idclub=1, emblem=None)),
    ], [])
    assert len(i) == 0
    assert len(m) == 1
    assert len(d) == 0

    assert not exists(join(basedir, 'b60ab2708daec7685f3d412a5e05191a.png'))

    i, m, d = save_changes(session, None, [
        ('idclub', dict(idclub=0, description="New test club", image=img, emblem='foo.png')),
    ], [])
    assert len(i) == 1
    assert len(m) == 0
    assert len(d) == 0

    assert exists(join(basedir, 'b60ab2708daec7685f3d412a5e05191a.png'))


def test_insert_and_modify(session, tourney_double, player_lele, player_bob, player_fata):
    tid = tourney_double.idtourney
    lid = player_lele.idplayer
    bid = player_bob.idplayer
    fid = player_fata.idplayer

    leleteam = session.query(Competitor).filter_by(idtourney=tid, idplayer1=lid).one()

    i, m, d = save_changes(session, None, [
        ('idcompetitor', dict(idcompetitor=0,
                              idtourney=tid,
                              idplayer1=bid,
                              idplayer2=fid)),
        ('idcompetitor', dict(idcompetitor=leleteam.idcompetitor,
                              idplayer2=None))
        ], [])
    assert len(i) == 1
    assert len(m) == 1
    assert len(d) == 0

    session.expunge_all()

    t = session.query(Tourney).get(tid)
    competitors = t.competitors
    assert len(competitors) == 3

    for c in competitors:
        if c.player1.idplayer == lid:
            assert c.idplayer2 is None
        elif c.player1.idplayer == bid:
            assert c.player2.idplayer == fid


def test_modify_match_boards(session, tourney_first):
    lastmatch = tourney_first.matches[-1]
    assert not lastmatch.boards

    mid = lastmatch.idmatch
    i, m, d = save_changes(session, None, [
        ('idmatch', dict(idmatch=mid,
                         coins1_1=1,
                         queen_1='2')),
    ], [])
    assert len(i) == 0
    assert len(m) == 1

    session.expunge_all()

    m = session.query(Match).get(mid)
    assert len(m.boards) == 1
    assert m.boards[0].coins1 == 1
    assert m.boards[0].queen == '2'

    i, m, d = save_changes(session, None, [
        ('idmatch', dict(idmatch=mid,
                         coins1_2=1,
                         queen_2='2')),
    ], [])
    assert len(i) == 0
    assert len(m) == 1

    session.expunge_all()

    m = session.query(Match).get(mid)
    assert len(m.boards) == 2
    assert m.boards[0].coins1 == 1
    assert m.boards[0].queen == '2'
    assert m.boards[1].coins1 == 1
    assert m.boards[1].queen == '2'

    i, m, d = save_changes(session, None, [
        ('idmatch', dict(idmatch=mid,
                         coins1_4=1,
                         queen_4='2')),
    ], [])
    assert len(i) == 0
    assert len(m) == 1

    session.expunge_all()

    m = session.query(Match).get(mid)
    assert len(m.boards) == 4
