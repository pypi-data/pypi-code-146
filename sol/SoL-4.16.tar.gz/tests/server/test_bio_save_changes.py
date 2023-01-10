# -*- coding: utf-8 -*-
# :Project:   SoL -- Tests /bio/saveChanges view
# :Created:   dom 08 lug 2018 08:30:12 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018, 2020 Lele Gaifax
#

from datetime import date
from pathlib import Path

import pytest

from metapensiero.sqlalchemy.proxy.json import JSON
from webtest.app import AppError

from sol.models import Club, Player


def test_admin_save_empty(admin_user):
    modified = []
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is True
    assert response.json['message'] == "Ok"


def test_admin_save_ok(admin_user, session, player_picol):
    modified = [('idplayer', dict(idplayer=player_picol.idplayer,
                                  lastname='Golin',
                                  nickname='picol'))]
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is True
    assert response.json['message'] == "Ok"

    session.expunge_all()
    juri = session.query(Player).get(player_picol.idplayer)
    assert juri.lastname == "Golin"
    assert juri.nickname == "picol"


def test_admin_save_emblem(admin_user, session, club_scr):
    img = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
           "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
           "9TXL0Y4OHwAAAABJRU5ErkJggg==")

    modified = [('idclub', dict(idclub=club_scr.idclub,
                                image=img,
                                emblem='foo.png'))]
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is True
    assert response.json['message'] == "Ok"

    settings = admin_user.app.registry.settings
    edir = Path(settings['sol.emblems_dir'])
    assert (edir / 'b60ab2708daec7685f3d412a5e05191a.png').exists()

    session.expunge_all()
    scr = session.query(Club).get(club_scr.idclub)
    assert scr.emblem == "b60ab2708daec7685f3d412a5e05191a.png"


def test_admin_save_portrait(admin_user, session, player_blond):
    img = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
           "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
           "9TXL0Y4OHwAAAABJRU5ErkJggg==")

    modified = [('idplayer', dict(idplayer=player_blond.idplayer,
                                  image=img,
                                  portrait='foo.png'))]
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is True
    assert response.json['message'] == "Ok"

    settings = admin_user.app.registry.settings
    pdir = Path(settings['sol.portraits_dir'])
    assert (pdir / 'b60ab2708daec7685f3d412a5e05191a.png').exists()

    session.expunge_all()
    blond = session.query(Player).get(player_blond.idplayer)
    assert blond.portrait == "b60ab2708daec7685f3d412a5e05191a.png"


def test_admin_save_cant_delete(admin_user, player_blond):
    modified = []
    deleted = [('idplayer', player_blond.idplayer)]
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is False
    assert "Deletion not allowed:" in response.json['message']


def test_admin_insert_ok(admin_user, session):
    modified = [('idplayer', dict(idplayer=0,
                                  lastname='Foo',
                                  firstname='bar',
                                  nickname='nick'))]
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is True
    assert response.json['message'] == "Ok"

    foo = session.query(Player).filter_by(lastname='Foo', firstname='bar').one()
    assert foo.firstname == "Bar"
    assert foo.nickname == "nick"


def test_admin_insert_missing_field(admin_user):
    modified = [('idplayer', dict(idplayer=0,
                                  lastname='Foo'))]
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is False
    assert "are mandatory" in response.json['message']

    modified = [('idclub', dict(idclub=0,
                                nationality='ITA'))]
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is False
    assert "is mandatory" in response.json['message']


def test_admin_insert_player_already_present(admin_user, player_lele):
    modified = [('idplayer', dict(idplayer=0,
                                  lastname=player_lele.lastname,
                                  firstname=player_lele.firstname))]
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is False
    assert "is already present" in response.json['message']

    modified = [('idplayer', dict(idplayer=0,
                                  lastname=player_lele.lastname,
                                  firstname=player_lele.firstname,
                                  nickname=player_lele.nickname))]
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is False
    assert "specify a different nickname to disambiguate" \
        in response.json['message']


def test_admin_insert_tourney_already_present(admin_user, tourney_first):
    modified = [('idtourney', dict(idtourney=0,
                                   idchampionship=tourney_first.idchampionship,
                                   date=tourney_first.date,
                                   description=tourney_first.description))]
    deleted = []
    response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is False
    assert "There cannot be two tourneys" in response.json['message']


