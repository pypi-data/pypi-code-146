# -*- coding: utf-8 -*-
# :Project:   SoL -- Light user interface controller
# :Created:   ven 12 dic 2008 09:18:37 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008–2010, 2013, 2014, 2016, 2018, 2020–2023 Lele Gaifax
#

from datetime import date
from functools import cmp_to_key, partial, wraps
from itertools import groupby
from operator import itemgetter
import logging
import time

from babel.numbers import format_decimal
from itsdangerous import BadData, Signer
from markupsafe import escape
from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPFound,
    HTTPMovedPermanently,
    HTTPNotFound,
    HTTPSeeOther,
    )
from pyramid.view import view_config
from pyramid.settings import asbool
from sqlalchemy import distinct, func, select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import and_, or_, exists
from transaction import doom

from . import get_request_logger
from ..i18n import country_name, translatable_string as _, translator, gettext, ngettext
from ..models import (
    Championship,
    Club,
    Match,
    MergedPlayer,
    Player,
    Rating,
    Tourney,
    )


logger = logging.getLogger(__name__)


@view_config(route_name="lit", renderer="lit/index.mako")
def index(request):
    sess = request.dbsession

    clubs_t = Club.__table__
    players_t = Player.__table__
    championships_t = Championship.__table__
    tourneys_t = Tourney.__table__
    ratings_t = Rating.__table__

    bycountry = {}
    query = (select([clubs_t.c.nationality, clubs_t.c.isfederation])
             .where(or_(exists().where(players_t.c.idclub == clubs_t.c.idclub),
                        exists().where(championships_t.c.idclub == clubs_t.c.idclub))))
    nclubs = nfeds = 0
    for nationality, isfederation in sess.execute(query):
        country = country_name(nationality, request=request)
        nclubs += 1
        counts = bycountry.setdefault((country, nationality), [0, 0, 0])
        counts[0] += 1
        if isfederation:
            nfeds += 1
            counts[1] += 1

    query = (select([players_t.c.nationality, func.count(players_t.c.idplayer)])
             .where(players_t.c.nationality != None)
             .group_by(players_t.c.nationality))
    for nationality, count in sess.execute(query):
        country = country_name(nationality, request=request)
        counts = bycountry.setdefault((country, nationality), [0, 0, 0])
        counts[2] += count

    query = select([func.count(tourneys_t.c.idtourney)])
    ntourneys = sess.execute(query).scalar()

    query = select([func.count(championships_t.c.idchampionship)])
    nchampionships = sess.execute(query).scalar()

    query = select([func.count(players_t.c.idplayer)])
    nplayers = sess.execute(query).scalar()

    query = (select([func.count(distinct(players_t.c.nationality))])
             .where(players_t.c.nationality != None))
    npcountries = sess.execute(query).scalar()

    query = select([func.count(ratings_t.c.idrating)])
    nratings = sess.execute(query).scalar()

    return {
        "_": gettext,
        "bycountry": bycountry,
        "nccountries": len(bycountry),
        "nchampionships": nchampionships,
        "nclubs": nclubs,
        "nfederations": nfeds,
        "ngettext": ngettext,
        "npcountries": npcountries,
        "nplayers": nplayers,
        "nratings": nratings,
        "ntourneys": ntourneys,
        "request": request,
        "session": sess,
        "today": date.today(),
        "version": request.registry.settings['desktop.version'],
    }


def _build_template_data(request, session, entity, **kwargs):
    data = {
        '_': gettext,
        'escape': escape,
        'entity': entity,
        'ngettext': ngettext,
        'request': request,
        'session': session,
        'today': date.today(),
        'version': request.registry.settings['desktop.version'],
    }
    data.update(kwargs)
    return data


def resolve_guids(*pairs):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            t = translator(request)
            params = request.matchdict
            sess = request.dbsession
            entities = []
            # Take paired arguments two-by-two, inline simpler version of
            # itertools::grouper recipe
            ipairs = iter(pairs)
            for pname, iclass in zip(ipairs, ipairs):
                try:
                    guid = params[pname]
                except KeyError:  # pragma: nocover
                    msg = "Missing required argument: %s" % pname
                    get_request_logger(request, logger).warning(msg)
                    raise HTTPBadRequest(msg)
                try:
                    instance = sess.query(iclass).filter_by(guid=guid).one()
                except NoResultFound:
                    if iclass is Player:
                        try:
                            merged = sess.query(MergedPlayer).filter_by(guid=guid).one()
                        except NoResultFound:
                            get_request_logger(request, logger).warning(
                                "Couldn't create page: no %s with guid %s",
                                iclass.__name__.lower(), guid)
                            msg = t(_('No $entity with guid $guid'),
                                    mapping=dict(entity=iclass.__name__.lower(), guid=guid))
                            raise HTTPNotFound(msg)
                        entities.append((guid, merged.player.guid))
                    else:
                        get_request_logger(request, logger).warning(
                            "Couldn't create page: no %s with guid %s",
                            iclass.__name__.lower(), guid)
                        msg = t(_('No $entity with guid $guid'),
                                mapping=dict(entity=iclass.__name__.lower(), guid=guid))
                        raise HTTPNotFound(msg)
                else:
                    entities.append(instance)
            return func(request, sess, entities)
        return wrapper
    return decorator


@view_config(route_name="lit_championship", renderer="lit/championship.mako")
@resolve_guids('guid', Championship)
def championship(request, session, entities):
    cship = entities[0]
    data = _build_template_data(request, session, cship)

    if cship.closed:
        request.response.cache_control.public = True
        request.response.cache_control.max_age = 60*60*24*365

    if cship.prizes != 'centesimal':
        def format_prize(p):  # pragma: no cover
            return format_decimal(p, '###0', request.locale_name)
    else:
        def format_prize(p):
            return format_decimal(p, '###0.00', request.locale_name)
    data["format_prize"] = format_prize
    return data


def compare_cships_by_sequence(c1, c2):
    previous_c1 = {c1.idchampionship}
    previous = c1.previous
    while previous is not None:
        previous_c1.add(previous.idchampionship)
        previous = previous.previous
    if c2.idchampionship in previous_c1:
        return 1
    previous_c2 = {c2.idchampionship}
    previous = c2.previous
    while previous is not None:
        previous_c2.add(previous.idchampionship)
        previous = previous.previous
    if c1.idchampionship in previous_c2:
        return -1
    return 0


@view_config(route_name="lit_club", renderer="lit/club.mako")
@resolve_guids('guid', Club)
def club(request, session, entities):
    club = entities[0]
    # The championships are already ordered by their description: perform another pass
    # taking into account their "previous" relationship
    cships = sorted(club.championships, key=cmp_to_key(compare_cships_by_sequence))
    data = _build_template_data(request, session, club)
    data['championships'] = cships
    return data


@view_config(route_name="lit_club_players", renderer="lit/club_players.mako")
@resolve_guids('guid', Club)
def club_players(request, session, entities):
    club = entities[0]
    query = session.query(Player) \
                   .filter(or_(Player.idclub == club.idclub,
                               Player.idfederation == club.idclub)) \
                   .order_by(Player.lastname, Player.firstname)
    players = groupby(query, lambda player: player.lastname[0])
    return _build_template_data(request, session, club, players=players)


@view_config(route_name="lit_country", renderer="lit/country.mako")
def country(request):
    ccode = request.matchdict['country']

    if ccode == 'None':
        ccode = None

    country = country_name(ccode, request=request)

    sess = request.dbsession

    clubs_t = Club.__table__
    players_t = Player.__table__
    championships_t = Championship.__table__

    clubs = []
    query = (select([clubs_t.c.description,
                     clubs_t.c.guid,
                     clubs_t.c.emblem,
                     clubs_t.c.isfederation,
                     select([func.count(championships_t.c.idchampionship)],
                            championships_t.c.idclub == clubs_t.c.idclub).as_scalar(),
                     select([func.count(players_t.c.idplayer)],
                            or_(players_t.c.idclub == clubs_t.c.idclub,
                                players_t.c.idfederation == clubs_t.c.idclub)).as_scalar()])
             .where(clubs_t.c.nationality == ccode))
    nfeds = 0
    for description, guid, emblem, isfed, nc, np in sess.execute(query):
        clubs.append((description, guid, emblem, isfed, nc, np))
        if isfed:
            nfeds += 1

    query = (select([func.count(players_t.c.idplayer)])
             .where(players_t.c.nationality == ccode))
    nplayers = sess.execute(query).scalar()

    return {
        '_': gettext,
        'ngettext': ngettext,
        'code': ccode,
        'country': country,
        'clubs': clubs,
        'nclubs': len(clubs),
        'nfederations': nfeds,
        'nplayers': nplayers,
        'request': request,
        'today': date.today(),
        'version': request.registry.settings['desktop.version'],
    }