def test_admin_reset_nickname(admin_user, session, player_pk):
    for value, expected in ((None, ''), ('  ', ''), (' pk ', 'pk')):
        modified = [('idplayer', dict(idplayer=player_pk.idplayer,
                                      nickname=value))]
        deleted = []
        response = admin_user.post_route(dict(modified_records=JSON.encode(modified),
                                              deleted_records=JSON.encode(deleted)),
                                         'save_changes')
        assert response.json['success'] is True
        assert response.json['message'] == "Ok"

        session.expunge_all()
        pk = session.query(Player).get(player_pk.idplayer)
        assert pk.nickname == expected


def test_anonymous_save(app):
    with pytest.raises(AppError):
        app.post_route({}, 'save_changes')


def test_lele_save_ok(lele_user, player_fata):
    modified = [('idplayer', dict(idplayer=player_fata.idplayer,
                                  agreedprivacy=' ',
                                  language='zz'))]
    deleted = []
    response = lele_user.post_route(dict(modified_records=JSON.encode(modified),
                                         deleted_records=JSON.encode(deleted)),
                                    'save_changes')
    assert response.json['success'] is True
    assert response.json['message'] == "Ok"


def test_lele_save_ko(lele_user, session, player_fata, player_bob):
    assert player_fata.agreedprivacy != 'o'
    assert player_bob.agreedprivacy != 'o'
    previous_language = player_fata.language
    modified = [('idplayer', dict(idplayer=player_fata.idplayer,
                                  agreedprivacy='o',
                                  language='zz')),
                ('idplayer', dict(idplayer=player_bob.idplayer,
                                  agreedprivacy='o',
                                  language='zz'))]
    deleted = []
    response = lele_user.post_route(dict(modified_records=JSON.encode(modified),
                                         deleted_records=JSON.encode(deleted)),
                                    'save_changes')
    assert response.json['success'] is False
    assert response.json['message'] == \
        "Non ti è permessa la modifica di record di cui non sei responsabile!"

    session.expunge_all()
    fata = session.query(Player).get(player_fata.idplayer)
    assert fata.agreedprivacy != 'o'
    assert fata.language == previous_language
    bob = session.query(Player).get(player_bob.idplayer)
    assert bob.agreedprivacy != 'o'


def test_lele_insert_delete_ok(lele_user, session, player_lele, user_lele):
    modified = [('idplayer', dict(idplayer=0,
                                  lastname='Foo',
                                  firstname='bar',
                                  nickname='FooBar'))]
    deleted = []
    response = lele_user.post_route(dict(modified_records=JSON.encode(modified),
                                         deleted_records=JSON.encode(deleted)),
                                    'save_changes')
    assert response.json['success'] is True
    assert response.json['message'] == "Ok"

    foo = session.query(Player).filter_by(nickname='FooBar').one()
    assert foo.firstname == "Bar"
    assert foo.idowner == user_lele.iduser

    modified = []
    deleted = [('idplayer', foo.idplayer)]
    response = lele_user.post_route(dict(modified_records=JSON.encode(modified),
                                         deleted_records=JSON.encode(deleted)),
                                    'save_changes')
    assert response.json['success'] is True
    assert response.json['message'] == "Ok"


def test_insert_tourney_in_bad_championship(guest_user, lele_user, championship_next):
    modified = [('idtourney', dict(idtourney=0,
                                   idchampionship=championship_next.idchampionship,
                                   date=date.today(),
                                   description='Not possible'))]
    deleted = []
    response = guest_user.post_route(dict(modified_records=JSON.encode(modified),
                                          deleted_records=JSON.encode(deleted)),
                                     'save_changes')
    assert response.json['success'] is False
    assert response.json['message'] == "Guest users are not allowed to perform this operation, sorry!"

    response = lele_user.post_route(dict(modified_records=JSON.encode(modified),
                                         deleted_records=JSON.encode(deleted)),
                                    'save_changes')
    assert response.json['success'] is False
    assert response.json['message'] == "Non ti è consentito aggiungere un torneo al campionato selezionato"