@view_config(route_name="lit_player", renderer="lit/player.mako")
@resolve_guids('guid', Player)
def player(request, session, entities):
    player = entities[0]
    if isinstance(player, tuple):
        old_guid, new_guid = player
        get_request_logger(request, logger).debug(
            "Redirecting from player %s to %s", old_guid, new_guid)
        raise HTTPMovedPermanently(
            request.route_path('lit_player', guid=new_guid))
    else:
        data = _build_template_data(request, session, player)

        def format_prize(p):  # pragma: no cover
            return format_decimal(p, '###0.00', request.locale_name)

        data["format_prize"] = format_prize
        return data


@view_config(route_name="lit_player_opponent", renderer="lit/player_opponent.mako")
@resolve_guids('guid', Player, 'opponent', Player)
def opponent(request, session, entities):
    player = entities[0]
    opponent = entities[1]
    if isinstance(player, tuple) or isinstance(opponent, tuple):
        if isinstance(player, tuple):
            p_old_guid, p_new_guid = player
        else:
            p_old_guid = p_new_guid = player.guid
        if isinstance(opponent, tuple):
            o_old_guid, o_new_guid = opponent
        else:
            o_old_guid = o_new_guid = opponent.guid
        get_request_logger(request, logger).debug(
            "Redirecting from player %s to %s and from opponent %s to %s",
            p_old_guid, p_new_guid, o_old_guid, o_new_guid)
        raise HTTPMovedPermanently(
            request.route_path('lit_player_opponent', guid=p_new_guid, opponent=o_new_guid))
    else:
        return _build_template_data(request, session, player, opponent=opponent)


@view_config(route_name="lit_player_matches", renderer="lit/player_matches.mako")
@resolve_guids('guid', Player)
def matches(request, session, entities):
    player = entities[0]
    if isinstance(player, tuple):
        old_guid, new_guid = player
        get_request_logger(request, logger).debug(
            "Redirecting from player %s to %s", old_guid, new_guid)
        raise HTTPMovedPermanently(
            request.route_path('lit_player', guid=new_guid))
    else:
        return _build_template_data(request, session, player)


@view_config(route_name="lit_players", renderer="lit/players.mako")
def players(request):
    sess = request.dbsession
    pt = Player.__table__
    query = sess.execute(select([func.substr(pt.c.lastname, 1, 1),
                                 pt.c.nationality,
                                 func.count()]).group_by(func.substr(pt.c.lastname, 1, 1),
                                                         pt.c.nationality))
    index = []
    for letter, countsbycountry in groupby(query, itemgetter(0)):
        bycountry = []
        for country in countsbycountry:
            ccode = country[1]
            cname = country_name(ccode, request=request)
            bycountry.append(dict(code=ccode, country=cname, count=country[2]))
        bycountry.sort(key=itemgetter('country'))
        index.append((letter, bycountry))

    return {
        '_': gettext,
        'ngettext': ngettext,
        'today': date.today(),
        'version': request.registry.settings['desktop.version'],
        'index': index,
        'request': request,
    }


@view_config(route_name="lit_players_list", renderer="lit/players_list.mako")
def players_list(request):
    ccode = request.matchdict['country']
    letter = request.params.get('letter')

    if ccode == 'None':
        ccode = None

    cname = country_name(ccode, request=request)

    sess = request.dbsession
    if letter:
        expr = and_(Player.nationality == ccode,
                    Player.lastname.startswith(letter))
    else:
        expr = Player.nationality == ccode
    players = (sess.query(Player)
               .filter(expr)
               .order_by(Player.lastname, Player.firstname))

    return {
        '_': gettext,
        'code': ccode,
        'country': cname,
        'letter': letter,
        'ngettext': ngettext,
        'players': players,
        'request': request,
        'today': date.today(),
        'version': request.registry.settings['desktop.version'],
    }


@view_config(route_name="lit_rating", renderer="lit/rating.mako")
@resolve_guids('guid', Rating)
def rating(request, session, entities):
    rating = entities[0]
    tt = Tourney.__table__
    ntourneys = session.execute(select([func.count(tt.c.idtourney)],
                                       tt.c.idrating == rating.idrating)).first()[0]
    return _build_template_data(request, session, rating, ntourneys=ntourneys)


@view_config(route_name="lit_tourney", renderer="lit/tourney.mako")
@resolve_guids('guid', Tourney)
def tourney(request, session, entities):
    t = translator(request)

    tourney = entities[0]
    turn = request.params.get('turn')
    if turn is not None:
        try:
            turn = int(turn)
        except ValueError:
            get_request_logger(request, logger).warning(
                "Couldn't create page: argument “turn” is not an integer: %r", turn)
            e = t(_('Invalid turn: $turn'), mapping=dict(turn=repr(turn)))
            raise HTTPBadRequest(str(e))
        else:
            if turn > tourney.currentturn:
                get_request_logger(request, logger).warning(
                    "Couldn't create page: argument “turn” is invalid: %r", turn)
                e = t(_('Invalid turn: $turn'), mapping=dict(turn=repr(turn)))
                raise HTTPBadRequest(str(e))

        board = request.params.get('board')
        if board is not None:
            try:
                board = int(board)
            except ValueError:
                get_request_logger(request, logger).warning(
                    "Couldn't create page: argument “board” is not an integer: %r", board)
                e = t(_('Invalid board number: $board'), mapping=dict(board=repr(board)))
                raise HTTPBadRequest(str(e))
            else:
                sess = request.dbsession
                match = sess.query(Match).filter_by(idtourney=tourney.idtourney, turn=turn,
                                                    board=board).one_or_none()
                if match is None:
                    get_request_logger(request, logger).warning(
                        "Couldn't create page: argument “board” is invalid: %r", board)
                    e = t(_('Invalid board number: $board'), mapping=dict(board=repr(board)))
                    raise HTTPBadRequest(str(e))

                match.compute_partial_scores()
        else:
            for match in tourney.matches:
                if match.turn == turn:
                    match.compute_partial_scores()
            match = None
    else:
        match = None

    player = request.params.get('player')
    if player is not None and turn is None and match is None:
        for match in tourney.matches:
            match.compute_partial_scores()
        match = None

    data = _build_template_data(request, session, tourney, turn=turn, match=match,
                                player=player)


    if tourney.championship.prizes != 'centesimal':
        def format_prize(p):
            return format_decimal(p, '###0', request.locale_name)
    else:
        def format_prize(p):
            return format_decimal(p, '###0.00', request.locale_name)

    data["format_prize"] = format_prize
    data["format_decimal"] = partial(format_decimal, locale=request.locale_name)

    if tourney.prized:
        request.response.cache_control.public = True
        request.response.cache_control.max_age = 60*60*24*365

    return data


@view_config(route_name="lit_latest", renderer="lit/latest.mako")
def latest(request):
    t = translator(request)

    n = request.params.get('n')
    if n is not None:
        try:
            n = int(n)
        except ValueError:
            get_request_logger(request, logger).warning(
                "Couldn't create page: argument “n” is not an integer: %r", n)
            e = t(_('Invalid number of tourneys: $n'), mapping=dict(n=repr(n)))
            raise HTTPBadRequest(str(e))
    else:
        n = 20

    sess = request.dbsession
    tourneys = sess.query(Tourney).filter_by(prized=True).order_by(Tourney.date.desc())[:n]

    return {
        '_': gettext,
        'escape': escape,
        'n': len(tourneys),
        'ngettext': ngettext,
        'request': request,
        'session': request.dbsession,
        'today': date.today(),
        'tourneys': tourneys,
        'version': request.registry.settings['desktop.version'],
    }


@view_config(route_name="training_match_form", renderer="lit/training_match.mako")
def training_match_form(request):
    settings = request.registry.settings
    signed_match = request.matchdict['match']
    if signed_match is not None:
        s = Signer(settings['sol.signer_secret_key'])
        try:
            match = s.unsign(signed_match).decode('ascii')
        except BadData:
            if ((asbool(settings.get('desktop.debug', False))
                 and settings.get('desktop.version') != 'test')):
                match = signed_match
            else:
                raise HTTPBadRequest("Bad signature")
        try:
            mid, cnum = match.split('-')
            mid = int(mid)
            cnum = int(cnum)
        except Exception:  # pragma: no cover
            get_request_logger(request, logger).warning(
                "Couldn't create training match form: invalid “match” argument: %r", match)
            raise HTTPBadRequest("Invalid arguments")
    else:
        raise HTTPBadRequest("Missing argument")

    m = request.dbsession.query(Match).get(mid)
    if m is None:
        raise HTTPNotFound()

    if cnum == 1:
        already_entered = (m.boards and m.boards[0].coins1) or m.score1
    else:
        already_entered = (m.boards and m.boards[0].coins2) or m.score2

    if already_entered:
        return HTTPFound(location=request.route_path('lit_tourney', guid=m.tourney.guid,
                                                     _query={'turn': m.tourney.currentturn}))

    if cnum == 1:
        player = m.competitor1.player1
        opponent = m.competitor2.player1
    else:
        player = m.competitor2.player1
        opponent = m.competitor1.player1

    return {
        '_': gettext,
        'escape': escape,
        'ngettext': ngettext,
        'championship': m.tourney.championship,
        'tourney': m.tourney,
        'currentturn': m.tourney.currentturn,
        'player': player,
        'opponent': opponent,
        'request': request,
        'session': request.dbsession,
        'today': date.today(),
        'version': request.registry.settings['desktop.version'],
    }


def errors_to_scores(e1, e2, n):
    """Compute the scores from the errors.

    >>> errors_to_scores(4, 4, 4)
    (1, 1)
    >>> errors_to_scores(1, 1, 4)
    (0, 0)
    >>> errors_to_scores(1, 2, 4)
    (1, 0)
    >>> errors_to_scores(2, 1, 4)
    (0, 1)
    >>> errors_to_scores(10, 21, 4)
    (5, 2)
    >>> errors_to_scores(25, 22, 4)
    (5, 6)
    >>> errors_to_scores(10, 31, 4)
    (8, 2)
    >>> errors_to_scores(100, 100, 4)
    (25, 25)
    >>> errors_to_scores(101, 100, 4)
    (24, 25)
    >>> errors_to_scores(99, 100, 4)
    (25, 24)
    >>> errors_to_scores(199, 120, 4)
    (24, 25)
    >>> errors_to_scores(120, 199, 4)
    (25, 24)
    >>> errors_to_scores(38, 27, 4)
    (7, 10)
    """

    s2 = round(e1 / n)
    s1 = round(e2 / n)

    if s1 > 25 or s2 > 25:
        if s1 > s2:
            s1 = 25
            if s2 >= s1:
                s2 = 24
        elif s1 < s2:
            s2 = 25
            if s1 >= s2:
                s1 = 24
        else:
            s1 = s2 = 25

    if s1 == s2 and e1 != e2:
        if e1 > e2:
            if s1 > 0:
                s1 -= 1
            else:
                s2 += 1
        else:
            if s2 > 0:
                s2 -= 1
            else:
                s1 += 1

    return s1, s2


@view_config(route_name="training_match_form", renderer="lit/training_match.mako",
             request_method="POST")
def store_training_match(request):
    from ..models import Board
    from ..models.bio import changes_logger

    settings = request.registry.settings
    signed_match = request.matchdict['match']
    if signed_match is not None:
        s = Signer(settings['sol.signer_secret_key'])
        try:
            match = s.unsign(signed_match).decode('ascii')
        except BadData:
            if ((asbool(settings.get('desktop.debug', False))
                 and settings.get('desktop.version') != 'test')):
                match = signed_match
            else:
                raise HTTPBadRequest("Bad signature")
        try:
            mid, cnum = match.split('-')
            mid = int(mid)
            cnum = int(cnum)
        except Exception:  # pragma: no cover
            get_request_logger(request, logger).warning(
                "Couldn't store training match results: invalid “match” argument: %r", match)
            raise HTTPBadRequest("Invalid arguments")
    else:
        raise HTTPBadRequest("Missing argument")

    m = request.dbsession.query(Match).get(mid)
    if m is None:
        raise HTTPNotFound()

    if cnum == 1:
        already_entered = (m.boards and m.boards[0].coins1) or m.score1
    else:
        already_entered = (m.boards and m.boards[0].coins2) or m.score2

    if already_entered:
        return HTTPFound(location=request.route_path('lit_tourney', guid=m.tourney.guid,
                                                     _query={'turn': m.tourney.currentturn}))

    if cnum == 1:
        player = m.competitor1.player1
        opponent = m.competitor2.player1
    else:
        player = m.competitor2.player1
        opponent = m.competitor1.player1

    tboards = m.tourney.championship.trainingboards
    errors = request.POST.getall('errors')
    if len(errors) != tboards or not all(e and e.isdigit() and 0 <= int(e) < 100
                                         for e in errors):
        return {
            '_': gettext,
            'error': gettext(_('All boards must be entered,'
                               ' as integer numbers between 0 and 99!')),
            'ngettext': ngettext,
            'championship': m.tourney.championship,
            'tourney': m.tourney,
            'currentturn': m.tourney.currentturn,
            'player': player,
            'opponent': opponent,
            'request': request,
            'session': request.dbsession,
            'today': date.today(),
            'version': request.registry.settings['desktop.version'],
        }

    if not m.boards:
        m.boards = [Board(number=i, **{f'coins{cnum}': int(e)})
                    for i, e in enumerate(errors, 1)]
    else:
        for i, e in enumerate(errors):
            setattr(m.boards[i], f'coins{cnum}', int(e))

    if m.boards:
        if all(b.coins1 is not None and b.coins2 is not None for b in m.boards):
            total1 = sum(b.coins1 or 0 for b in m.boards)
            total2 = sum(b.coins2 or 0 for b in m.boards)
            m.score1, m.score2 = errors_to_scores(total1, total2, tboards)

    changes_logger.info('%r self updated his errors for %r: %s => %s', player, m,
                        ', '.join(str(e) for e in errors), sum(int(e) for e in errors))

    return HTTPFound(location=request.route_path('lit_tourney', guid=m.tourney.guid,
                                                 _query={'turn': m.tourney.currentturn}))


@view_config(route_name="match_form", renderer="lit/match.mako")
def match_form(request):
    settings = request.registry.settings
    signed_board = request.matchdict['board']
    if signed_board is not None:
        s = Signer(settings['sol.signer_secret_key'])
        try:
            board = s.unsign(signed_board).decode('ascii')
        except BadData:  # pragma: no cover
            if asbool(settings.get('desktop.debug', False)):
                board = signed_board
            else:
                raise HTTPBadRequest("Bad signature")
        try:
            tid, board = board.split('-')
            tid = int(tid)
            board = int(board)
        except Exception:  # pragma: no cover
            get_request_logger(request, logger).warning(
                "Couldn't create match form: invalid “board” argument: %r", board)
            raise HTTPBadRequest("Invalid arguments")
    else:  # pragma: no cover
        raise HTTPBadRequest("Missing argument")

    q = request.dbsession.query(Match).join(Tourney)
    q = q.filter(Tourney.idtourney == tid,
                 Match.turn == Tourney.currentturn,
                 Match.board == board)
    m = q.one_or_none()
    if m is None:  # pragma: no cover
        raise HTTPNotFound()
    elif m.tourney.championship.trainingboards:
        raise HTTPBadRequest()
    elif m.score1 or m.score2:
        return HTTPFound(location=request.route_path('lit_tourney', guid=m.tourney.guid,
                                                     _query={'turn': m.tourney.currentturn}))

    if m.tourney.countdownstarted is None:
        elapsed = None
    else:
        elapsed = int(time.time() * 1000) - m.tourney.countdownstarted
        if elapsed > m.tourney.duration * 60 * 1000:  # pragma: no cover
            elapsed = None

    return {
        '_': gettext,
        'escape': escape,
        'ngettext': ngettext,
        'championship': m.tourney.championship,
        'tourney': m.tourney,
        'match': m,
        'currentturn': m.tourney.currentturn,
        'elapsed': elapsed,
        'request': request,
        'session': request.dbsession,
        'today': date.today(),
        'version': request.registry.settings['desktop.version'],
    }


@view_config(route_name="match_form", request_method="POST", renderer='json')
def store_match_boards(request):
    from ..models import Board
    from ..models.bio import changes_logger

    settings = request.registry.settings
    signed_board = request.matchdict['board']
    if signed_board is not None:
        s = Signer(settings['sol.signer_secret_key'])
        try:
            board = s.unsign(signed_board).decode('ascii')
        except BadData:  # pragma: no cover
            if asbool(settings.get('desktop.debug', False)):
                board = signed_board
            else:
                raise HTTPBadRequest("Bad signature")
        try:
            tid, board = board.split('-')
            tid = int(tid)
            board = int(board)
        except Exception:  # pragma: no cover
            get_request_logger(request, logger).warning(
                "Couldn't store match results: invalid “board” argument: %r", board)
            raise HTTPBadRequest("Invalid arguments")
    else:  # pragma: no cover
        raise HTTPBadRequest("Missing argument")

    q = request.dbsession.query(Match).join(Tourney)
    q = q.filter(Tourney.idtourney == tid,
                 Match.turn == Tourney.currentturn,
                 Match.board == board)
    m = q.one_or_none()
    if m is None:  # pragma: no cover
        raise HTTPNotFound()
    elif m.tourney.championship.trainingboards:
        raise HTTPBadRequest()

    getter = request.params.get

    if m.score1 or m.score2 or int(getter('turn', 0)) != m.tourney.currentturn:
        return HTTPSeeOther(
            location=request.route_path('lit_tourney', guid=m.tourney.guid,
                                        _query={'turn': m.tourney.currentturn}))

    breaker = getter('breaker')
    if breaker is not None:
        m.breaker = breaker

    boards = m.boards
    nboards = len(boards)
    translate = request.localizer.translate
    for boardno in range(1, 10):
        queen = getter(f'queen_{boardno}')
        coins1 = getter(f'coins_{boardno}_1')
        coins2 = getter(f'coins_{boardno}_2')

        if queen is coins1 is coins2 is None:
            break

        if boardno > nboards:
            board = Board(number=boardno)
            boards.append(board)
        else:
            board = boards[boardno - 1]

        coins1 = 0 if coins1 is None or not coins1.isdigit() else int(coins1)
        coins2 = 0 if coins2 is None or not coins2.isdigit() else int(coins2)

        if coins1 > 0 and coins2 > 0:
            doom()
            return {'success': False,
                    'message': translate(_('Cannot accept both coins in board $board!',
                                           mapping=dict(board=boardno)))}

        if queen is not None:
            if queen not in ('1', '2'):  # pragma: no cover
                doom()
                return {'success': False,
                        'message': translate(_('Bad value for Queen in board $board!',
                                               mapping=dict(board=boardno)))}

        if not 0 <= coins1 < 10:
            doom()
            return {'success': False,
                    'message': translate(_('Out of range value for coins 1 in board'
                                           ' $board!', mapping=dict(board=boardno)))}

        if not 0 <= coins2 < 10:
            doom()
            return {'success': False,
                    'message': translate(_('Out of range value for coins 2 in board'
                                           ' $board!', mapping=dict(board=boardno)))}

        board.coins1 = coins1
        board.coins2 = coins2
        board.queen = queen

    if 'endgame' in request.params:
        m.score1 = int(getter('score1'))
        if not 0 <= m.score1 <= 25:  # pragma: no cover
            doom()
            return {'success': False,
                    'message': translate(_('Out of range value for score 1!'))}

        m.score2 = int(getter('score2'))
        if not 0 <= m.score2 <= 25:
            doom()
            return {'success': False,
                    'message': translate(_('Out of range value for score 2!'))}

        changes_logger.info('%r has been self-compiled', m)
        return HTTPSeeOther(
            location=request.route_path('lit_tourney', guid=m.tourney.guid,
                                        _query={'turn': m.tourney.currentturn,
                                                'board': m.board}))
    else:
        changes_logger.info('%r is being self-compiled', m)
        if m.tourney.countdownstarted is None:
            elapsed = None
        else:
            elapsed = int(time.time() * 1000) - m.tourney.countdownstarted
            if elapsed > m.tourney.duration * 60 * 1000:  # pragma: no cover
                elapsed = None
        return {
            'success': True, 'message': 'Ok',
            'elapsed': elapsed
        }
